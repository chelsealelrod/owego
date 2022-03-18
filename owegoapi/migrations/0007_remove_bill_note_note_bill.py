# Generated by Django 4.0.3 on 2022-03-16 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('owegoapi', '0006_remove_tag_note_tag_tag_bill_tag_alter_bill_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='note',
        ),
        migrations.AddField(
            model_name='note',
            name='bill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='owegoapi.bill'),
        ),
    ]