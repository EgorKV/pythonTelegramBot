from django.contrib import admin
from django.urls import path, include
from .views import botresponse, ListStudents

urlpatterns = [
    path('899061394:AAFefj4ey2FMpzOkI08CN1Xri6R9SuiEFRo/', botresponse),
    path('getInfo/', ListStudents.as_view()),
]
