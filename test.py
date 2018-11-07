import requests
import json

payload = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Client-ID': 'uo6dggojyb8d6soh92zknwmi5ej1q2',
    'Authorization': 'OAuth cfabdegwdoklmawdzdo98xt2fo512y'
}

header = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Client-ID': 'pd3lvk0ljyh29btxqptm8c1zmc512g',

}
channel = 78181956  # may be xdd
url = 'https://api.twitch.tv/kraken/channels/%d' % channel


r = requests.get(url, headers=header)

print(type(r.text))
