# Generated by Django 2.1.4 on 2019-01-04 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bots',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('build_id', models.CharField(max_length=255)),
            ],
        ),
    ]