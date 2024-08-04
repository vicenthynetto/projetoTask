from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import *
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_task(request, format=None):
    result = []
    data = request.data
    try:
        title = data.get('title')
        description = data.get('description')
        due_date = data.get('due_date')

        if not isinstance(title, str) or not isinstance(description, str):
            return Response(
                {"detail": "Title and description must be strings."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            return Response(
                {"detail": "Due date must be a valid date in the format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        if not title or not description or not due_date:
            return Response(
                {"detail": "All fields (title, description, due_date) are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cria a nova task
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
        )
        task.save()

        result = f"Task {task.title} has been successfully registered!"
        result = {
            "result": result,
            "id": task.pk,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        }
        return Response(result)
    except Exception as e:
        re = {
            "detail": f"Erro: {str(e)}"
        }
        return Response(re, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_task(request, format=None):
    result = []
    task_id = request.GET.get('id')
    
    try:
        if task_id:
            tasks = Task.objects.filter(status=True, id=task_id)
            if not tasks:
                return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            tasks = Task.objects.filter(status=True).order_by('-created_at')
        
        for tsk in tasks:
            result.append({
                "id":tsk.pk,
                "title": tsk.title,
                "description": tsk.description,
                "due_date": tsk.due_date,
                "creatad_at": tsk.created_at,
                "updated_at": tsk.updated_at,
            })
        
        return Response(result, status=status.HTTP_200_OK)
    
    except Exception as e:
        re = {
            "detail": f"Erro: {str(e)}"
        }
        return Response(re, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_task(request, format=None):
    task_id = request.GET.get('id')
    
    try:
        if task_id:
            task = Task.objects.get(id=task_id, status=True)

            fields_to_update = {
                "title": request.data.get('title', task.title),
                "description": request.data.get('description', task.description),
                "due_date": request.data.get('due_date', task.due_date),
            }
            with transaction.atomic():
                for field, value in fields_to_update.items():
                    setattr(task, field, value)
                
                task.updated_at = timezone.now()

                task.save()
            
            result = {
                "result": f"Task {task.title} has been successfully edited!",
                "id": task.pk,
                "title": task.title,
                "description": task.description,
                "due_date": task.due_date,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Task.DoesNotExist:
        return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        re = {
            "detail": f"Erro: {str(e)}"
        }
        return Response(re, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, format=None):
    task_id = request.GET.get('id')
    try:
        if task_id:
            task = Task.objects.get(id=task_id, status=True)
        
            task.status = False
            task.updated_at = timezone.now()
            task.save()

            return Response({"detail": "Task deleted successfully."}, status=status.HTTP_200_OK)
        
        return Response({"detail": "Task ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        re = {
            "detail": f"Erro: {str(e)}"
        }
        return Response(re, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)