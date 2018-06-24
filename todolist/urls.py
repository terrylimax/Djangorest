from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TaskCreateView, TaskDetailsView, TasklistCreateView, TasklistDetailsView
from .views import TagCreateView, TagDetailsView, CreateUserView, UserDetailsView, UserListView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = {
    url(r'^todolists/$', TaskCreateView.as_view(), name="create"),
    url(r'^todolists/(?P<pk>[0-9]+)/$', TaskDetailsView.as_view(), name="detail"),
}

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns = {
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^todolists/$', TasklistCreateView.as_view(), name="lists"),
    url(r'^todolists/(?P<pk>[0-9]+)/$', TasklistDetailsView.as_view(), name="list-detail"),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/$', TaskCreateView.as_view(), name="tasks"),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', TaskDetailsView.as_view(), name="task-detail"),
    url(r'^todolists/tags/$', TagCreateView.as_view(), name='tags'),
    url(r'^todolists/tags/(?P<pk>[0-9]+)/$', TagDetailsView.as_view(), name="tag-detail"),
    url(r'^users/$', UserListView.as_view(), name="users"),
    url(r'^users/register/$', CreateUserView.as_view(), name="create-user"),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetailsView.as_view(), name="user-detail"),
    url(r'^get-token/', obtain_auth_token),
}

urlpatterns = format_suffix_patterns(urlpatterns)