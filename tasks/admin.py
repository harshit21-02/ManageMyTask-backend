from django.contrib import admin

# Register your models here.
from .models import TodoList, OperationLog
admin.site.register(TodoList)
admin.site.register(OperationLog)