from django.db import models

# Create your models here.
class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)
    email = models.CharField(max_length=100)
    title = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.id) + "/" + str(self.name) + "/" + str(self.surname) + "/" + \
            str(self.email) + "/" + str(self.title)

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    adminEmail = models.CharField(max_length=100, blank=True)
    lecturer = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id) + "/" + str(self.topic) + "/" + str(self.subject) + "/" + \
            str(self.adminEmail) + "/" + str(self.lecturer)

class Student(models.Model):
    index = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)
    email = models.CharField(max_length=100)
    teamId = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    isTeamAdmin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.index) + "/" + str(self.name) + "/" + str(self.surname) + "/" + \
            str(self.email) + "/" + str(self.teamId) + "/" + str(self.isTeamAdmin)

class Message(models.Model):
    NORMAL = '0'
    INVITATION = '1'
    MSG_TYPES_CHOICES = [
        (NORMAL, 'Normal'),
        (INVITATION, 'Invitation')
        ]
    id = models.AutoField(primary_key=True)
    fromUser = models.CharField(max_length=60)
    toUser = models.CharField(max_length=60)
    subject = models.CharField(max_length=150, blank=True)
    msgLines = models.CharField(max_length=500, blank=True)
    type = models.CharField(max_length=20,
                            choices=MSG_TYPES_CHOICES,
                            default=NORMAL)
    isRead = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + "/" + \
                str(self.fromUser) + "/" + \
                str(self.toUser) + "/" + \
                str(self.subject) + "/" + \
                str(self.msgLines) + "/" + \
                str(self.type) + "/" + \
                str(self.isRead)

class User(models.Model):
    STUDENT = '0'
    LECTURER = '1'
    ACCOUNT_TYPES_CHOICES = [
        (STUDENT, 'Student'),
        (LECTURER, 'Lecturer')
        ]
    email = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=20)
    accountType = models.CharField(max_length=20,
                                   choices=ACCOUNT_TYPES_CHOICES,
                                   default=STUDENT)