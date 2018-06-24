from rest_framework import serializers
from .models import Task
from .models import Tasklist
from .models import Tag, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import hashlib, random, datetime
from django.shortcuts import get_object_or_404


# UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'id', 'password', )
        write_only_fields = ('password', )
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'],
                                   first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                                   is_active=0)
        user.set_password(validated_data['password'])
        user.save()

        salt = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
        # print('SAAAAAAAAAAALT', salt)
        salt_bytes = salt.encode('utf-8')
        email_bytes = user.email.encode('utf-8')
        activation_key = hashlib.sha1(salt_bytes + email_bytes).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        # return user
        new_profile = UserProfile(user=user, activation_key=activation_key,
                                  key_expires=key_expires)
        new_profile.save()
        # Send email with activation key
        email_subject = 'Подтверждение регистрации'
        email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
        48hours http://127.0.0.1:8080/activate/%s/" % (user.username, activation_key)
        # print(email_body)
        send_mail(email_subject, email_body, 'dimon191198@gmail.com',
                  [user.email], fail_silently=False)

        def save(self, commit=True):
            # user = super(RegistrationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.is_active = 0  # not active until he opens activation link
            user.save()
        user.is_active = 1
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'tasks',)
        read_only_fields = ('tasks',)


class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True,
                                        queryset=Tag.objects.all(),
                                        slug_field='name')

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'completed', 'date_created',
                  'date_modified', 'due_date', 'priority', 'tags')
        read_only_fields = ('date_created', 'date_modified',)


class TasklistSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    owner = serializers.StringRelatedField(source='owner.username', read_only=True)

    class Meta:
        model = Tasklist
        fields = ('id', 'name', 'owner', 'tasks', 'friend',)

        read_only_fields = ('tasks',)
