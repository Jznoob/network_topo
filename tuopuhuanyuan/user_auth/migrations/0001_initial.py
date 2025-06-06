# Generated by Django 5.2 on 2025-05-21 06:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100, unique=True, verbose_name='重置令牌')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('expires_at', models.DateTimeField(verbose_name='过期时间')),
                ('is_used', models.BooleanField(default=False, verbose_name='是否已使用')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reset_tokens', to='user_auth.user')),
            ],
            options={
                'verbose_name': '密码重置令牌',
                'verbose_name_plural': '密码重置令牌',
            },
        ),
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP地址')),
                ('user_agent', models.TextField(verbose_name='用户代理')),
                ('login_time', models.DateTimeField(auto_now_add=True, verbose_name='登录时间')),
                ('is_successful', models.BooleanField(default=True, verbose_name='是否成功')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='login_histories', to='user_auth.user')),
            ],
            options={
                'verbose_name': '登录历史',
                'verbose_name_plural': '登录历史',
                'ordering': ['-login_time'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='手机号')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='头像')),
                ('bio', models.TextField(blank=True, max_length=500, null=True, verbose_name='个人简介')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='user_auth.user')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
    ]
