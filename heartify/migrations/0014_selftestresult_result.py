# Generated by Django 4.2.7 on 2023-12-28 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heartify', '0013_personprofile_alter_selftestresult_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='selftestresult',
            name='result',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]