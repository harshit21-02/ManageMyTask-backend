from django.db import models

# Create your models here.

class OperationLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    description = models.TextField()
    changes = models.JSONField(null=True, blank=True)
    todo_instance = models.ForeignKey('TodoList', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timestamp} - {self.action}"

class TodoList(models.Model):

    STATUS_CHOICES = (
    (1, 'To-Do'),
    (2, 'In-Progress'),
    (3, 'Completed'),
    )

    PRIORITY_CHOICES = (
    (1, 'High'),
    (2, 'Medium'),
    (3, 'Low'),
    )

    id = models.AutoField('id',primary_key=True)
    title=models.CharField('title',blank=False,max_length=255)
    description=models.TextField('description',blank=True, null=True)
    due_date=models.DateField('due_date',blank=False)
    priority=models.IntegerField('priority',choices=PRIORITY_CHOICES,default=3)
    status=models.IntegerField('status',choices=STATUS_CHOICES,default=3)
    created_at = models.DateTimeField('created_at',auto_now_add= True)
    updated_at= models.DateTimeField('updated_at',auto_now= True)

    def __str__(self):
        return self.title

