# Generated by Django 3.2 on 2023-10-31 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_adminapp', '0011_auto_20231011_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offerprice',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(),
        ),
    ]
