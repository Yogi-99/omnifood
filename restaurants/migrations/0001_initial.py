# Generated by Django 2.2.4 on 2019-08-03 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='restaurant_logo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]