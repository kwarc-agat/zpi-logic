from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
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
            print("Password OK")
            return JsonResponse({"accountType": int(user.accountType)})
        else:
            response = {"id": ErrorCode.INCORRECT_PASSWORD, "message": MessageInfo.INCORRECT_PASSWORD}
            return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        response = {"id": ErrorCode.INCORRECT_PASSWORD, "message": MessageInfo.NOT_EXISTS_USER}
        return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)


def markMessageAsRead(request):
    email = request.GET.get('email', '')
    messageId = request.GET.get('messageId', '')

    try:
        msg = Message.objects.get(toUser=email, id=messageId)
        msg.isRead = True
        msg.save()
        return HttpResponse(status=200)

    except Message.DoesNotExist:
        return HttpResponse({"id": ErrorCode.NOT_EXISTS_MESSAGE,
                             "message": MessageInfo.NOT_EXISTS_MESSAGE},
                            status=status.HTTP_404_NOT_FOUND)


def acceptInvitation(request):
    inputEmail = request.GET.get('email', '')
    inputMsgId = request.GET.get('messageId', '')

    try:
        student = Student.objects.get(email=inputEmail)
        msg = Message.objects.get(id=inputMsgId)
        team = Team.objects.get(adminEmail=msg.fromUser)

        if student.teamId is None:
            teamMembers = Student.objects.filter(teamId=team)
            if len(teamMembers) >= 4:
                return HttpResponse({"id": ErrorCode.TOO_MANY_MEMBERS,
                                     "message": MessageInfo.TOO_MANY_MEMBERS},
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                student.teamId = team
                student.save()
                msg.delete()
                responseMsg = Message.objects.create(fromUser=student.email,
                                                     toUser=msg.fromUser,
                                                     subject=MessageInfo.SUBJ_INVITATION,
                                                     msgLines=MessageInfo.MSG_INVITATION_ACCEPT)
                return JsonResponse({"teamId": team.id})

        else:
            return HttpResponse({"id": ErrorCode.ERR_STUDENT_HAS_TEAM,
                                 "message": MessageInfo.HAS_TEAM},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Student.DoesNotExist:
        return HttpResponse({"id": ErrorCode.NOT_EXISTS_STUDENT,
                             "message": MessageInfo.NOT_EXISTS_STUDENT},
                            status=status.HTTP_404_NOT_FOUND)
    except Team.DoesNotExist:
        return HttpResponse({"id": ErrorCode.NOT_EXISTS_TEAM,
                             "message": MessageInfo.NOT_EXISTS_TEAM},
                            status=status.HTTP_404_NOT_FOUND)
    except Message.DoesNotExist:
        return HttpResponse({"id": ErrorCode.NOT_EXISTS_MESSAGE,
                             "message": MessageInfo.NOT_EXISTS_MESSAGE},
                            status=status.HTTP_404_NOT_FOUND)


def deleteMessage(email, messageId):
    try:
        msg = Message.objects.get(toUser=email, id=messageId)
        msg.delete()
        return HttpResponse(status=status.HTTP_200_OK)

    except Message.DoesNotExist:
        return HttpResponse({"id": ErrorCode.NOT_EXISTS_MESSAGE,
                             "message": MessageInfo.NOT_EXISTS_MESSAGE},
                            status=status.HTTP_404_NOT_FOUND)


def getMessages(email):
    my_messages = Message.objects.filter(toUser=email)
    response = []
    for msg in my_messages:
        response.append(getMessageById(msg.id))

    return JsonResponse(response, safe=False)


def manageMessages(request):
    email = request.GET.get('email', '')
    messageId = request.GET.get('messageId', '')
    if messageId == '':
        return getMessages(email)
    else:
        return deleteMessage(email, messageId)


def leaveTeam(request):
    inputEmail = request.GET.get('email', '')
    try:
        student = Student.objects.get(email=inputEmail)
        print(student)
        if student.teamId is not None:
            if student.isTeamAdmin:
                return HttpResponse({"id": ErrorCode.IS_TEAM_ADMIN,
                                     "message": MessageInfo.IS_TEAM_ADMIN},
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                student.teamId = None
                student.save()
                return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse({"id": ErrorCode.HAS_NO_TEAM,
                                 "message": MessageInfo.HAS_NO_TEAM},
                                status=status.HTTP_404_NOT_FOUND)

    except Student.DoesNotExist:
        return HttpResponse({"id": ErrorCode.NOT_EXISTS_STUDENT,
                             "message": MessageInfo.NOT_EXISTS_STUDENT},
                            status=status.HTTP_404_NOT_FOUND)


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
        return HttpResponse({"id": ErrorCode.NOT_EXISTS_STUDENT,
                             "message": MessageInfo.NOT_EXISTS_STUDENT},
                            status=status.HTTP_404_NOT_FOUND)


def getTeachers(request):
    all_teachers = Teacher.objects.all()
    response = []
    for teacher in all_teachers:
        response.append(getTeacherByEmail(teacher.email))

    return JsonResponse(response, safe=False)


def addTeamLecturer(request):
    inputTeamId = request.GET.get('teamId', '')
    inputEmail = request.GET.get('email', '')

    try:
        team = Team.objects.get(id=inputTeamId)
        teacher = Teacher.objects.get(email=inputEmail)

        teams_common_teacher = Team.objects.filter(lecturer=teacher)
        if len(teams_common_teacher) >= 3:
            return HttpResponse({"id": ErrorCode.TOO_MANY_TEAMS,
                                 "message": MessageInfo.TOO_MANY_TEAMS},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            team.lecturer = teacher
            team.save()
            return HttpResponse(status=status.HTTP_200_OK)

    except Team.DoesNotExist:
        return HttpResponse({"id": ErrorCode.NOT_EXISTS_TEAM,
                             "message": MessageInfo.NOT_EXISTS_TEAM},
                            status=status.HTTP_404_NOT_FOUND)
    except Teacher.DoesNotExist:
        return HttpResponse({"id": ErrorCode.NOT_EXISTS_TEACHER,
                             "message": MessageInfo.NOT_EXISTS_TEACHER},
                            status=status.HTTP_404_NOT_FOUND)


def removeTeam(teamId):
    try:
        team = Team.objects.get(id=teamId)
        team_students = Student.objects.filter(teamId=team)
        if len(team_students) > 1:
            return HttpResponse({"id": ErrorCode.HAS_MEMBERS,
                                 "message": MessageInfo.HAS_MEMBERS},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            team.delete()
            return HttpResponse(status=status.HTTP_200_OK)

    except Team.DoesNotExist:
        return HttpResponse({"id": ErrorCode.NOT_EXISTS_TEAM,
                             "message": MessageInfo.NOT_EXISTS_TEAM},
                            status=status.HTTP_404_NOT_FOUND)


def getAllTeams(request):
    all_teams = Team.objects.all()
    response = []
    for team in all_teams:
        response.append(getTeamById(team.id))

    return JsonResponse(response, safe=False)


def getTeam(email):
    return JsonResponse(getTeamByUserEmail(email))


def createTeam(studentEmail):
    print("creating team")

    try:
        student = Student.objects.get(email=studentEmail)
        if student.teamId is not None:
            return HttpResponse({"id": ErrorCode.HAS_TEAM,
                                 "teamId": student.teamId.id,
                                 "message": MessageInfo.HAS_TEAM},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            team = Team.objects.create(adminEmail=studentEmail)
            student.isTeamAdmin = True
            student.teamId = team
            student.save()
            return JsonResponse({"teamId": team.id})

    except Student.DoesNotExist:
        return HttpResponse({"id": ErrorCode.NOT_EXISTS_STUDENT,
                             "message": MessageInfo.NOT_EXISTS_STUDENT},
                            status=status.HTTP_404_NOT_FOUND)


def manageTeam(request, param):
    if request.method == 'GET':
        return getTeam(param)
    elif request.method == 'PUT':
        return createTeam(param)
    elif request.method == 'DELETE':
        return removeTeam(param)
