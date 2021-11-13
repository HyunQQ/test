import json

import numpy as np
from django.http import HttpResponse
from django.views import View
from django.db.models import Q

from .utils import inq_api_requester, check_message_table, check_channels_table, check_channel_to_users_table
from .models import InqMessage, InqChannels, InqChannelToUsers


class MessageList(View):
    # TODO 1번 기능 구현
    def get(self, *args, **kwargs):
        # get request parameters
        param_channel_ids = self.request.GET.getlist('channel_id')
        param_message = self.request.GET.get('message')
        param_nickname = self.request.GET.get('nickname')
        param_table_update = self.request.GET.get('update', False)

        # uri value
        message_inq_uri = 'https://ipd-incubator.toss.im/api/v1/messages/'
        users_inq_uri = 'https://ipd-incubator.toss.im/api/v1/users/'
        channels_inq_uri = 'https://ipd-incubator.toss.im/api/v1/channels/'
        channel_to_user_list_inq_uri = 'https://ipd-incubator.toss.im/api/v1/channel-to-users/'

        # check table
        check_message_table(message_inq_uri, param_table_update)
        check_channels_table(channels_inq_uri, param_table_update)
        check_channel_to_users_table(channel_to_user_list_inq_uri, param_table_update)

        # users는 1시간 별로 변동이 가능하므로 api를 통해서 조회
        users = inq_api_requester(users_inq_uri)

        # make filter options
        q = Q()
        if param_message:
            q.add(Q(message__contains=param_message), q.OR)
        if len(param_channel_ids) > 0:
            q.add(Q(channel_id__in=param_channel_ids), q.OR)
        if param_nickname:
            q.add(Q(user_id__in=[
                _user.get('id') for _user in users if _user.get('nickname', '') == param_nickname
            ]), q.OR)

        # set message info
        messages = list(InqMessage.objects.filter(q).values())
        for message in messages:
            message['channel'] = list(InqChannels.objects.filter(id=message.get('channel_id')).values())
            for user in users:
                if message.get('user_id') == user.get('id'):
                    if user.get('included_channels'):
                        pass
                    else:
                        user['included_channels'] = list(InqChannelToUsers.objects.filter(user_id=user.get('id'))
                                                         .values_list('channel_id', flat=True))
                    message['user'] = user

        sorted_payload = sorted(
            messages, key=lambda x: x.get('created_at'), reverse=True
        )

        return HttpResponse(json.dumps({'payload': sorted_payload}),
                            content_type='application/json; charset=utf8')


# TODO 2번 기능 구현
class MessageSendAPI(View):
    def get(self, *args, **kwargs):
        # get request parameters
        param_message = self.request.GET.get('message')

        # uri value
        message_sent_inq_uri = 'https://ipd-incubator.toss.im/api/v1/messages/'

        # make filter options
        q = Q()
        if param_message:
            q.add(Q(message__contains=param_message), q.OR)

        # get list for send message
        users = list(set(InqChannelToUsers.objects
                         .filter(channel_id__in=set(InqMessage.objects.filter(q).values_list('channel_id', flat=True)))
                         .values_list('user_id', flat=True)))

        request_params = [
            {
                'user_id': user,
                'text': '리마인드 메시지입니다.'
            }
            for user in users
        ]

        # api request 실패건이 없을때까지 요청
        while len(request_params) != 0:
            request_result = inq_api_requester(message_sent_inq_uri, request_params, "POST")
            idx_list = []
            for idx, item in enumerate(request_result):
                if item.get('success') is None:
                    idx_list.append(idx)

            request_params = np.array(request_params)[idx_list].tolist()

        return HttpResponse(json.dumps({'msg': '메세지 요청에 성공했습니다.'}),
                            content_type='application/json; charset=utf8')

