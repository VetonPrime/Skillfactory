# Generated by Django 4.2.2 on 2023-06-24 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_comment_reply_to_comment_subscriptions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_news',
            field=models.CharField(choices=[('PO', 'ПОСТ')], max_length=2),
        ),
    ]