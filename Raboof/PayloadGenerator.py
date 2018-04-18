import HTTPRequester
import urllib


payload_type = None
parameter_pollution_payload = '&rab=oof'
soap_inj_foo = '</foo>'
soap_inj_foo_closed = '<foo></foo>'
soap_inj_comment = '<!--'
soap_inj_close_comment = '<!--beasted!-->'
paylist = None
lessthanutf16 = '%u003C'
greaterthanutf16 = '%u003E'
exclamationutf16 = '%u0021'
hyphenutf16 = '%u002D'
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
    if option == 'si':
        soap_injection_payload_gen()
    return paylist


def parameter_pollution_payload_gen():
    global paylist, parameter_pollution_payload, andutf16, equalutf16
    paylist = []
    paylist.append(urllib.quote_plus(parameter_pollution_payload))
    paylist.append(urllib.quote_plus(urllib.quote_plus(parameter_pollution_payload)))
    paylist.append(parameter_pollution_payload.replace('=', equalutf16).replace('&', andutf16))


def soap_injection_payload_gen():
    global paylist, soap_inj_foo, soap_inj_foo_closed, soap_inj_comment, soap_inj_close_comment
    paylist.append([urllib.quote_plus(soap_inj_foo), urllib.quote_plus(soap_inj_foo_closed)])
    paylist.append([urllib.quote_plus(urllib.quote_plus(soap_inj_foo)), urllib.quote_plus(urllib.quote_plus(soap_inj_foo_closed))])
    paylist.append([soap_inj_foo.replace('<', lessthanutf16).replace('/', forwardslashutf16).replace('>', greaterthanutf16),
                    soap_inj_foo_closed.replace('<', lessthanutf16).replace('/', forwardslashutf16).replace('>', greaterthanutf16)])

    paylist.append([urllib.quote_plus(soap_inj_comment), urllib.quote_plus(soap_inj_close_comment)])
    paylist.append(
        [urllib.quote_plus(urllib.quote_plus(soap_inj_comment)), urllib.quote_plus(urllib.quote_plus(soap_inj_close_comment))])
    paylist.append(
        [soap_inj_comment.replace('<', lessthanutf16).replace('!', exclamationutf16).replace('-', hyphenutf16),
         soap_inj_close_comment.replace('<', lessthanutf16).replace('!', exclamationutf16).replace('-', hyphenutf16).replace('>', greaterthanutf16)])
