from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from chat.models import Room


# 채널레이어 그룹명은 정규표현식으로 검사
# str, 100자 미만, 알파벳 대소문자, 숫자, 하이픈, 언더바, 마침표만 허용
class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_pk = -1
        self.group_name = ""

    def connect(self):
        # current user
        user = self.scope["user"]
        if not user.is_authenticated:
            self.close()
        else:
            # url captured value
            self.room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
            self.group_name = Room.make_chat_group_name(room_pk=self.room_pk)

            async_to_sync(self.channel_layer.group_add)(
                self.group_name, self.channel_name
            )

            self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )

    # 클라이언트 요청 처리
    # group_send를 호출하여 채널 레이어로 데이터 전송
    # 채널 레이어에서 그룹에 맞게 Consumer instance로 데이터 전송
    def receive_json(self, content, **kwargs):
        user = self.scope["user"]
        _type = content["type"]

        if _type == "chat.message":
            sender = user.username
            message = content["message"]
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "chat.message",
                    "message": message,
                    "sender": sender,
                },
            )
        else:
            print(f"Invalid message type : {_type}")

    # 채널 레이어에서 보낸 메세지 수신
    # type에 따라 맞는 이름을 자동으로 호출
    # send_json으로 클라이언트에게 데이터 전송
    def chat_message(self, message_dict):
        self.send_json(
            {
                "type": "chat.message",
                "message": message_dict["message"],
                "sender": message_dict["sender"],
            }
        )

    def chat_room_deleted(self, message_dict):
        custom_code = 4000
        self.close(code=custom_code)
