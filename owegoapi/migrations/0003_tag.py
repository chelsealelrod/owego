# Generated by Django 4.0.3 on 2022-03-09 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owegoapi', '0002_remove_bill_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('note_tag', models.ManyToManyField(to='owegoapi.note')),
            ],
        ),
    ]