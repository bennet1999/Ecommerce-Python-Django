# Generated by Django 4.1.1 on 2022-12-03 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='reason',
            field=models.CharField(default='Reason', max_length=200),
        ),
    ]
