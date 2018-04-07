import HTTPRequester
import urllib


payload_type = None
parameter_pollution_payload = '&rab=oof'
paylist = None
dotutf16 = '%u002e'
forwardslashutf16 = '%u2215'
backslashutf16 = '%u2216'
andutf16 = '%u0026'
equalutf16 = '%u003D'



def setType(option):
    global payload_type
    payload_type = option


def payloadslist(option):
    global paylist
    if option == 'pp':
        parameter_pollution_payload_gen()
    return paylist


def parameter_pollution_payload_gen():
    global paylist, parameter_pollution_payload, andutf16, equalutf16
    paylist = []
    paylist.append(urllib.quote_plus(parameter_pollution_payload))
    paylist.append(urllib.quote_plus(urllib.quote_plus(parameter_pollution_payload)))
    paylist.append(parameter_pollution_payload.replace('=', equalutf16).replace('&', andutf16))