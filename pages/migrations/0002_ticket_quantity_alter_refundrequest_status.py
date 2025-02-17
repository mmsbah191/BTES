# Generated by Django 5.1.2 on 2024-11-03 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='refundrequest',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('cancelled', 'Cancelled')], max_length=20),
        ),
    ]
