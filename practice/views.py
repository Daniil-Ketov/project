from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from practice.forms import RegisterForm
from practice.forms import ProfileForm
from practice.forms import PostForm
from practice.forms import MessageForm
from practice.models import Profile
from practice.models import Post
from practice.models import Comment
from practice.models import Friends
from practice.models import FriendRequest
from practice.models import Chat

class HomeView(TemplateView):
    template_name = "home.html"
    timeline_template_name = "timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect(reverse("home"))
        context = {
            'posts': Post.objects.all()
        }
        return render(request, self.timeline_template_name, context)


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                self.create_new_user(form)
                messages.success(request, u"Вы успешно зарегистрировались!")
                return redirect(reverse("login"))

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def create_new_user(self, form):
        email = None
        if 'email' in form.cleaned_data:
            email = form.cleaned_data['email']
        User.objects.create_user(form.cleaned_data['username'], email, form.cleaned_data['password'],
                                 first_name=form.cleaned_data['first_name'],
                                 last_name=form.cleaned_data['last_name'])


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class ProfileView(TemplateView):
    template_name = "registration/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user=request.user).exists():
            return redirect(reverse("edit_profile"))
        context = {
            'selected_user': request.user
        }
        return render(request, self.template_name, context)


class EditProfileView(TemplateView):
    template_name = "registration/edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.get_profile(request.user))
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                messages.success(request, u"Профиль успешно обновлен!")
                return redirect(reverse("profile"))
        return render(request, self.template_name, {'form': form})

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None
        

class PostCommentView(View):
    def dispatch(self, request, *args, **kwargs):
        post_id = request.GET.get("post_id")
        comment = request.GET.get("comment")
        if comment and post_id:
            post = Post.objects.get(pk=post_id)
            comment = Comment(text=comment, post=post, author=request.user)
            comment.save()
            return render(request, "blocks/comment.html", {'comment': comment})
        return HttpResponse(status=500, content="")
    

def friend_request(request, pk):
    sender = request.user
    recipient = User.objects.get(id=pk)
    model = FriendRequest.objects.get_or_create(sender=request.user, receivers=recipient)
    return redirect('/Display')


def delete_request(request, operation, pk):
    client1 = User.objects.get(id=pk)
    print(client1)
    if operation == 'Sender_deleting':
        model1 = FriendRequest.objects.get(sender=request.user, receivers=client1)
        model1.delete()
    elif operation == 'Receiver_deleting':
        model2 = FriendRequest.objects.get(sender=client1, receivers=request.user)
        model2.delete()
        return redirect('/formation')

    return redirect('/Display')


def add_or_remove_friend(request, operation, pk):
    new_friend = User.objects.get(id=pk)
    if operation == 'add':
        fq = FriendRequest.objects.get(sender=new_friend, receivers=request.user)
        Friends.make_friend(request.user, new_friend)
        Friends.make_friend(new_friend, request.user)
        fq.delete()
    elif operation == 'remove':
        Friends.lose_friend(request.user, new_friend)
        Friends.lose_friend(new_friend, request.user)

    
    return redirect('form4')

class DialogsView(View):
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request, 'chat/dialogs.html', {'user_profile': request.user, 'chats': chats})


class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None
 
        return render(
            request,
            'chat/messages.html',
            {
                'user_profile': request.user,
                'chat': chat,
                'form': MessageForm()
            }
        )
 
    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('users:messages', kwargs={'chat_id': chat_id}))


class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('users:messages', kwargs={'chat_id': chat.id}))


