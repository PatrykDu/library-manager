# Generated by Django 4.2 on 2023-05-07 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('published_date', models.DateField()),
                ('isbn_10', models.CharField(max_length=10)),
                ('isbn_13', models.CharField(max_length=13)),
                ('page_count', models.IntegerField()),
                ('thumbnail', models.CharField(max_length=255)),
                ('authors', models.ManyToManyField(to='books.author')),
                ('language', models.ManyToManyField(to='books.language')),
            ],
        ),
    ]
