# Generated by Django 3.0.3 on 2020-02-15 08:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20200215_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectapproval',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
