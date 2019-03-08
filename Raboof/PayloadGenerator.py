import HTTPRequester
import urllib
import random
import string

payload_type = None
pathtraversalaux_linux = 'TxtAux/LinuxPathTraversal.txt'
pathtraversalaux_windows = 'TxtAux/WindowsPathTraversal.txt'
###################################
parameter_pollution_payload = '&rab=oof'
###################################
soap_inj_foo = '</foo>'
soap_inj_foo_closed = '<foo></bar>'
soap_inj_comment = '<!--'
soap_inj_close_comment = '<!--beasted!-->'
###################################
pttestafter = ['...', '"""', "<<<>>>"]
pttestbefore = ['./././', 'gotya/../', 'gotya//....//', 'gotya\\\\....\\\\', 'gotya\\..\\..\\']
ptaddition = '../../../../../../../../../../../../'
nullbytes = ['%00.pdf', '%00.jpg', '%00.png', '%00.jpeg', '%00.mpeg', '%00.mp4', '%00.html', '%00.php', '%00.jsp', '%00.asp', '%00.js', '%00.cgi']
###################################
template_injection_test_type1 = ['{7*7}', '{{7*7}}']
template_injection_test_type2 = ['{7*\'7\'}','{{7*\'7\'}}']
###################################
paylist = None

def convert_to_unicode(payload):
    retVal = payload

    if payload:
        retVal = ""
        i = 0

        while i < len(payload):
            if payload[i] == '%' and (i < len(payload) - 2) and payload[i + 1:i + 2] in string.hexdigits and payload[
                                                                                                             i + 2:i + 3] in string.hexdigits:
                retVal += "%%u00%s" % payload[i + 1:i + 3]
                i += 3
            else:
                retVal += '%%u%.4X' % ord(payload[i])
                i += 1
    return retVal


def setType(option):
    global payload_type
    payload_type = option


def payloadslist(option):
    global paylist
    if option == 'pp':
        parameter_pollution_payload_gen()
    if option == 'si':
        soap_injection_payload_gen()
    if option == 'ti':
        template_injection_payload_gen()
    return paylist


def parameter_pollution_payload_gen():
    global paylist, parameter_pollution_payload, andutf16, equalutf16
    paylist = []
    paylist.append(urllib.quote_plus(parameter_pollution_payload))
    paylist.append(urllib.quote_plus(urllib.quote_plus(parameter_pollution_payload)))
    paylist.append(parameter_pollution_payload.replace('=', equalutf16).replace('&', andutf16))


def soap_injection_payload_gen():
    global paylist, soap_inj_foo, soap_inj_foo_closed, soap_inj_comment, soap_inj_close_comment
    paylist = []
    paylist.append([urllib.quote_plus(soap_inj_foo), urllib.quote_plus(soap_inj_foo_closed)])
    paylist.append([urllib.quote_plus(urllib.quote_plus(soap_inj_foo)), urllib.quote_plus(urllib.quote_plus(soap_inj_foo_closed))])
    paylist.append([convert_to_unicode(soap_inj_foo), convert_to_unicode(soap_inj_foo_closed)])

    paylist.append([urllib.quote_plus(soap_inj_comment), urllib.quote_plus(soap_inj_close_comment)])
    paylist.append(
        [urllib.quote_plus(urllib.quote_plus(soap_inj_comment)), urllib.quote_plus(urllib.quote_plus(soap_inj_close_comment))])
    paylist.append(
        [convert_to_unicode(soap_inj_comment),
         convert_to_unicode(soap_inj_close_comment)])

def template_injection_payload_gen():
    global template_injection_test_type1,template_injection_test_type2, paylist
    paylist = []
    paylist.append(template_injection_test_type1)
    paylist.append(template_injection_test_type2)
