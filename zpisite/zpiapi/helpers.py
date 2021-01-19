from .models import *
from .constans import *


def getTeacherByEmail(teacher_email):
    try:
        teacher = Teacher.objects.get(email=teacher_email)
        return {"id": teacher.id,
                "name": teacher.name,
                "surname": teacher.surname,
                "email": teacher.email,
                "title": teacher.title}
    except Teacher.DoesNotExist:
        return {"message": MessageInfo.NOT_EXISTS_TEACHER}


def getStudentsByTeam(commonTeam):
    one_team_students = Student.objects.filter(teamId=commonTeam)
    students_list = []
    for student in one_team_students:
        students_list.append(parseStudentObjectNoTeamId(student))
    return students_list


def getTeamById(teamId):
    try:
        team = Team.objects.get(id=teamId)
        if team.lecturer is not None:
            lecturer = getTeacherByEmail(team.lecturer.email)
        else:
            lecturer = None
        return {
            "id": team.id,
            "topic": team.topic,
            "subject": team.subject,
            "members": getStudentsByTeam(team),
            "adminEmail": team.adminEmail,
            "lecturer": lecturer
        }
    except Team.DoesNotExist:
        return {"message": MessageInfo.NOT_EXISTS_TEAM}


def getTeamByUserEmail(userEmail):
    try:
        student = Student.objects.get(email=userEmail)
        if student.teamId is not None:
            team = student.teamId
            if team.lecturer is not None:
                lecturer = getTeacherByEmail(team.lecturer.email)
            else:
                lecturer = None
            return {
                "id": team.id,
                "topic": team.topic,
                "subject": team.subject,
                "members": getStudentsByTeam(team),
                "adminEmail": team.adminEmail,
                "lecturer": lecturer
            }
        else:
            return {"message": MessageInfo.HAS_NO_TEAM}
    except Team.DoesNotExist:
        return {"message": MessageInfo.NOT_EXISTS_TEAM}


def getMessageById(msgId):
    try:
        msg = Message.objects.get(id=msgId)
        return {
            "id": msg.id,
            "from": msg.fromUser,
            "to": msg.toUser,
            "subject": msg.subject,
            "msgLines": [msg.msgLines],
            "type": int(msg.type),
            "isRead": msg.isRead
        }
    except Message.DoesNotExist:
        return {"message": MessageInfo.NOT_EXISTS_MESSAGE}


def parseStudentObject(student):
    if student.teamId is not None:
        teamId = student.teamId.id
    else:
        teamId = None
    return {"name": student.name,
            "surname": student.surname,
            "email": student.email,
            "index": student.index,
            "teamId": teamId,
            "isTeamAdmin": student.isTeamAdmin}


def parseStudentObjectNoTeamId(student):
    return {"name": student.name,
            "surname": student.surname,
            "email": student.email,
            "index": student.index,
            "isTeamAdmin": student.isTeamAdmin}
