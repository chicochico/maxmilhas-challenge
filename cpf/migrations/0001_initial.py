# Generated by Django 2.0 on 2017-12-06 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CPF',
            fields=[
                ('number', models.CharField(max_length=14, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CPF_Blacklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cpf.CPF')),
            ],
        ),
    ]
