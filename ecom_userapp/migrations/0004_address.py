# Generated by Django 3.2 on 2023-10-31 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_adminapp', '0012_auto_20231031_1207'),
        ('ecom_userapp', '0003_cart_user_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=20)),
                ('nearest_land_mark', models.CharField(max_length=20)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecom_adminapp.product')),
                ('user_login', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecom_userapp.userloginn')),
            ],
        ),
    ]