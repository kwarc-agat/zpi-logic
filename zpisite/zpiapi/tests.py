from django.test import TestCase, Client
from django.urls import reverse
from .models import *
import json

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        print("In method", self._testMethodName)

        self.userNoTeam = User.objects.create(
            email="245001@gmail.com",
            password="1234")


        self.studentNoTeam = Student.objects.create(
            index="245001",
            name="Nowak",
            surname="Jan",
            email="245001@gmail.com",
            teamId=None,
            isTeamAdmin=False)

        self.studentAdmin = Student.objects.create(
            index="245002",
            name="Nowak",
            surname="Jan",
            email="245002@gmail.com",
            teamId=None,
            isTeamAdmin=False)

        self.team = Team.objects.create(
            adminEmail=self.studentAdmin.email)

        self.studentWithTeam = Student.objects.create(
            index="245003",
            name="Nowak",
            surname="Jan",
            email="245003@gmail.com",
            teamId=self.team,
            isTeamAdmin=False)

        self.studentAdmin.teamId = self.team
        self.studentAdmin.isTeamAdmin = True

        self.teacher = Teacher.objects.create(
            name="Kowalski",
            surname="Adam",
            email="akowal@gmail.com",
            title="dr")

        self.invitation = Message.objects.create(
            fromUser="245002@gmail.com",
            toUser="245001@gmail.com",
            subject="",
            msgLines="",
            type='1',
            isRead=False)

        
        self.msgToDelete = Message.objects.create(
            fromUser="245002@gmail.com",
            toUser="245001@gmail.com",
            subject="",
            msgLines="",
            type='0',
            isRead=False)

    def test_getAllTeachers(self):
        
        response = self.client.get(reverse('teachers'))
        self.assertEquals(response.status_code, 200)
        
    def test_getAllTeams(self):
        
        response = self.client.get(reverse('teams'))
        self.assertEquals(response.status_code, 200)

    def test_getAllStudents(self):
        
        response = self.client.get(reverse('students'))
        self.assertEquals(response.status_code, 200)

    def test_get_messages(self):
        
        response = self.client.get('/mailbox?email={}'.format(self.studentNoTeam.email))
        self.assertEquals(response.status_code, 200)

    def test_confirmPassword(self):
        response = self.client.get('/auth?email={email}&password={password}'
                                   .format(email=self.userNoTeam.email,
                                           password=self.userNoTeam.password))
        self.assertEquals(response.status_code, 200)

    def test_markMessageAsRead(self):
        response = self.client.post('/mailbox/markReaded?email={email}&messageId={messageId}'
                                        .format(email=self.invitation.toUser, 
                                                messageId=self.invitation.id))
        self.invitation.refresh_from_db()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.invitation.isRead, True)

    def test_acceptInvitation(self):
        response = self.client.post('/mailbox/accept?email={email}&messageId={messageId}'
                                   .format(email=self.studentNoTeam.email,
                                           messageId=self.invitation.id))

        self.studentNoTeam.refresh_from_db()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.studentNoTeam.teamId, self.team)

    def test_acceptInvitation_hasTeam(self):
        response = self.client.get('/mailbox/accept?email={email}&messageId={messageId}'
                                   .format(email=self.studentWithTeam.email,
                                           messageId=self.invitation.id))

        self.studentWithTeam.refresh_from_db()
        self.assertEquals(response.status_code, 405)

    def test_deleteMessage(self):
        response = self.client.delete('/mailbox?email={email}&messageId={messageId}'
                                        .format(email=self.invitation.toUser, 
                                                messageId=self.msgToDelete.id))
        self.assertEquals(response.status_code, 200)

    def test_leaveTeam(self):
        response = self.client.post('/students/leaveTeam?email={email}'
                                   .format(email=self.studentWithTeam.email))

        self.studentWithTeam.refresh_from_db()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.studentWithTeam.teamId, None)
        

    def test_getStudent(self):
        response = self.client.get('/students/{}/'.format(self.studentNoTeam.email))
        self.assertEquals(response.status_code, 200)

    def test_addTeamLecturer(self):
        response = self.client.post('/teams/addLecturer?teamId={teamId}&email={email}'
                                   .format(teamId=self.team.id,
                                           email=self.teacher.email))

        self.team.refresh_from_db()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.team.lecturer, self.teacher)

    def test_removeTeam(self):
        response = self.client.delete('/teams/{teamId}/'
                                        .format(teamId=self.team.id))
        self.assertEquals(response.status_code, 200)

    def test_getTeam(self):
        response = self.client.get('/teams/{}/'.format(self.studentWithTeam.email))
        self.assertEquals(response.status_code, 200)

    def test_createTeam(self):
        response = self.client.put('/teams/{email}/'
                                        .format(email=self.studentNoTeam.email))
        self.assertEquals(response.status_code, 200)

        self.studentNoTeam.refresh_from_db()
        self.assertEquals(self.studentNoTeam.isTeamAdmin, True)
        self.assertNotEquals(self.studentNoTeam.teamId, None)


    def test_createTeam_studentWithTeam(self):
        response = self.client.put('/teams/{email}/'
                                        .format(email=self.studentWithTeam.email))
        self.assertEquals(response.status_code, 405)