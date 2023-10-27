# Generated by Django 4.2.6 on 2023-10-27 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aimodels', '0002_rename_category_categorie'),
    ]

    operations = [
        migrations.CreateModel(
            name='AiModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('price', models.FloatField()),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aimodels', to='aimodels.categorie')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
