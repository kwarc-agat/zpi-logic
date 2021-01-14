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
    # NOT IMPLEMENTED - TABLE NOT CREATED
    return JsonResponse({"email": email, 
                         "password": password})

def markMessageAsRead(request):
    email = request.GET.get('email', '')
    messageId = request.GET.get('messageId', '')

    try:
        msg = Message.objects.get(toUser=email, id=messageId)
        msg.isRead = True
        msg.save()
        return HttpResponse(status=200)

    except Message.DoesNotExist:
        return JsonResponse({"message": "Message does not exist"})
       
def acceptInvitation(request):
    email = request.GET.get('email', '')
    messageId = request.GET.get('messageId', '')

    # NOT IMPLEMENTED - WHAT TEAM AM I IN?
    return JsonResponse({"email": email, 
                         "messageId": messageId})

def deleteMessage(email, messageId):
    try:
        msg = Message.objects.get(toUser=email, id=messageId)
        msg.delete()
        return HttpResponse(status=200)

    except Message.DoesNotExist:
        return JsonResponse({"message": "Message does not exist"})

def getMessages(email):
    my_messages = Message.objects.filter(toUser=email)
    response = []
    for msg in my_messages:
        response.append(getMessageById(msg.id))

    return JsonResponse(response, safe=False)

def manageMessages(request):
    email = request.GET.get('email', '')
    messageId = request.GET.get('messageId', '')
    if messageId=='':
        return getMessages(email)
    else:
        return deleteMessage(email, messageId)

def leaveTeamStudents(request):
    email = request.GET.get('email', '')
    # NOT IMPLEMENTED - DIFFERENCE WITH leaveTeamTeams???
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
    inputTeamId = request.GET.get('teamId', '')
    inputEmail = request.GET.get('email', '')
    
    try:
        team = Team.objects.get(id=inputTeamId)
        teacher = Teacher.objects.get(email=inputEmail)

        teams_common_teacher = Team.objects.filter(lecturer=teacher)
        if len(teams_common_teacher) >= 3:
            return JsonResponse({"message": "Teacher has 3 teams already"})
        else:
            team.lecturer = teacher
            team.save()
            return HttpResponse(status=200)

    except Team.DoesNotExist:
        return JsonResponse({"message": "Team does not exist"})
    except Teacher.DoesNotExist:
        return JsonResponse({"message": "Teacher does not exist"})

def leaveTeamTeams(request):
    email = request.GET.get('email', '')
    teamId = request.GET.get('teamId', '')
    # NOT IMPLEMENTED - ADMIN CANT LEAVE TEAM ONLY REMOVE DIFFERENCE WITH leaveTeamStudents???
    return JsonResponse({"email": email,
                         "teamId": teamId})

def removeTeam(request):
    teamId = request.GET.get('teamId', '')
    try:
        team = Team.objects.get(id=teamId)
        team_students = Student.objects.filter(teamId=team)
        if len(team_students) > 1:
            return JsonResponse({"message": "Team has multiple members"})
        else:
            team.delete()
        return HttpResponse(status=200)

    except Team.DoesNotExist:
        return JsonResponse({"message": "Team does not exist"})

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
    # NOT IMPLEMENTED - ADMIN EMAIL AS USER EMAIL
    return JsonResponse({"id-post": id})

def manageTeam(request, id):
    if request.method == 'GET':
        return getTeam(id)
    elif request.method == 'POST':
        return createTeam(request)















