# Generated by Django 3.1.7 on 2021-10-26 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='imagen',
            field=models.ImageField(blank=True, default='perfil/gelionz1.jpg/', null=True, upload_to='perfil/'),
        ),
    ]
