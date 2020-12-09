# Generated by Django 3.0.8 on 2020-12-09 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0007_userapp_customer_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('app_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_notification', to='app.App')),
            ],
        ),
    ]
