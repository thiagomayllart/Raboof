
import HTTPRequester
import Thread_types

def multi_post_call_test_reply(path, headers, lines, boundaries, payload, i, before_or_after):
    try:
        pay_line = lines[:]
        if before_or_after == 0:
            pay_line[1] = lines[1] + payload
        else:
            pay_line[1] = payload + lines[1]
        pay_boundaries = boundaries[:]
        pay_boundaries[i] = '\n'.join(pay_line)
        pay_data = '\n\n'.join(pay_boundaries)
        reply = HTTPRequester.post_call(path, pay_data, headers)
        if reply.getcode() == 200:
            return [True, pay_line[1], reply.headers.get('content-length')]
        else:
            return [False, None, None]
    except Exception as e:
        print e
        return [False, None, None]

def multi_post_call(path, headers, payloadslist, boundaries, original_request, os, dt):
    i = 1

    while i < len(boundaries):
        lines = boundaries[i].splitlines()

        prob_path_trav_after = []

        #j = 0
        #while j < len(payloadslist[0]): #testing if adding payloads to the end will return 200 ok
        #    if multi_post_call_test_reply(path, headers, lines, boundaries, payloadslist[1][j], i, 0)[0] == True:
        #        prob_path_trav_after.append(payloadslist[1][j])
        #    j = j + 1

        prob_path_trav_before = []
        j = 0
        while j < len(payloadslist[1]): #testing if adding payloads to the beginning will return 200 ok
            if multi_post_call_test_reply(path, headers, lines, boundaries, payloadslist[0][j], i, 1)[0] == True:
                prob_path_trav_before.append(payloadslist[0][j])
            j = j + 1

        HTTPRequester.check_max_threads()
        new_thread = Thread_types.Threadpt(path, headers, prob_path_trav_before, prob_path_trav_after, original_request,
                                           lines[0], 'multi_POST', payloadslist[2], payloadslist[3], os, dt,
                                           [path, headers, lines, boundaries, i, 0])
        HTTPRequester.thread_starter(new_thread)
        i = i + 1

def common_post_call_test_reply(path, headers, vars, post_params, payload, i, before_or_after):
    try:

        pay_vars = vars[:]
        if before_or_after == 0:
            pay_vars[1] = vars[1] + payload
        else:
            pay_vars[1] = payload + vars[1]
        pay_params = post_params[:]
        pay_params[i] = '='.join(pay_vars)
        pay_data = '&'.join(pay_params)

        reply = HTTPRequester.post_call(path, pay_data, headers)
        if reply.getcode() == 200:
            return [True, pay_vars[1], reply.headers.get('content-length')]
        else:
            return [False, None, None]
    except Exception as e:
        print e
        return [False, None, None]

def common_post_call(path, headers, payloadslist, post_params, original_request, os, dt):
    i = 0

    while i < len(post_params):
        vars = post_params[i].split('=')
        j = 0

        prob_path_trav_after = []

        #while j < len(payloadslist[0]):
        #    if common_post_call_test_reply(path, headers, vars, post_params, payloadslist[1][j], i, 0)[0] == True:
        #        prob_path_trav_after.append(payloadslist[0][j])
        #    j = j + 1

        prob_path_trav_before = []
        j = 0
        while j < len(payloadslist[1]):  # testing if adding payloads to the beginning will return 200 ok
            if common_post_call_test_reply(path, headers, vars, post_params, payloadslist[0][j], i, 1)[0] == True:
                prob_path_trav_before.append(payloadslist[1][j])
            j = j + 1

        HTTPRequester.check_max_threads()
        new_thread = Thread_types.Threadpt(path, headers, prob_path_trav_before, prob_path_trav_after, original_request,
                                           vars[0], 'POST', payloadslist[2], payloadslist[3], os, dt,
                                           [path, headers, vars, post_params, i, 0])
        HTTPRequester.thread_starter(new_thread)
        i = i + 1

def get_call_test_reply(path, headers, var, params, payload, i, before_or_after, url):
    try:

        pay_vars = var[:]
        if before_or_after == 0:
            pay_vars[1] = var[1] + payload
        else:
            pay_vars[1] = payload + var[1]
        pay_params = params[:]
        pay_params[i] = '='.join(pay_vars)
        pay_data = '&'.join(pay_params)
        pay_path = url + '?' + pay_data

        reply = HTTPRequester.get_call(pay_path, headers)
        if reply.getcode() == 200:
            return [True, pay_vars[1], reply.headers.get('content-length')]
        else:
            return [False, None, None]
    except Exception as e:
        print e
        return [False, None, None]

def get_call(path, headers, data, payloadslist, original_request, os, dt):
    url, link_params = path.split('?')
    params = link_params.split('&')
    i = 0
    while i < len(params):
        var = params[i].split('=')

        j = 0

        prob_path_trav_after = []

        #while j < len(payloadslist[1]):
        #    if get_call_test_reply(path, headers, var, params, payloadslist[1][j], i, 0, url)[0] == True:
        #        prob_path_trav_after.append(payloadslist[1][j])
        #    j = j + 1

        prob_path_trav_before = []
        j = 0
        while j < len(payloadslist[0]):  # testing if adding payloads to the beginning will return 200 ok
            if get_call_test_reply(path, headers, var, params, payloadslist[0][j], i, 1, url)[0] == True:
                prob_path_trav_before.append(payloadslist[0][j])
            j = j + 1
        HTTPRequester.check_max_threads()
        new_thread = Thread_types.Threadpt(path, headers, prob_path_trav_before, prob_path_trav_after, original_request,
                                           var[0], 'GET', payloadslist[2], payloadslist[3], os, dt,
                                           [path, headers, var, params, i, 0, url])
        HTTPRequester.thread_starter(new_thread)

        i = i + 1

    else:
        # no params to test
        pass