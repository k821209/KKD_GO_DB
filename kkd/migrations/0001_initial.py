# Generated by Django 2.0 on 2017-12-17 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GO', models.CharField(max_length=20)),
                ('Pvalue', models.CharField(max_length=20)),
                ('Odd', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('defin', models.TextField()),
            ],
        ),
    ]
