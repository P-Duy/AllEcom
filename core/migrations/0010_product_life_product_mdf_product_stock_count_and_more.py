# Generated by Django 5.0 on 2023-12-22 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_productimages_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='life',
            field=models.CharField(default='100 ngày', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='mdf',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_count',
            field=models.CharField(default='10', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(default='Organic', max_length=100),
        ),
    ]
