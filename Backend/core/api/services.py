import pytz
import requests
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.template import Template, Context
from datetime import datetime

class PaystackService:
    @staticmethod
    def verify_payment(reference):
        verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }
        
        try:
            response = requests.get(verify_url, headers=headers)
            response.raise_for_status()  # Raise exception for non-200 status codes
            return response.json()
        except requests.RequestException as e:
            print(f"Payment verification error: {str(e)}")
            return None

class EmailService:
    @staticmethod
    def send_bulk_email(template, recipients):
        """
        Send bulk emails using a template to multiple recipients
        """
        # Parse template variables
        subject_template = Template(template.subject)
        body_template = Template(template.body)
        
        # Prepare emails
        messages = []
        for recipient in recipients:
            # Create context for template
            context = Context({
                'email': recipient.email if hasattr(recipient, 'email') else recipient,
                'name': recipient.name if hasattr(recipient, 'name') else '',
            })
            
            # Render templates with context
            subject = subject_template.render(context)
            body = body_template.render(context)
            
            # Create email tuple
            email_message = (
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [recipient.email if hasattr(recipient, 'email') else recipient]
            )
            messages.append(email_message)
        
        # Send mass mail
        return send_mass_mail(messages, fail_silently=False)

    @staticmethod
    def send_single_email(subject, body, recipient):
        """
        Send a single email to one recipient
        """
        return send_mail(
            subject=subject,
            message=body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient],
            fail_silently=False
        )