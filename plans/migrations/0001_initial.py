# Generated by Django 3.0.8 on 2020-12-16 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('duration', models.CharField(max_length=50)),
                ('notifications', models.IntegerField()),
                ('emails', models.IntegerField()),
                ('apps', models.IntegerField()),
                ('description', models.TextField(null=True)),
            ],
        ),
    ]
