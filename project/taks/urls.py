from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import UserListView


urlpatterns = [
    path('addtask/', views.add_task, name='add_task'),
    path('listtask/', views.list_task, name='list_task'),
    path('edittask/', views.edit_task, name='edit_task'),
    path('deletetask/', views.delete_task, name='delete_task'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', UserListView.as_view(), name='user-list'),
]