from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['time', 'place', 'language', 'name', 'telephone_number',
                  'chat_owner_contacts', 'student', 'knowledge_level', 'specialization']
