# Generated by Django 4.2.4 on 2023-10-14 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0046_alter_reviewreply_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_note',
            field=models.TextField(blank=True, default=''),
        ),
    ]
