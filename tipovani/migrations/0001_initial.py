# Generated by Django 5.1.7 on 2025-04-01 08:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('poradatel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vybrany_team', models.CharField(choices=[('A', 'Tým A'), ('B', 'Tým B')], max_length=1)),
                ('kolo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tipy', to='poradatel.kolo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'kolo')},
            },
        ),
    ]
