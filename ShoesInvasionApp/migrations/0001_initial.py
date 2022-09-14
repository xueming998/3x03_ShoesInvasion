# Generated by Django 3.2.15 on 2022-09-14 12:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='admin_users',
            fields=[
                ('admin_user_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('admin_username', models.CharField(max_length=255)),
                ('admin_password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='products',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=45)),
                ('product_price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('review', models.TextField(default='')),
                ('product_info', models.TextField(default='')),
                ('product_brand', models.CharField(max_length=45)),
                ('product_category', models.CharField(max_length=45)),
                ('gender_type', models.CharField(max_length=1)),
                ('available', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='users',
            fields=[
                ('user_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=45)),
                ('lname', models.CharField(max_length=45)),
                ('address', models.TextField(default='')),
                ('email', models.CharField(max_length=255)),
                ('dob', models.DateField(default=datetime.date.today)),
                ('gender', models.CharField(max_length=1)),
                ('user_username', models.CharField(max_length=255)),
                ('user_password', models.CharField(max_length=255)),
                ('forget_pwd_code', models.CharField(max_length=10)),
                ('phone', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='transactions',
            fields=[
                ('transaction_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('createdDate', models.DateField(default=datetime.date.today)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShoesInvasionApp.users')),
            ],
        ),
        migrations.CreateModel(
            name='transaction_details',
            fields=[
                ('transaction_details_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0)),
                ('size', models.CharField(max_length=5)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShoesInvasionApp.products')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShoesInvasionApp.transactions')),
            ],
        ),
        migrations.CreateModel(
            name='Shopping_Cart',
            fields=[
                ('shopping_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('product_id', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('size', models.CharField(max_length=5)),
                ('color', models.CharField(max_length=45)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('status', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShoesInvasionApp.users')),
            ],
        ),
        migrations.CreateModel(
            name='product_quantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=5)),
                ('quantity', models.IntegerField(default=0)),
                ('color', models.CharField(max_length=45)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShoesInvasionApp.products')),
            ],
        ),
    ]
