import requests
import json

PAYLOAD = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Client-ID': 'uo6dggojyb8d6soh92zknwmi5ej1q2',
    'Authorization': 'OAuth cfabdegwdoklmawdzdo98xt2fo512y'
}

HEADER = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Client-ID': 'pd3lvk0ljyh29btxqptm8c1zmc512g',
}


def get_channel_id(name: str) -> str:
    channel = name
    url = 'https://api.twitch.tv/kraken/users?login=%s' % channel
    channel_id = requests.get(url, headers=HEADER)
    channel_id = json.loads(channel_id.text)
    channel_id = channel_id['users'][0]['_id']
    return channel_id


def view_channel_info(channel_name: int):
    channel_id = get_channel_id(channel_name)
    url = 'https://api.twitch.tv/kraken/channels/%d' % int(channel_id)

    r = requests.get(url, headers=HEADER)

    txt = r.text

    js = json.loads(txt)
    print(json.dumps(js, indent=2, sort_keys=True))


def check_stream_online(channel_name: int) -> bool:
    channel_id = get_channel_id(channel_name)
    url = 'https://api.twitch.tv/kraken/streams/%d' % int(channel_id)
    r = requests.get(url, headers=HEADER)
    txt = r.text
    js = json.loads(txt)

    if js['stream']:

        game = js['stream']['game']
        stream_name = js['stream']['channel']['status']
        js_output = json.dumps(json.loads(txt), indent=2, sort_keys=True)

        print(stream_name)
        print(game)
    else:
        print('stream is offline')


check_stream_online('ssslon_')
