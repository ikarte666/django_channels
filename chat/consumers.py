from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from chat.models import Room


# 채널레이어 그룹명은 정규표현식으로 검사
# 문자열, 100자 미만, 알파벳 대소문자, 숫자, 하이픈, 언더바, 마침표만 허용
class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_pk = -1
        self.group_name = ""

    def connect(self):
        self.room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
        self.group_name = Room.make_chat_group_name(room_pk=self.room_pk)

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )

    # 클라이언트에서 요청이 올 경우 동작
    # 이후 내부 로직에 따라 group_send를 호출하여 채널 레이어로 데이터를 보냄
    # 이후 채널 레이어에서 그룹에 맞게 Consumer를 찾아 데이터 전송
    def receive_json(self, content, **kwargs):
        _type = content["type"]

        if _type == "chat.message":
            message = content["message"]
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {"type": "chat.message", "message": message}
            )
        else:
            print(f"Invalid message type : {_type}")

    # group_send에서 같은 그룹으로 보낸 메세지를 여기서 받음
    # 채널 레이어에서 데이터 타입에 맞게 자동 호출함
    # 여기서 사용한 send_json으로 클라이언트에게 데이터를 보낼 수 있는것
    def chat_message(self, message_dict):
        self.send_json({"type": "chat.message", "message": message_dict["message"]})
