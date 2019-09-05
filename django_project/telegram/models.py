from django.db import models
from django.utils import timezone

# Create your models here.


class Chat(models.Model):
    chat_id = models.CharField(max_length=200, unique=True, primary_key=True)
    telephone_number = models.CharField(max_length=20, null=True, blank=True)
    chat_owner_contacts = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    student = models.BooleanField(blank=True, null=True)
    specialization = models.CharField(max_length=30, null=True, blank=True)
    knowledge_level = models.CharField(max_length=20, null=True, blank=True)
    language = models.CharField(max_length=3, default='U')
    time = models.DateTimeField()
    place = models.CharField(max_length=20)
    # @classmethod
    # def new_start(cls, chat_id):
    #     chat = Chat.objects.get(chat_id=chat_id)
    #     chat.start_count = chat.start_count + 1
    #     chat.save()


# class Worker(models.Model):
#     user_id = models.CharField(max_length=100)
#     chat = models.ForeignKey(
#         'Chat', related_name='workers', on_delete=models.CASCADE)
#     contact_info = models.TextField(max_length=200, blank=True, null=True)


# class Student(models.Model):
#     user_id = models.CharField(max_length=100)
#     specialization = models.CharField(max_length=20)
#     knowledge_level = models.CharField(max_length=20, null=True, blank=True)
#     date_start = models.DateTimeField(default=timezone.now())
#     chat = models.ForeignKey(
#         'Chat', related_name='students', on_delete=models.CASCADE)
#     contact_info = models.TextField(max_length=200, blank=True, null=True)

#     @classmethod
#     def get_knowledge_level(cls, student_id):
#         student = Student.objects.get(id=student_id)
#         if student.knowledge_level == "startU":
#             return "початковий"
#         elif student.knowledge_level == "startR":
#             return "начальный"
#         elif student.knowledge_level == "middleU":
#             return "середній"
#         elif student.knowledge_level == "middleR":
#             return "средний"
#         elif student.knowledge_level == "advancedU":
#             return "високий"
#         elif student.knowledge_level == "advancedR":
#             return "высокий"

#     @classmethod
#     def set_knowledge_level(cls, student_id, k_level):
#         student = Student.objects.get(id=student_id)
#         student.knowledge_level = k_level
#         student.save()
#         return Student.get_knowledge_level(student_id)
