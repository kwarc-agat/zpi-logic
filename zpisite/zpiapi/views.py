from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponse

from .serializers import *
from .models import *
from django.core import serializers
from .helpers import *


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('id')
    serializer_class = TeacherSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('id')
    serializer_class = TeamSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('index')
    serializer_class = StudentSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('id')
    serializer_class = MessageSerializer

def confirmPassword(request):
    email = request.GET.get('email', '')
    password = request.GET.get('password', '')

    return JsonResponse({"email": email, 
                         "password": password})

def markMessageAsRead(request):
    email = request.GET.get('email', '')
    messageId = request.GET.get('messageId', '')

    return JsonResponse({"email": email, 
                         "messageId": messageId})

def acceptInvitation(request):
    email = request.GET.get('email', '')
    messageId = request.GET.get('messageId', '')

    return JsonResponse({"email": email, 
                         "messageId": messageId})

def deleteMessage(email, messageId):

    return JsonResponse({"delete-email": email,
                         "delete-msgID": messageId})

def getMessages(email):

    return JsonResponse({"get-email": email})

def manageMessages(request):
    email = request.GET.get('email', '')
    messageId = request.GET.get('messageId', '')
    if messageId=='':
        return getMessages(email)
    else:
        return deleteMessage(email, messageId)


def leaveTeam(request):
    email = request.GET.get('email', '')

    return JsonResponse({"email": email})

def getStudents(request):
    all_students = Student.objects.all()
    response = []
    for student in all_students:
        response.append(parseStudentObject(student))

    return JsonResponse(response, safe=False)

def getStudent(request, inputEmail):
    student = Student.objects.get(email=inputEmail)
    return JsonResponse(parseStudentObject(student))

def getTeachers(request):
    all_teachers = Teacher.objects.all()
    response = []
    for teacher in all_teachers:
        response.append(getTeacherById(teacher.id))

    return JsonResponse(response, safe=False)

def addTeamLecturer(request):
    teamId = request.GET.get('teamId', '')
    email = request.GET.get('email', '')

    return JsonResponse({"teamId": teamId, 
                         "email": email})

def leaveTeam(request):
    email = request.GET.get('email', '')
    teamId = request.GET.get('teamId', '')

    return JsonResponse({"email": email,
                         "teamId": teamId})

def removeTeam(request):
    teamId = request.GET.get('teamId', '')

    return JsonResponse({"teamId": teamId})

def getAllTeams(request):
    all_teams = Team.objects.all()
    response = []
    for team in all_teams:
        response.append(getTeamById(team.id))

    return JsonResponse(response, safe=False)

def getTeam(id):
    return JsonResponse(getTeamById(id))

def createTeam(request):
    id = request.GET.get('id', '')

    return JsonResponse({"id-post": id})

def manageTeam(request, id):
    if request.method == 'GET':
        return getTeam(id)
    elif request.method == 'POST':
        return createTeam(request)















