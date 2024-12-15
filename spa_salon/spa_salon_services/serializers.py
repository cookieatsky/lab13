# serializers.py
from rest_framework import serializers
from .models import News  # Импортируйте вашу модель новостей

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'  # Или укажите конкретные поля, которые хотите сериализовать