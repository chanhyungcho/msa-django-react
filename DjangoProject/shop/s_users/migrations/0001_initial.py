# Generated by Django 4.1.3 on 2022-11-30 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SUser',
            fields=[
                ('s_userid', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('nickname', models.TextField()),
                ('password', models.TextField()),
                ('point', models.TextField()),
            ],
            options={
                'db_table': 's_users',
            },
        ),
    ]
