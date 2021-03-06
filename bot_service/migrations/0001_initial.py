# Generated by Django 3.1.3 on 2020-11-27 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, null=True)),
                ('videos', models.FileField(null=True, upload_to='videos/', verbose_name='video')),
                ('gif', models.FileField(null=True, upload_to='gifs/', verbose_name='gif')),
            ],
        ),
        migrations.CreateModel(
            name='ChannelPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='post/image/')),
                ('Description', models.TextField(default=False, null=True)),
                ('Post_time', models.DateTimeField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=False, null=True)),
                ('number', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('name', models.CharField(default='', max_length=100, null=True)),
                ('id', models.IntegerField(default=False, primary_key=True, serialize=False, verbose_name='Product Code')),
                ('image', models.ImageField(null=True, upload_to='image/')),
                ('album', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='bot_service.album')),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=False, null=True)),
                ('counter', models.IntegerField(default=0, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_service.product')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(default=False, max_length=50, primary_key=True, serialize=False)),
                ('order', models.ManyToManyField(to='bot_service.Order')),
            ],
            options={
                'ordering': ['user_id'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='bot_service.product'),
        ),
    ]
