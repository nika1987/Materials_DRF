# Generated by Django 5.0.1 on 2024-03-13 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_payment_stripe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(default=2, max_length=255, unique=True, verbose_name='Идентификатор платежа'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_link',
            field=models.URLField(blank=True, max_length=400, null=True, verbose_name='Ссылка на оплату'),
        ),
    ]
