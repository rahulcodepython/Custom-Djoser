# Generated by Django 4.2.6 on 2023-10-20 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_resetpasswordcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
