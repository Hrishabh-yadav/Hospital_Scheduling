# Generated by Django 2.2.3 on 2020-05-09 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_auto_20200509_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='finedate',
            field=models.DateField(),
        ),
    ]
