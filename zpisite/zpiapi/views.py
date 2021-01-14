from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponse

from .serializers import *
from .models import *
from django.core import serializers
from .helpers import *
from .constans import *


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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('email')
    serializer_class = UserSerializer


def confirmPassword(request):
    email = request.GET.get('email', '')
    password = request.GET.get('password', '')
    try:
        user = User.objects.get(email=email)
        if user.password == password:
            return JsonResponse({"accountType": user.accountType})
        else:
            return JsonResponse({"id": ErrorCode.INCORRECT_PASSWORD,
                                 "message": MessageInfo.INCORRECT_PASSWORD})
    except User.DoesNotExist:
        return JsonResponse({"message": MessageInfo.NOT_EXISTS_USER})


def markMessageAsRead(request):
    email = request.GET.get('email', '')
    messageId = request.GET.get('messageId', '')

    try:
        msg = Message.objects.get(toUser=email, id=messageId)
        msg.isRead = True
        msg.save()
        return HttpResponse(status=200)

    except Message.DoesNotExist:
        return JsonResponse({"message": MessageInfo.NOT_EXISTS_MESSAGE})
       
def acceptInvitation(request):
    inputEmail = request.GET.get('email', '')
    inputTeamId = request.GET.get('teamId', '')

    try:
        student = Student.objects.get(email=inputEmail)
        team = Team.objects.get(id=inputTeamId)

        if student.teamId is None:
            student.teamId = team
            student.save()
            return JsonResponse({"teamId": team.id})

        else:
            return JsonResponse({"id": ErrorCode.ERR_STUDENT_HAS_TEAM,
                             "message": MessageInfo.HAS_TEAM})
    except Student.DoesNotExist:
        return JsonResponse({"id": ErrorCode.NOT_EXISTS_STUDENT,
                             "message": MessageInfo.NOT_EXISTS_STUDENT})
    except Team.DoesNotExist:
        return JsonResponse({"id": ErrorCode.NOT_EXISTS_TEAM,
                                "message": MessageInfo.NOT_EXISTS_TEAM})

def deleteMessage(email, messageId):
    try:
        msg = Message.objects.get(toUser=email, id=messageId)
        msg.delete()
        return HttpResponse(status=200)

    except Message.DoesNotExist:
        return JsonResponse({"message": MessageInfo.NOT_EXISTS_MESSAGE})

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

def leaveTeam(request):
    inputEmail = request.GET.get('email', '')
    
    try:
        student = Student.objects.get(email=inputEmail)
        if student.teamId is not None:
            if student.isTeamAdmin:
                return JsonResponse({"message": MessageInfo.IS_TEAM_ADMIN})
            else:
                student.teamId = None
                student.save()
                return HttpResponse()
        else:
            return JsonResponse({"message": MessageInfo.HAS_NO_TEAM})

    except Student.DoesNotExist:
        return JsonResponse({"id": ErrorCode.NOT_EXISTS_STUDENT,
                             "message": MessageInfo.NOT_EXISTS_STUDENT})

def getStudents(request):
    all_students = Student.objects.all()
    response = []
    for student in all_students:
        response.append(parseStudentObject(student))

    return JsonResponse(response, safe=False)

def getStudent(request, inputEmail):
    try:
        student = Student.objects.get(email=inputEmail)
        return JsonResponse(parseStudentObject(student))
    except Student.DoesNotExist:
        return JsonResponse({"id": ErrorCode.NOT_EXISTS_STUDENT,
                                "message": MessageInfo.NOT_EXISTS_STUDENT})

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
            return JsonResponse({"message": MessageInfo.TOO_MANY_TEAMS})
        else:
            team.lecturer = teacher
            team.save()
            return HttpResponse(status=200)

    except Team.DoesNotExist:
        return JsonResponse({"message": MessageInfo.NOT_EXISTS_TEAM})
    except Teacher.DoesNotExist:
        return JsonResponse({"message": MessageInfo.NOT_EXISTS_TEACHER})

def removeTeam(request):
    teamId = request.GET.get('teamId', '')
    try:
        team = Team.objects.get(id=teamId)
        team_students = Student.objects.filter(teamId=team)
        if len(team_students) > 1:
            return JsonResponse({"message": MessageInfo.HAS_MEMBERS})
        else:
            team.delete()
        return HttpResponse(status=200)

    except Team.DoesNotExist:
        return JsonResponse({"message": MessageInfo.NOT_EXISTS_TEAM})

def getAllTeams(request):
    all_teams = Team.objects.all()
    response = []
    for team in all_teams:
        response.append(getTeamById(team.id))

    return JsonResponse(response, safe=False)

def getTeam(id):
    return JsonResponse(getTeamById(id))

def createTeam(studentEmail):
    try:
        student = Student.objects.get(email=studentEmail)
        if student.teamId is not None:
            return JsonResponse({"id": 0,
                                 "teamId": student.teamId.id,
                                "message": MessageInfo.HAS_TEAM})
        else:
            team = Team.objects.create(adminEmail=studentEmail)
            student.isTeamAdmin = True
            student.save()
            return JsonResponse({"teamId": team.id})

    except Student.DoesNotExist:
        return JsonResponse({"id": ErrorCode.NOT_EXISTS_STUDENT,
                             "message": MessageInfo.NOT_EXISTS_STUDENT})

def manageTeam(request, param):
    if request.method == 'GET':
        return getTeam(param)
    elif request.method == 'POST':
        return createTeam(param)















