from rest_framework import serializers
from todo.models import Todo

#ModelSerializer provides an API to create serializers from your models
class TodoSerializer(serializers.ModelSerializer): 
    created = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()

class Meta:
    model = Todo
    fields = ['id','title','memo','created','completed']