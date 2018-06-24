from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .permissions import IsOwner
from .serializers import TaskSerializer, TasklistSerializer, TagSerializer, UserSerializer
from .models import Task, Tasklist, Tag
from rest_framework import permissions
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Q


class TasklistCreateView(generics.ListCreateAPIView):
    queryset = Tasklist.objects.all()
    serializer_class = TasklistSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def filter_queryset(self, queryset):
        queryset = queryset.filter(Q(owner=self.request.user)|Q(friend=self.request.user))
        return queryset


class TasklistDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasklist.objects.all()
    serializer_class = TasklistSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def filter_queryset(self, queryset):
        queryset = queryset.filter(Q(owner=self.request.user)|Q(friend=self.request.user))
        return queryset


class TagCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TagDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TaskCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Task.objects.all()
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None:
            queryset = queryset.filter(tasklist_id=list_id)
        return queryset

    def perform_create(self, serializer):
        list_id = self.kwargs.get('list_id', None)
        try:
            tasklist = Tasklist.objects.get(pk=list_id)
        except Tasklist.DoesNotExist:
            raise NotFound()
        serializer.save(tasklist=tasklist)

    def post(self, request, list_id, *args, **kwargs):
        print(type(request.data), request.data)
        tasklist = Tasklist.objects.get(pk=list_id)
        tag_names = request.data.get('tags', []).split()
        data = request.data.copy()
        data.pop('tags')
        tags_set = []
        for tag_name in tag_names:
            tags_set.append(Tag.objects.get_or_create(name=tag_name)[0])
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(tasklist=tasklist)
        for tag in tags_set:
            serializer.instance.tags.add(tag)
        return Response(serializer.data)


class TaskDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Task.objects.all()
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None:
            queryset = queryset.filter(tasklist_id=list_id)
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        tag_names = request.data.get('tags', []).split()
        data = request.data.copy()
        data.pop('tags')
        tags_set = []
        for tag_name in tag_names:
            tags_set.append(Tag.objects.get_or_create(name=tag_name)[0])
        serializer = self.serializer_class(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        for tag in tags_set:
            serializer.instance.tags.add(tag)
        return Response(serializer.data)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    '''def filter_queryset(self, queryset):
        queryset = queryset.filter(username=self.request.user)
        return queryset'''


class CreateUserView(generics.CreateAPIView):
    # model = get_user_model()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated():
            raise PermissionDenied()
        serializer.save()


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs.get('pk'))