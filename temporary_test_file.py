import asyncio
import os
import django
from channels.layers import get_channel_layer

os.environ["DJANGO_SETTINGS_MODULE"] = "channelss.settings"


django.setup()


async def main():
    # 채널 레이어는 내부적으로 직렬화 실행
    channel_layer = get_channel_layer()
    message_dict = {"content": "world"}

    await channel_layer.send("hello", message_dict)

    response_dict = await channel_layer.receive("hello")
    is_equal = message_dict == response_dict
    print(is_equal)


asyncio.run(main())
