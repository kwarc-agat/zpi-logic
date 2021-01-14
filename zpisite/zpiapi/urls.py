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

    path('mailbox/markReaded', views.markMessageAsRead),
    path('mailbox/accept', views.acceptInvitation),
    path('mailbox', views.manageMessages),
    
    path('students/leaveTeam', views.leaveTeam),
    path('students/<str:inputEmail>/', views.getStudent),
    path('students', views.getStudents),
    
    path('teachers', views.getTeachers),
    
    path('teams/addLecturer', views.addTeamLecturer),
    path('teams/leaveTeam', views.leaveTeam),
    path('teams/removeTeam', views.removeTeam),
    path('teams', views.getAllTeams),
    path('teams/<str:id>/', views.manageTeam),

    #path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
