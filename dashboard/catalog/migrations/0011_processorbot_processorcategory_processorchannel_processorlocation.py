# Generated by Django 2.1 on 2018-11-29 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_auto_20181102_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessorBot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'processor_bots',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessorCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'processor_categories',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessorChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.TextField()),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'processor_channels',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessorLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=100)),
                ('state_symbol', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'processor_locations',
                'managed': False,
            },
        ),
    ]