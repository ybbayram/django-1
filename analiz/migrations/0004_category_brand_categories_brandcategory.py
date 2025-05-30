# Generated by Django 5.1.4 on 2025-03-02 18:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analiz', '0003_brand_brandfeature_brandfeaturevalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='brand',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='brands', to='analiz.category'),
        ),
        migrations.CreateModel(
            name='BrandCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analiz.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analiz.category')),
            ],
            options={
                'unique_together': {('brand', 'category')},
            },
        ),
    ]
