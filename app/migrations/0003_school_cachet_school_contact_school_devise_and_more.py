# Generated by Django 5.1.4 on 2024-12-18 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_school_user_alter_classe_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='cachet',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='contact',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='devise',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='logo',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='signature_principale',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='photos',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='academic_year',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='image_url',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='sexe',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
