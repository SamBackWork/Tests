from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Question(models.Model):
    QUESTION_TYPES = (
        ('text', 'Text Input'),
        ('single_choice', 'Single Choice'),
        ('multiple_choice', 'Multiple Choice'),
        # Добавь другие типы по необходимости
    )

    text = models.CharField(max_length=255, verbose_name="Question Text")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name="Question Type")
    order = models.PositiveIntegerField(default=0, blank=False, null=False,
                                        help_text="The order of the question in the survey.")

    class Meta:
        ordering = ['order']  # Сортируем вопросы по полю order
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name="Question")
    text = models.CharField(max_length=255, verbose_name="Answer Text")

    # Можно добавить value, если нужны числовые значения ответов, баллы и т.д.
    # value = models.IntegerField(null=True, blank=True, verbose_name="Answer Value")

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.text


class QuestionLink(models.Model):
    source_question = models.ForeignKey(Question, related_name='outgoing_links', on_delete=models.CASCADE,
                                        verbose_name="Source Question")
    source_answer = models.ForeignKey(Answer, related_name='links', on_delete=models.CASCADE, null=True, blank=True,
                                      verbose_name="Source Answer (Leave blank for any answer)")
    target_question = models.ForeignKey(Question, related_name='incoming_links', on_delete=models.CASCADE,
                                        verbose_name="Target Question")

    class Meta:
        verbose_name = "Question Link"
        verbose_name_plural = "Question Links"
        unique_together = ('source_question', 'source_answer', 'target_question')  # Защита от дублей

    def __str__(self):
        if self.source_answer:
            return f"{self.source_question.text} ({self.source_answer.text}) -> {self.target_question.text}"
        else:
            return f"{self.source_question.text} (Any Answer) -> {self.target_question.text}"

    def clean(self):
        # Валидация: проверяем, что target_question != source_question
        if self.target_question == self.source_question:
            raise ValidationError("Target question cannot be the same as the source question.")

        # Валидация: если source_answer указан, проверяем что он принадлежит source_question
        if self.source_answer and self.source_answer.question != self.source_question:
            raise ValidationError("The selected answer does not belong to the source question.")


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="user_answers",
                                 verbose_name="Question")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True, related_name="user_answers",
                               verbose_name="Chosen Answer")
    text_answer = models.TextField(null=True, blank=True,
                                   verbose_name="Text Answer")  # Для текстовых ответов и других типов, где нет готовых вариантов
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_answers",
                             verbose_name="User")  # Связь с пользователем, если нужна

    # Можешь добавить created_at = models.DateTimeField(auto_now_add=True) для отслеживания времени ответа

    class Meta:
        verbose_name = "User Answer"
        verbose_name_plural = "User Answers"

    def __str__(self):
        if self.answer:
            return f"User: {self.user}, Question: {self.question.text}, Answer: {self.answer.text}"
        elif self.text_answer:
            return f"User: {self.user}, Question: {self.question.text}, Text Answer: {self.text_answer}"
        else:
            return f"User:{self.user}, Question: {self.question.text}, No answer"

    def clean(self):
        if self.answer and self.text_answer:
            raise ValidationError("Only one of 'answer' or 'text_answer' should be provided.")
        if not self.answer and not self.text_answer:
            raise ValidationError("Either 'answer' or 'text_answer' must be provided.")
        if self.answer and self.answer.question != self.question:
            raise ValidationError("Selected answer does not belong to the question.")
