# Generated by Django 4.2.16 on 2024-12-07 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_remove_bannermodel_index_remove_bannermodel_url_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bannermodel',
            options={'verbose_name': '首页轮播图资源表', 'verbose_name_plural': '首页轮播图资源表'},
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='file_product',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='文件所属产品类型'),
        ),
    ]
