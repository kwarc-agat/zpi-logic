from rest_framework import serializers
from .models import *
from django.core.serializers.json import DjangoJSONEncoder

class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name', 'surname', 'email', 'title')

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'topic', 'subject', 'adminEmail', 'lecturer')

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('index', 'name', 'surname', 'email', 'teamId', 'isTeamAdmin')

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'fromUser', 'toUser', 'subject', 'msgLines', 'type', 'isRead')
