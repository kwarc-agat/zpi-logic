from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'teachers', views.TeacherViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'students', views.StudentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    
    path('auth', views.confirmPassword),

    path('mailbox/markReaded', views.markMessageAsRead, name='mailboxMarkReaded'),
    path('mailbox/accept', views.acceptInvitation, name='mailboxAccept'),
    path('mailbox', views.manageMessages, name='mailbox'),
    
    path('students/leaveTeam', views.leaveTeam, name='studentsLeaveTeam'),
    path('students/<str:inputEmail>/', views.getStudent, name='getStudent'),
    path('students', views.getStudents, name='students'),
    
    path('teachers', views.getTeachers, name='teachers'),
    path('teachers/<str:inputEmail>/', views.getTeacherByEmail, name='getTeacher'),

    path('teams/addLecturer', views.addTeamLecturer, name='teamsAddLecturer'),
    path('teams', views.getAllTeams, name='teams'),
    path('teams/<str:param>/', views.manageTeam, name='teamsManage'),

    #path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'), name='teachers'),
    
]
