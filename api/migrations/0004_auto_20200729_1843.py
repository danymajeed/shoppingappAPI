# Generated by Django 3.0.8 on 2020-07-29 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200729_1843'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_name',
            new_name='title',
        ),
    ]