from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import UserSubmission, EmailTemplate, AdditionalEmail
from .serializers import UserSubmissionSerializer, EmailTemplateSerializer, AdditionalEmailSerializer
from .services import EmailService, PaystackService


class UserSubmissionView(generics.ListCreateAPIView):
    queryset = UserSubmission.objects.all()
    serializer_class = UserSubmissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        transaction_reference = serializer.validated_data.get('transaction_reference')

        # Check for existing submission
        existing_user = UserSubmission.objects.filter(email=email).first()
        
        if existing_user:
            # If user exists but payment is pending and new reference is provided
            if not existing_user.is_paid and transaction_reference:
                verification_response = self._verify_payment(
                    existing_user, 
                    transaction_reference
                )
                if verification_response.get('is_paid'):
                    return Response({
                        'message': 'Payment verified successfully',
                        'user': UserSubmissionSerializer(existing_user).data
                    }, status=status.HTTP_200_OK)
                
            return Response({
                'error': 'User with this email already exists',
                'is_paid': existing_user.is_paid
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create new user submission
        user_submission = serializer.save()

        # Verify payment if reference is provided
        if transaction_reference:
            verification_response = self._verify_payment(
                user_submission, 
                transaction_reference
            )
            if not verification_response.get('is_paid'):
                return Response({
                    'error': 'Payment verification failed',
                    'details': verification_response.get('error')
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _verify_payment(self, user_submission, transaction_reference):
        """Helper method to verify payment and update models"""
        try:
            # Check if transaction reference has already been used successfully
            existing_success = UserSubmission.objects.filter(
                transaction_reference=transaction_reference,
                payment_status='success'
            ).exists()
            
            if existing_success:
                return {
                    'is_paid': False,
                    'error': 'Transaction reference has already been used'
                }
            
            # Update the user submission with the transaction reference
            user_submission.transaction_reference = transaction_reference
            
            verification_response = PaystackService.verify_payment(transaction_reference)
            user_submission.payment_verification_response = verification_response
            
            if not verification_response:
                user_submission.payment_status = 'failed'
                user_submission.save()
                return {
                    'is_paid': False,
                    'error': 'Payment verification failed'
                }

            data = verification_response.get('data', {})
            is_successful = (
                verification_response.get('status') and 
                data.get('status') == 'success'
            )

            if is_successful:
                # Update user payment status
                user_submission.is_paid = True
                user_submission.payment_status = 'success'
                user_submission.payment_verified_at = timezone.now()
                user_submission.save()

                # Send confirmation email
                try:
                    EmailService.send_single_email(
                        subject="Payment Confirmation",
                        body=f"Thank you for your payment, {user_submission.name}!",
                        recipient=user_submission.email
                    )
                except Exception as e:
                    print(f"Failed to send confirmation email: {str(e)}")
            else:
                user_submission.payment_status = 'failed'
                user_submission.save()

            return {
                'is_paid': is_successful,
                'error': None if is_successful else 'Payment verification failed'
            }

        except Exception as e:
            user_submission.payment_status = 'failed'
            user_submission.save()
            return {
                'is_paid': False,
                'error': str(e)
            }
        
class EmailTemplateView(generics.ListCreateAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

class EmailTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

class AdditionalEmailView(generics.ListCreateAPIView):
    queryset = AdditionalEmail.objects.all()
    serializer_class = AdditionalEmailSerializer


class SendMailView(APIView):
    def post(self, request):
        template_id = request.data.get('template_id')
        recipient_type = request.data.get('recipient_type', 'all')
        
        try:
            template = EmailTemplate.objects.get(id=template_id)
            recipients = []
            
            # Gather recipients based on type
            if recipient_type in ['all', 'submissions']:
                submissions = UserSubmission.objects.all()
                recipients.extend(submissions)
            
            if recipient_type in ['all', 'additional']:
                additional = AdditionalEmail.objects.all()
                recipients.extend(additional)
            
            # Send emails
            try:
                EmailService.send_bulk_email(template, recipients)
                return Response({
                    'message': 'Emails sent successfully',
                    'recipient_count': len(recipients)
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'error': f'Failed to send emails: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except EmailTemplate.DoesNotExist:
            return Response({
                'error': 'Template not found'
            }, status=status.HTTP_404_NOT_FOUND)
            

@api_view(['GET'])
def get_submission_count(request):
    count = UserSubmission.objects.count()
    return Response({'count': count})