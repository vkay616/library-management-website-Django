# Generated by Django 4.0 on 2022-09-28 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0003_issuedbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('available', 'Available for issuing'), ('issued', 'Issued by someone')], default='available', max_length=10),
        ),
        migrations.DeleteModel(
            name='IssuedBook',
        ),
    ]
