from django.db import models
from django.db.models.signals import post_save, post_delete
from django.urls import reverse

from app.mixins import ChannelLayerGroupSendMixin


class Post(ChannelLayerGroupSendMixin, models.Model):
    CHANNEL_LAYER_GROUP_NAME = "liveblog"
    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        ordering = ["-id"]


def post__on_post_save(instance: Post, created: bool, **kwargs):
    if created:
        message_type = "liveblog.post.created"
    else:
        message_type = "liveblog.post.updated"

    post_id = instance.pk
    post_partial_url = reverse("post_partial", args=[post_id])

    # 채널 레이어에 값을 보낼 때는 반드시 딕셔너리로 보내야 하며 반드시 type 필드가 지정되어야 함
    instance.channel_layer_group_send(
        {
            "type": message_type,
            "post_id": post_id,
            "post_partial_url": post_partial_url,
        }
    )


# 시그널을 통한 등록(save()메소드가 끝날 때 실행)
# 첫 인자(receiver) : 실행할 함수(즉 시그널 발동시에 수행할 콜백함수), sender : 모델 객체, dispatch_uid : 시그널이 중복될 경우를 대비한 유니크한 식별자
post_save.connect(post__on_post_save, sender=Post, dispatch_uid="post__on_post_save")


def post__on_post_delete(instance: Post, **kwargs):
    post_id = instance.pk

    message_type = "liveblog.post.deleted"

    instance.channel_layer_group_send(
        {
            "type": message_type,
            "post_id": post_id,
        }
    )


post_delete.connect(
    post__on_post_delete, sender=Post, dispatch_uid="post__on_post_delete"
)
