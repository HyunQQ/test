import asyncio
import requests
import json

from aiohttp import ClientSession

from .models import InqMessage, InqChannels, InqChannelToUsers


def async_inq_api_requester(basic_uri: str, items: list, req_type: str = 'GET',) -> list:
    """
    비동기 인큐베이터 api 호출 함수
    basic_uri : basic uri format
    items : uri에 변경 가능한 옵션
    req_type : request type (GET or POST)
    return 호출 결과 list
    """

    async def request_inq(url, item):
        async with ClientSession() as session:
            if req_type == "GET":
                async with session.get(url) as response:
                    r = await response.json()
                    return r
            elif req_type == "POST":
                _item = json.dumps(item).encode('utf-8')
                async with session.post(url, data=_item) as response:
                    r = await response.json()
                    return r

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    if req_type == 'GET':
        for item in items:
            task = asyncio.ensure_future(request_inq(basic_uri.format(item)))
            tasks.append(task)
    elif req_type == 'POST':
        for item in items:
            task = asyncio.ensure_future(request_inq(basic_uri, item))
            tasks.append(task)

    loop.run_until_complete(asyncio.wait(tasks))

    result = [task.result() for task in tasks]
    return result


def inq_api_requester(basic_uri: str, items: list = [], req_type: str = "GET") -> list:
    """
    인큐베이터 api 호출 함수
    basic_uri : basic uri format
    items : uri에 변경 가능한 옵션
    req_type : request type (GET or POST)
    return 호출 결과 list
    """

    if len(items) > 0:
        if req_type == "GET":
            basic_uri += '{0}/'
        else:
            pass
        return async_inq_api_requester(basic_uri, items, req_type)
    else:
        return requests.get(basic_uri).json().get('data')


def check_message_table(uri: str, update: bool = False):
    """
    Check message table
    uri : message api uri
    update: Table update YN
    """
    if len(InqMessage.objects.all()) == 0:
        messages = inq_api_requester(uri)
        items = [InqMessage(
            id=item.get('id'),
            message=item.get('message'),
            channel_id=item.get('channel_id'),
            user_id=item.get('user_id'),
            created_at=item.get('created_at')
        )
            for item in messages]

        InqMessage.objects.bulk_create(items)

    else:
        if update:
            InqMessage.objects.all().delete()
            check_message_table(uri)


def check_channels_table(uri: str, update: bool = False):
    """
    Check channels table
    uri : channels api uri
    update: Table update YN
    """
    if len(InqChannels.objects.all()) == 0:
        channels = inq_api_requester(uri)
        items = [InqChannels(
            id=item.get('id'),
            name=item.get('name'),
        )
            for item in channels]

        InqChannels.objects.bulk_create(items)

    else:
        if update:
            InqChannels.objects.all().delete()
            check_channels_table(uri)


def check_channel_to_users_table(uri: str, update: bool = False):
    """
    Check channel_to_users table
    uri : channel_to_users api uri
    update: Table update YN
    """
    if len(InqChannelToUsers.objects.all()) == 0:
        channel_to_users = inq_api_requester(uri)
        items = [InqChannelToUsers(
            channel_id=item.get('channel_id'),
            user_id=item.get('user_id'),
        )
            for item in channel_to_users]

        InqChannelToUsers.objects.bulk_create(items)

    else:
        if update:
            InqChannelToUsers.objects.all().delete()
            check_channel_to_users_table(uri)
