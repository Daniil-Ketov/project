"""practice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from practice.views import HomeView
from practice.views import LogoutView
from practice.views import RegisterView
from practice.views import ProfileView
from practice.views import EditProfileView
from practice.views import PostCommentView
from practice.views import DialogsView
from practice.views import CreateDialogView
from practice.views import MessagesView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(r'', HomeView.as_view(), name="home"),
    path(r'admin/', admin.site.urls),
    path(r'login/', LoginView.as_view(), name="login"),
    path(r'logout/', LogoutView.as_view(), name="logout"),
    path(r'register/', RegisterView.as_view(), name="register"),
    path(r'profile/', ProfileView.as_view(), name="profile"),
    path(r'accounts/profile/', ProfileView.as_view()),
    path(r'profile/edit/', EditProfileView.as_view(), name="edit_profile"),
    path(r'post-comment/', PostCommentView.as_view()),
    path(r'dialogs/', login_required(DialogsView.as_view()), name='dialogs'),
    path(r'dialogs/create/(?P<user_id>\d+)/', login_required(CreateDialogView.as_view()), name='create_dialog'),
    path('dialogs/(?P<chat_id>\d+)/$', login_required(MessagesView.as_view()), name='messages'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

