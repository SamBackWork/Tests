# Generated by Django 5.1.7 on 2025-03-16 16:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Question Text')),
                ('question_type', models.CharField(choices=[('text', 'Text Input'), ('single_choice', 'Single Choice'), ('multiple_choice', 'Multiple Choice')], max_length=20, verbose_name='Question Type')),
                ('order', models.PositiveIntegerField(default=0, help_text='The order of the question in the survey.')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Answer Text')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='firstapp.question', verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.TextField(blank=True, null=True, verbose_name='Text Answer')),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='firstapp.answer', verbose_name='Chosen Answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='firstapp.question', verbose_name='Question')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User Answer',
                'verbose_name_plural': 'User Answers',
            },
        ),
        migrations.CreateModel(
            name='QuestionLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='links', to='firstapp.answer', verbose_name='Source Answer (Leave blank for any answer)')),
                ('source_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_links', to='firstapp.question', verbose_name='Source Question')),
                ('target_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_links', to='firstapp.question', verbose_name='Target Question')),
            ],
            options={
                'verbose_name': 'Question Link',
                'verbose_name_plural': 'Question Links',
                'unique_together': {('source_question', 'source_answer', 'target_question')},
            },
        ),
    ]
