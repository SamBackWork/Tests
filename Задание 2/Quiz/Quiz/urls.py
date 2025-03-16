from django.contrib import admin
from django.urls import path
from firstapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('survey/', views.survey_view, name='survey_view'),  # Начало
    path('survey/<int:question_id>/', views.survey_view, name='survey_view'),  # С question_id
]
