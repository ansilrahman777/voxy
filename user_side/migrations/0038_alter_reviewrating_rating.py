# Generated by Django 4.2.4 on 2023-10-13 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0037_reviewrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
