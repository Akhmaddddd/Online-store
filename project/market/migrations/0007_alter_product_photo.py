# Generated by Django 4.2.6 on 2023-11-11 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_alter_product_photo_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(default='Нет фото', upload_to='photos/', verbose_name='Картинка продукта'),
        ),
    ]