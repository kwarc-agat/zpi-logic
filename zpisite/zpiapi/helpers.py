from .models import *

def getTeacherById(teacherId):
    teacher = Teacher.objects.get(id=teacherId)
    return {"id": teacher.id,
            "name": teacher.name,
            "surname": teacher.surname,
            "email": teacher.email,
            "title": teacher.title}

def getStudentsByTeam(commonTeam):
    one_team_students = Student.objects.filter(teamId=commonTeam)
    students_list = []
    for student in one_team_students:
        students_list.append(parseStudentObjectNoTeamId(student))
    return students_list

def getTeamById(teamId):
    team = Team.objects.get(id=teamId)
    if team.lecturer is not None:
        lecturer = getTeacherById(team.lecturer.id)
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
def getMessageById(msgId):
    msg = Message.objects.get(id=msgId)
    return{
        "id": msg.id,
        "from": msg.fromUser,
        "to": msg.toUser,
        "subject": msg.subject,
        "msgLines": [msg.msgLines],
        "type": int(msg.type),
        "isRead": msg.isRead
        }

def parseStudentObject(student):
    if student.teamId is not None:
        teamId = student.teamId.id
    else: teamId = None
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
