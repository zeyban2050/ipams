# Generated by Django 4.0.3 on 2022-03-17 16:34

import ckeditor.fields
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
            name='AuthorRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CollaborationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PSCEDClassification',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PublicationLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('year_accomplished', models.CharField(max_length=30)),
                ('abstract', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('abstract_file', models.FileField(default='', upload_to='abstract/')),
                ('is_ip', models.BooleanField(default=False)),
                ('for_commercialization', models.BooleanField(default=False)),
                ('community_extension', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('representative', models.CharField(max_length=100)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('adviser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('classification', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='records.classification')),
                ('psced_classification', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='records.pscedclassification')),
            ],
        ),
        migrations.CreateModel(
            name='RecordType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecordUploadStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('record_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='records.recordtype')),
            ],
        ),
        migrations.CreateModel(
            name='ResearchRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposal', to='records.record')),
                ('research', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='research', to='records.record')),
            ],
        ),
        migrations.CreateModel(
            name='RecordUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('is_ip', models.BooleanField(default=False)),
                ('for_commercialization', models.BooleanField(default=False)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.record')),
                ('record_upload_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.recorduploadstatus')),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.upload')),
            ],
        ),
        migrations.AddField(
            model_name='record',
            name='record_type',
            field=models.ForeignKey(blank=True, default=3, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='records.recordtype'),
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('venue', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('conference_level', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='records.conferencelevel')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.record')),
            ],
        ),
        migrations.CreateModel(
            name='Collaboration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry', models.CharField(max_length=100)),
                ('institution', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('collaboration_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='records.collaborationtype')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.record')),
            ],
        ),
        migrations.CreateModel(
            name='CheckedUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date_checked', models.DateTimeField(auto_now_add=True)),
                ('checked_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('record_upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.recordupload')),
            ],
        ),
        migrations.CreateModel(
            name='CheckedRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('checked_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.record')),
            ],
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget_allocation', models.FloatField()),
                ('funding_source', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('budget_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='records.budgettype')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.record')),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('author_role', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='records.authorrole')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.record')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('name', models.CharField(max_length=200, null=True)),
                ('isbn', models.CharField(blank=True, max_length=50, null=True)),
                ('issn', models.CharField(blank=True, max_length=50, null=True)),
                ('isi', models.CharField(blank=True, max_length=50, null=True)),
                ('year_published', models.CharField(blank=True, max_length=50, null=True)),
                ('record', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='records.record')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('publication_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='records.publicationlevel')),
            ],
        ),
    ]
