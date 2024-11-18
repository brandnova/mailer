# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import UserSubmission, EmailTemplate, AdditionalEmail

@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'email', 
        'phone',
        'colored_payment_status',
        'transaction_reference',
        'created_at',
        'payment_verified_at'
    ]
    list_filter = ['payment_status', 'is_paid', 'created_at']
    search_fields = ['name', 'email', 'phone', 'transaction_reference']
    readonly_fields = [
        'payment_verified_at', 
        'payment_verification_response',
        'created_at'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Payment Information', {
            'fields': (
                'transaction_reference',
                'payment_status',
                'is_paid',
                'payment_verified_at',
                'payment_verification_response'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def colored_payment_status(self, obj):
        colors = {
            'pending': 'orange',
            'success': 'green',
            'failed': 'red'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.payment_status, 'black'),
            obj.get_payment_status_display()
        )
    colored_payment_status.short_description = 'Payment Status'

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of successful payments
        if obj and obj.payment_status == 'success':
            return False
        return super().has_delete_permission(request, obj)

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'created_at']
    search_fields = ['name', 'subject', 'body']
    readonly_fields = ['created_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'subject')
        }),
        ('Template Content', {
            'fields': ('body',),
            'description': 'Available variables: {{ name }}, {{ email }}'
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(AdditionalEmail)
class AdditionalEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'created_at']
    search_fields = ['email', 'name']
    readonly_fields = ['created_at']