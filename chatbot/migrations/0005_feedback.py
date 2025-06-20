# Generated by Django 5.2.3 on 2025-06-16 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_budgetestimate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('comment', models.TextField()),
                ('language', models.CharField(choices=[('fr', 'Français'), ('mg', 'Malgache')], default='fr', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
