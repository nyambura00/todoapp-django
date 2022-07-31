from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoToggleCompleteSerializer
from todo.models import Todo

from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# ListAPIView is a built-in generic class which creates a
# read-only endpoint for model instances
class TodoListCreate(generics.ListCreateAPIView):
# ListAPIView requires two attributes, serializer_class and queryset.
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    # IsAuthenticatedOrReadOnly class - full auth/read-only to unauthenticated users

    def get_queryset(self):
        user = self.request.user # get the todos of this.user from the request
        return Todo.objects.filter(user=user).order_by('-created')

    def perform_create(self, serializer):
        #serializer holds a django model
        serializer.save(user=self.request.user) # set the user of the todo as the request’s user before creation in the database

class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # user can only update, delete own posts
        return Todo.objects.filter(user=user)

class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self,serializer):
        serializer.instance.completed=not(serializer.instance.completed)
        serializer.save()

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request) # returning a dictionary of data
            user = User.objects.create_user(
                        username=data['username'],
                        password=data['password'])
            user.save()

            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=201)

        except IntegrityError:
            return JsonResponse(
                {'error':'username exists. choose another username'},
                status=400)