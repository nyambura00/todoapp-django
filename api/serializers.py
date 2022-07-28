from rest_framework import serializers
from todo.models import Todo

#ModelSerializer provides an API to create serializers from your models
class TodoSerializer(serializers.ModelSerializer): 
    created = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['id','title','memo','created','completed']

class TodoToggleCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id'] # why need to show id?
        read_only_fields = ['title','memo','created','completed']