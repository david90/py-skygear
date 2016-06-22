import logging
import skygear
import requests
import urllib

from skygear import static_assets
from skygear.utils.assets import relative_assets
from .chat import plugin as chat_plugin
from .fb_messager import messager_handler

log = logging.getLogger(__name__)


@skygear.op("chima:hi")
def echo():
    return {"message": "Hello World"}


@static_assets(prefix='demo')
def chat_demo():
    return relative_assets('chat/js-sdk/demo')


@messager_handler('direction')
def direction(evt, postman):
    sender = evt['sender']['id']
    if 'message' in evt:
        msg = evt['message']
        reply = construct_reply(msg['text'])

        if 'text' in msg:
            r = postman.send(sender, reply)
    log.info('Cat cannot handle')


@messager_handler('fbwebhook')
def echo(evt, postman):
    sender = evt['sender']['id']
    if 'message' in evt:
        msg = evt['message']
        if 'text' in msg:
            r = postman.send(sender, msg['text'])
    log.info('Cat cannot handle')


# Helper
def get_direction_info(start_point, end_point):
    map_api_key = "AIzaSyCHrkIMXnwvJ8zLVFK0GrAqaxkHQByl1Nk"
    map_api_endpoint = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}"
    map_api_endpoint = map_api_endpoint.format(
        start_point,
        end_point,
        map_api_key)

    result = {}
    r = requests.get(map_api_endpoint)
    j = r.json()

    result["status"] = j["status"]
    routes = j["routes"]
    result["route_count"] = len(routes)
    if len(routes) > 0:
        legs = routes[0]["legs"]
        result["summary"] = routes[0]["summary"]

        result["leg_count"] = len(legs)
        result["distance"] = legs[0]["distance"]
        result["duration"] = legs[0]["duration"]
        result["start_address"] = legs[0]["start_address"]
        result["end_address"] = legs[0]["end_address"]
    return result


def parse_direction_question(text):
    tokens = text.split()
    from_point = ""
    to_point = ""
    detecting_from = False
    detecting_to = False
    for tok in tokens:
        if tok == '.' or tok == '?':
            detecting_to = False
        if detecting_from:
            from_point = from_point+" "+tok
        if tok == 'from':
            detecting_from = True
        if tok == 'to':
            detecting_from = False
            detecting_to = True
        if detecting_to:
            to_point = to_point+" "+tok
    return from_point, to_point


def construct_reply(text):
    reply = ""
    start_point, end_point = parse_direction_question(text)
    info = get_direction_info(start_point, end_point)

    if info["status"] == "OK":
        reply = "OK, it's {} away. It will take you {} to travel via {} from {} to {}. More: {}"
        more_link = "https://www.google.com/maps/dir/{}/{}".format(
            urllib.parse.quote(info["start_address"]),
            urllib.parse.quote(info["end_address"]
        )
        reply = reply.format(
            info["distance"]["text"],
            info["duration"]["text"],
            info["summary"],
            info["start_address"],
            info["end_address"],
            more_link)
    else:
        reply = "Oh, sorry. Can you be more exact? (e.g. HK Cyberport)"

    print(info)
    return reply
