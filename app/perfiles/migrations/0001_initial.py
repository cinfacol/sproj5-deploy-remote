# Generated by Django 4.0.4 on 2022-06-05 02:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import perfiles.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Accounts',
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(default='users/user_default_profile.png', upload_to=perfiles.models.user_directory_path_profile)),
                ('banner', models.ImageField(default='users/user_default_bg.jpg', upload_to=perfiles.models.user_directory_path_banner)),
                ('gender', models.CharField(choices=[('male', 'Hombre'), ('female', 'Mujer')], default='male', max_length=10)),
                ('verified', models.CharField(choices=[('unverified', 'No verificado'), ('verified', 'Verificado')], default='unverified', max_length=10)),
                ('url', models.CharField(blank=True, max_length=80, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, max_length=150, null=True)),
                ('phone', models.CharField(max_length=50)),
                ('mobile', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuario',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('shipping_address', models.CharField(max_length=150, verbose_name='Dirección de envío')),
                ('billing_address', models.CharField(max_length=150, verbose_name='Dirección de facturacion')),
                ('pais', django_countries.fields.CountryField(max_length=2)),
                ('departamento', models.CharField(max_length=100)),
                ('ciudad', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=100, verbose_name='Zip code')),
                ('address_type', models.CharField(choices=[('Billing', 'B'), ('Shipping', 'S')], default='Shipping', max_length=8)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Direccion',
                'verbose_name_plural': 'Direcciones',
            },
        ),
    ]
