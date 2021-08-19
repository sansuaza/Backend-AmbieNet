# Generated by Django 3.2.3 on 2021-08-19 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0010_auto_20210818_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cant_user_complaints',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='is_banned',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='PostComplaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='modified at')),
                ('reported_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('reporting_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
