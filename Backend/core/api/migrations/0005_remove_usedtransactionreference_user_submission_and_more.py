# Generated by Django 5.1.3 on 2024-11-17 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_usedtransactionreference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usedtransactionreference',
            name='user_submission',
        ),
        migrations.AddField(
            model_name='usersubmission',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='usersubmission',
            name='payment_verification_response',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usersubmission',
            name='payment_verified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddConstraint(
            model_name='usersubmission',
            constraint=models.UniqueConstraint(condition=models.Q(('payment_status', 'success')), fields=('transaction_reference',), name='unique_successful_transaction'),
        ),
        migrations.DeleteModel(
            name='UsedTransactionReference',
        ),
    ]