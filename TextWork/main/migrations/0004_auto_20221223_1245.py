# Generated by Django 3.1.7 on 2022-12-23 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20221214_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название тега')),
                ('description', models.TextField(verbose_name='Краткое описание тега')),
            ],
        ),
        migrations.AlterField(
            model_name='articles',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.category', verbose_name='Тег'),
        ),
    ]
