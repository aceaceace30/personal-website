# Generated by Django 3.1.2 on 2020-10-14 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0010_auto_20200507_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=1200, null=True)),
                ('back_end', models.CharField(max_length=255)),
                ('front_end', models.CharField(max_length=255)),
                ('classification', models.CharField(choices=[('', '----'), ('company', 'Company'), ('freelance', 'Freelance'), ('personal', 'Personal')], max_length=30)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='project_details/')),
                ('git_link', models.URLField(blank=True, null=True)),
                ('website_link', models.URLField(blank=True, null=True)),
                ('ordering', models.PositiveIntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Portfolio',
        ),
    ]
