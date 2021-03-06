# Generated by Django 2.2.3 on 2020-04-14 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docid', models.IntegerField()),
                ('docname', models.CharField(max_length=50)),
                ('deptno', models.IntegerField()),
                ('deptname', models.CharField(max_length=15)),
                ('passwd', models.CharField(max_length=50)),
                ('fees', models.IntegerField()),
                ('isdoc', models.BooleanField(default=True)),
            ],
        ),
    ]
