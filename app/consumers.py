import json
from channels.generic.websocket import JsonWebsocketConsumer

# view와 비슷한 역할
# 매핑된 url로 요청이 오면 해당 Consumer의 인스턴스를 생성
# 생성된 인스턴스는 웹소켓 연결이 유지되는 동안 계속해서 살아있음
# receive는 말 그대로 메세지를 받았을 때 처리


class LiveblogConsumer(JsonWebsocketConsumer):
    # 메세지를 받을 그룹명을 명시. 지금은 liveblog라고 고정되어있으니 명시 가능
    groups = ["liveblog"]
    # 그룹을 통해 받은 메세지를 그대로 클라이언트에게 전달(self.send(message))
    # 메세지의 type 값과 같은 이름의 메서드 호출(단, .은 _로 변환됨
    # ex) type이 liveblog.post.created라면 liveblog_post_created 이름을 가진 메소드가 호출됨

    # 인자는 event_dict 하나만 들어오게 되는데 저게 group_send 할 때 보냈던 dictionary임

    def liveblog_post_created(self, event_dict):
        print(event_dict)
        self.send_json(event_dict)

    def liveblog_post_updated(self, event_dict):
        print(event_dict)
        self.send_json(event_dict)

    def liveblog_post_deleted(self, event_dict):
        print(event_dict)
        self.send_json(event_dict)


class EchoConsumer(JsonWebsocketConsumer):
    def receive_json(self, content, **kwargs):
        print("수신 : ", content)

        self.send_json(
            {
                "content": content["content"],
                "user": content["user"],
            }
        )
