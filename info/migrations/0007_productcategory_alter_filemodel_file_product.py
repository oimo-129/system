# Generated by Django 5.1.1 on 2025-01-02 09:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_alter_news_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='产品类别')),
            ],
            options={
                'verbose_name': '产品类别',
                'verbose_name_plural': '产品类别',
            },
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='file_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='info.productcategory', verbose_name='文件所属产品类型'),
        ),
    ]
