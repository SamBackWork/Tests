from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, QuestionLink, UserAnswer
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.contrib import messages


def survey_view(request, question_id=None):
    if question_id is None:
        question = Question.objects.order_by('order').first()
        if not question:
            return HttpResponseNotFound("No questions found.")
    else:
        question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        answer_text = request.POST.get('answer')
        user = request.user if request.user.is_authenticated else None

        if question.question_type in ('single_choice', 'multiple_choice'):
            try:
                answer = Answer.objects.get(question=question, text=answer_text)
                UserAnswer.objects.create(question=question, answer=answer, user=user)
            except Answer.DoesNotExist:
                messages.error(request, "Invalid answer for this question.")
                return render(request, 'survey_question.html', {'question': question})

        elif question.question_type == 'text':
            if not answer_text:
                messages.error(request, "Answer is required.")
                return render(request, 'survey_question.html', {'question': question})
            UserAnswer.objects.create(question=question, text_answer=answer_text, user=user)

        else:
            messages.error(request, 'Unsupported question type')
            return render(request, 'survey_question.html', {'question': question})

        # Вот здесь определяем следующий вопрос *ПОСЛЕ* сохранения ответа
        next_question = get_next_question(question, answer_text)

        if next_question:
            return redirect('survey_view', question_id=next_question.pk)
        else:
            # Опрос завершен
            return render(request, 'survey_complete.html')  # Убедись что тут!!!

    # Этот return ТОЛЬКО для отображения вопроса (GET-запрос)
    return render(request, 'survey_question.html', {'question': question})


def get_next_question(current_question, current_answer_text):
    """
    Определяет следующий вопрос на основе текущего вопроса и ответа.
    """
    # Сначала пробуем найти ответ в БД, если вопрос предполагает выбор
    if current_question.question_type in ('single_choice', 'multiple_choice'):
        try:
            current_answer = Answer.objects.get(question=current_question, text=current_answer_text)
        except Answer.DoesNotExist:
            # Если ответа нет, ищем связи для любого ответа, если вопрос предполагает предопределенный ответ, то это ошибка
            current_answer = None

    else:
        current_answer = None  # Для текстовых и других вопросов

    # Ищем связь с конкретным ответом
    if current_answer:  # Проверяем, что current_answer существует
        try:
            link = QuestionLink.objects.get(source_question=current_question, source_answer=current_answer)
            return link.target_question
        except QuestionLink.DoesNotExist:
            pass

    # Ищем связь для любого ответа (важно для текстовых и других типов)
    try:
        link = QuestionLink.objects.get(source_question=current_question, source_answer=None)
        return link.target_question
    except QuestionLink.DoesNotExist:
        pass

    # Если связей нет, получаем следующий вопрос по порядку
    next_question = Question.objects.filter(order__gt=current_question.order).order_by('order').first()
    return next_question
