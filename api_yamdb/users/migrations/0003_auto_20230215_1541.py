# Generated by Django 3.2 on 2023-02-15 15:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230215_0743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-id',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Код подтверждения'),
        ),
    ]