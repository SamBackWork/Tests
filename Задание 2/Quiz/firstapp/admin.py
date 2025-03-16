from django.contrib import admin
from .models import Question, Answer, QuestionLink


class AnswerInline(admin.TabularInline):  # Или StackedInline, если хочешь другой вид
    model = Answer
    extra = 1  # Количество пустых форм для добавления ответов


class QuestionLinkInline(admin.TabularInline):
    model = QuestionLink
    fk_name = "source_question"  # Указываем, какое поле ForeignKey использовать
    extra = 1
    autocomplete_fields = ['target_question']  # Для удобства выбора целевого вопроса
    # raw_id_fields = ('target_question',)  # Если очень много вопросов


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline, QuestionLinkInline]
    list_display = ('text', 'question_type', 'order')  # Поля в списке
    list_editable = ('order',)  # Редактирование порядка прямо в списке
    search_fields = ['text']
    ordering = ['order']
    list_filter = ('question_type',)

    def display_links(self, obj):
        # Формируем список связей для отображения
        links = obj.outgoing_links.all()  # Исходящие связи
        return format_html_join(
            '; ',
            "{} -> {}",
            ((self.format_link(link), link.target_question.text) for link in links)
        )

    display_links.short_description = 'Outgoing Links'  # Заголовок колонки

    def format_link(self, link):
        # Фоматирование текста связи
        if link.source_answer:
            return f"{link.source_question.text} <b style='color: green'>({link.source_answer.text})</b>"
        else:
            return f"{link.source_question.text} <b style='color: red'>(Any Answer)</b>"


class QuestionLinkAdmin(admin.ModelAdmin):
    list_display = ('source_question', 'source_answer', 'target_question')
    autocomplete_fields = ['source_question', 'target_question']
    # raw_id_fields = ('source_question', 'target_question')


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionLink)  # Отдельно QuestionLink тоже можно оставить
