# Generated by Django 4.0.4 on 2022-05-15 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockCodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comapny_code', models.TextField()),
                ('company_name', models.CharField(max_length=50)),
                ('stock_market_type', models.CharField(max_length=30)),
                ('business_type_code', models.TextField()),
                ('business_type', models.TextField()),
            ],
        ),
    ]
