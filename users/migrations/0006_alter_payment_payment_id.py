# Generated by Django 5.0.1 on 2024-04-02 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_payment_payment_id_payment_payment_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Идентификатор платежа'),
        ),
    ]
