from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserForm, SignUpForm
from room.models import *


def frontpage(request):
    return render(request, "core/frontpage.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()

    return render(request, "core/signup.html", {"form": form})


@login_required
def users(request):
    users = ChatUser.objects.all().exclude(id=request.user.id)
    return render(request, 'core/users.html', {'users': users})


def hash_names(user1, user2):
    # "Hashes" the names of 2 users of a one-on-one conversation
    # to create a unique room name only accessible to user1 or user2
    names = [str(user1.id), str(user2.id)]
    names.sort()
    names = [name + str((len(name)) + 69 * 6 * 9 - 420) for name in names]
    names = [name[::-1] for name in names]
    names = "".join(names)
    return names


@login_required
def direct_messages(request, pk):
    self_user = request.user
    to_user = ChatUser.objects.get(id=pk)
    if self_user.username != to_user.username:
        room, _ = Room.objects.get_or_create(name=hash_names(self_user, to_user), private=True)
        self_messages = Message.objects.filter(user=self_user, room=room)
        to_messages = Message.objects.filter(user=to_user, room=room)
        messages = self_messages | to_messages
        sorted_messages = messages.distinct().order_by('date_added')
        context = {
            'room': room,
            'to_user': to_user,
            'self_user': self_user,
            'sorted_messages': sorted_messages
        }
        return render(request, 'core/direct_message.html', context)

    else:
        return redirect('frontpage')


@login_required()
def show_profile(request):
    chatuser = request.user.chatuser
    user_form = UserForm(instance=chatuser)
    context = {"user": chatuser, 'user_form': user_form}

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=chatuser)
        if form.is_valid():
            form.save()

    return render(request, 'core/profile.html', context)
