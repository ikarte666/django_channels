from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from chat.forms import RoomForm
from chat.models import Room


def index(request):
    rooms = Room.objects.all()
    return render(
        request,
        "chat/index.html",
        {
            "rooms": rooms,
        },
    )


@login_required
def room_new(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            created_room = form.save(commit=False)
            created_room.owner = request.user
            created_room.save()
            return redirect("chat:room_chat", created_room.pk)
    else:
        form = RoomForm()

    return render(
        request,
        "chat/room_form.html",
        {
            "form": form,
        },
    )


@login_required
def room_chat(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    return render(request, "chat/room_chat.html", {"room": room})


@login_required
def room_delete(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    if room.owner != request.user:
        messages.error(request, "권한이 없습니다.")
        return redirect("chat:index")

    if request.method == "POST":
        room.delete()
        messages.success(request, "채팅방 삭제 완료")
        return redirect("chat:index")

    return render(
        request,
        "chat/room_confirm_delete.html",
        {
            "room": room,
        },
    )
