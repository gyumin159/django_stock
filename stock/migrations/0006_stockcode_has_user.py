# Generated by Django 3.2.13 on 2022-05-18 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_newsdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockcode',
            name='has_user',
            field=models.BooleanField(default=False),
        ),
    ]