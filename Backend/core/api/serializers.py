from rest_framework import serializers
from .models import UserSubmission, EmailTemplate, AdditionalEmail

class UserSubmissionSerializer(serializers.ModelSerializer):
    payment_status = serializers.CharField(read_only=True)
    
    class Meta:
        model = UserSubmission
        fields = ['id', 'name', 'email', 'phone', 'transaction_reference', 
                 'created_at', 'is_paid', 'payment_status']
        read_only_fields = ['is_paid']

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'

class AdditionalEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalEmail
        fields = '__all__'