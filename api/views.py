from rest_framework import generics
from .serializers import TodoSerializer
from todo.models import Todo

# ListAPIView is a built-in generic class which creates a
# read-only endpoint for model instances
class TodoListCreate(generics.ListCreateAPIView):
# ListAPIView requires two attributes, serializer_class and queryset.
    serializer_class = TodoSerializer

    def get_queryset(self):
        user = self.request.user # get the todos of this.user from the request
        return Todo.objects.filter(user=user).order_by('-created')

    def perform_create(self, serializer):
        #serializer holds a django model
        serializer.save(user=self.request.user) # set the user of the todo as the request’s user before creation in the database