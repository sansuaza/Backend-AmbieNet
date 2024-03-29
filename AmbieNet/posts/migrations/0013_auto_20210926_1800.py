# Generated by Django 3.2.7 on 2021-09-26 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_alter_post_validator_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='type_report',
            field=models.CharField(blank=True, choices=[('COM', 'common'), ('ADV', 'advanced')], default='COM', max_length=4),
        ),
        migrations.AlterField(
            model_name='post',
            name='type_post',
            field=models.CharField(choices=[('REP', 'report'), ('CAT', 'catastrophe'), ('NEW', 'positive_news'), ('COMP', 'complaint')], max_length=4),
        ),
    ]
