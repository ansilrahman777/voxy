# Generated by Django 4.2.4 on 2023-10-20 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0057_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('mobile', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=500)),
            ],
        ),
    ]
