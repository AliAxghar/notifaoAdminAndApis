# Generated by Django 3.0.8 on 2020-12-21 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billing_id', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('interval', models.CharField(max_length=255, null=True)),
                ('notifications', models.IntegerField(blank=True, null=True)),
                ('apps', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=555, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_method', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('charge_id', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_id', models.CharField(blank=True, max_length=255, null=True)),
                ('subscription_id', models.CharField(blank=True, max_length=255, null=True)),
                ('subscription_created_at', models.CharField(blank=True, max_length=255, null=True)),
                ('charge_receipt_url', models.CharField(blank=True, max_length=555, null=True)),
            ],
        ),
    ]
