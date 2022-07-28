from rest_framework import generics
from .serializers import TodoSerializer
from todo.models import Todo

# ListAPIView is a built-in generic class which creates a
# read-only endpoint for model instances
class TodoList(generics.ListAPIView):
# ListAPIView requires two attributes, serializer_class and queryset.
    serializer_class = TodoSerializer

    def get_queryset(self):
        user = self.request.user # get the todos of user from the request
        return Todo.objects.filter(user=user).order_by('-created')