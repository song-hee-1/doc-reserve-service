# Generated by Django 4.2.5 on 2023-09-17 13:37

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
            name='Clinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='병원 이름', max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='의사 이름', max_length=20)),
                ('introduction', models.TextField(blank=True, help_text='의사 소개')),
                ('credentials', models.TextField(blank=True, help_text='의사 약력')),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='clinics.clinic')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NonInsuredMedicalCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(help_text='비급여 진료 과목 코드', max_length=100)),
                ('name', models.CharField(help_text='비급여 진료 과목 이름', max_length=40)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(help_text='진료과 코드', max_length=50)),
                ('name', models.CharField(help_text='진료과 이름', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DoctorSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], help_text='요일', max_length=3)),
                ('start_time', models.TimeField(help_text='진료 시작 시간', null=True)),
                ('end_time', models.TimeField(help_text='진료 종료 시간', null=True)),
                ('lunch_start_time', models.TimeField(blank=True, help_text='점심 시작 시간', null=True)),
                ('lunch_end_time', models.TimeField(blank=True, help_text='점심 종료 시간', null=True)),
                ('is_day_off', models.BooleanField(default=False, help_text='휴무 여부')),
                ('reason_for_day_off', models.CharField(blank=True, choices=[('Regular', '정기 휴무'), ('Personal', '개인 휴무'), ('Other', '기타 이유')], help_text='휴무 이유', max_length=10)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='clinics.doctor')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='non_insured_medical_category',
            field=models.ManyToManyField(blank=True, help_text='비급여 진료과목', related_name='clinics', to='clinics.noninsuredmedicalcategory'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='specialities',
            field=models.ManyToManyField(help_text='진료과', related_name='doctors', to='clinics.speciality'),
        ),
        migrations.CreateModel(
            name='ClinicAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending_approve', '대기'), ('complete', '수락')], default='pending_approve', help_text='진료 요청 상태', max_length=20)),
                ('desired_date', models.DateTimeField(help_text='진료 희망 날짜')),
                ('expired_at', models.DateTimeField(help_text='진료 요청 만료 시간')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clinic_appointments', to='clinics.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clinic_appointments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
