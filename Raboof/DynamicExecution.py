
import HTTPRequester
import Thread_types

def multi_post_call_test_reply(path, headers, lines, boundaries, payload, i, original_request, checkstring):
    try:
        pay_line = lines[:]
        pay_line[1] = lines[1] + payload
        pay_boundaries = boundaries[:]
        pay_boundaries[i] = '\n'.join(pay_line)
        pay_data = '\n\n'.join(pay_boundaries)
        reply = HTTPRequester.post_call(path, pay_data, headers)
        if reply.getcode() == 200 and original_request.headers.get('content-length') != reply.headers.get('content-length') and checkstring in reply.read():
            return [True, pay_line[1], reply.headers.get('content-length')]
        else:
            return [False, None, None]
    except Exception as e:
        return [False, None, None]

def multi_post_call(path, headers, payloadslist, boundaries, original_request):
    i = 1

    while i < len(boundaries):
        lines = boundaries[i].splitlines()


        j = 0
        while j < len(payloadslist[0]): #testing if adding payloads to the beginning will return 200 ok
            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadde1(path, headers, lines, boundaries, payloadslist[0][j], i, 'multi_POST', original_request, payloadslist[2])
            HTTPRequester.thread_starter(new_thread)

            j = j + 1

        #Test for delay
        i = i + 1

def common_post_call_test_reply(path, headers, vars, post_params, payload, i, original_request, checkstring):
    try:

        pay_vars = vars[:]
        pay_vars[1] = vars[1] + payload
        pay_params = post_params[:]
        pay_params[i] = '='.join(pay_vars)
        pay_data = '&'.join(pay_params)

        reply = HTTPRequester.post_call(path, pay_data, headers)
        if reply.getcode() == 200 and original_request.headers.get('content-length') != reply.headers.get('content-length') and checkstring in reply.read():
            return [True, pay_vars[1], reply.headers.get('content-length')]
        else:
            return [False, None, None]
    except Exception as e:
        return [False, None, None]

def common_post_call(path, headers, payloadslist, post_params, original_request):
    i = 0

    while i < len(post_params):
        vars = post_params[i].split('=')
        j = 0
        while j < len(payloadslist[0]):  # testing if adding payloads to the beginning will return 200 ok
            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadde1(path, headers, vars, post_params, payloadslist[0][j], i, 'POST',
                                                original_request, payloadslist[2])
            HTTPRequester.thread_starter(new_thread)
            j = j + 1

        i = i + 1

def get_call_test_reply(url, headers, var, params, payload, i, original_request, checkstring):
    try:

        pay_vars = var[:]
        pay_vars[1] = var[1] + payload
        pay_params = params[:]
        pay_params[i] = '='.join(pay_vars)
        pay_data = '&'.join(pay_params)
        pay_path = url + '?' + pay_data

        reply = HTTPRequester.get_call(pay_path, headers)
        if reply.getcode() == 200 and original_request.headers.get('content-length') != reply.headers.get('content-length') and checkstring in reply.read():
            return [True, pay_vars[1], reply.headers.get('content-length')]
        else:
            return [False, None, None]
    except Exception as e:
        return [False, None, None]

def get_call(path, headers, data, payloadslist, original_request):
    url, link_params = path.split('?')
    params = link_params.split('&')
    i = 0
    while i < len(params):
        j = 0
        while j < len(payloadslist[0]):  # testing if adding payloads to the beginning will return 200 ok
            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadde1(url, headers, params, link_params, payloadslist[0][j], i, 'POST',
                                                original_request, payloadslist[2])
            HTTPRequester.thread_starter(new_thread)
            j = j + 1

        i = i + 1

    else:
        # no params to test
        pass