# Generated by Django 4.2.6 on 2023-10-28 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_alter_category_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(default='Нет фото', upload_to='photos/', verbose_name='Картинка продукта'),
        ),
    ]
