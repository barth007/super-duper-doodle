# Generated by Django 5.0.8 on 2024-08-08 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=150)),
                ('content', models.FileField(upload_to='uploaded_newsletters/')),
            ],
        ),
    ]
