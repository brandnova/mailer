from django.db import models
from django.utils import timezone

class UserSubmission(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    payment_status = models.CharField(
        max_length=10, 
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    payment_verified_at = models.DateTimeField(null=True, blank=True)
    payment_verification_response = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.email} ({self.payment_status})"

    class Meta:
        ordering = ['-created_at']
        # Ensure transaction reference is unique when payment is successful
        constraints = [
            models.UniqueConstraint(
                fields=['transaction_reference'],
                condition=models.Q(payment_status='success'),
                name='unique_successful_transaction'
            )
        ]

# Update EmailTemplate model
class EmailTemplate(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    body = models.TextField(help_text="Available variables: {{ name }}, {{ email }}")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class AdditionalEmail(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-created_at']
