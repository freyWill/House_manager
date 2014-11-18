# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import spending.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ammount', models.FloatField(validators=[spending.models.validate_deposit])),
                ('theDate', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MonthlyBill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('utility', models.FloatField()),
                ('internet', models.FloatField()),
                ('theDate', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ammount', models.FloatField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ammount', models.FloatField()),
                ('description', models.CharField(max_length=220)),
                ('theDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('person', models.ForeignKey(to='spending.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ammount', models.FloatField(validators=[spending.models.validate_withdraw])),
                ('theDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('person', models.ForeignKey(to='spending.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='monthlybill',
            name='person',
            field=models.ForeignKey(to='spending.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deposit',
            name='person',
            field=models.ForeignKey(to='spending.Person'),
            preserve_default=True,
        ),
    ]
