from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import TodoList, OperationLog
from .serializers import TodoListSerializer, OperationLogSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404
import pandas as pd
from datetime import datetime

# Create your views here.
def tasks(request):
    return HttpResponse("HELLO")

@api_view(['GET'])
def get_todo_list(request):
    todo_items = TodoList.objects.all()
    serializer = TodoListSerializer(todo_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_todo_item(request, pk):
    todo_item = get_object_or_404(TodoList, pk=pk)
    serializer = TodoListSerializer(todo_item)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_todo_item(request):
    if request.method == 'POST':
        serializer = TodoListSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new TodoList item
            todo_item = serializer.save()

            # Create the log entry for the new item
            OperationLog.objects.create(
                action='CREATED',
                description='New Todo item created',
                todo_instance=todo_item
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_log_details(request, pk):
    try:
        log_instance = OperationLog.objects.filter(todo_instance=pk)
    except OperationLog.DoesNotExist:
        return Response({"error": "Log entry not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = OperationLogSerializer(log_instance,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def map_value(key, value):
    value_mapping = {
        'status': {
            '1': 'To-Do',
            '2': 'In-Progress',
            '3': 'Completed',
        },
        'priority': {
            '1': 'High',
            '2': 'Medium',
            '3': 'Low',
        }
    }
    return value_mapping.get(key, {}).get(value, value)

@api_view(['PATCH'])
def update_todo_item(request):
    pk = request.data.get('pk')
    try:
        todo_item = TodoList.objects.get(pk=pk)
    except TodoList.DoesNotExist:
        return Response({"error": "Todo item not found."}, status=status.HTTP_404_NOT_FOUND)

    old_todo_item = TodoListSerializer(todo_item).data.copy()

    serializer = TodoListSerializer(todo_item, data=request.data, partial=True)
    if serializer.is_valid():
        # new_title = serializer.validated_data.get('title')
        serializer.save(updated_at=timezone.now())

        # Create the log entry for the update
        print(old_todo_item)
        print(serializer.validated_data)
        log_changes = {}
        for key, value in serializer.validated_data.items():
            if old_todo_item[key] != value:
                print(key)
                oldvalue=str(old_todo_item[key])
                newvalue=str(value)
                
                if key in ('status', 'priority'):
                    oldvalue = map_value(key, oldvalue)
                    newvalue = map_value(key, newvalue)

                log_changes[key] = str(key).upper() + " changed from \'"+ oldvalue + "\' to \'" + newvalue + "\'"
                    

        if len(log_changes)>0:
            print("here")
            OperationLog.objects.create(
                action='UPDATED',
                description='Todo item updated',
                changes=log_changes,
                todo_instance=todo_item
            )

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_todo_item(request, pk):
    try:
        todo_item = get_object_or_404(TodoList, pk=pk)
        todo_item.delete()
        return Response({"message": "Todo item deleted successfully."}, status=status.HTTP_200_OK)
    except TodoList.DoesNotExist:
        return Response({"error": "Todo item not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


