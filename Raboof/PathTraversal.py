
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
            return [True, pay_line[1]]
        else:
            return [False, None]
    except Exception as e:
        return [False, None]

def multi_post_call(path, headers, payloadslist, boundaries, original_request, os, dt):
    i = 1

    while i < len(boundaries):
        lines = boundaries[i].splitlines()

        prob_path_trav_after = []

        j = 0
        while j < len(payloadslist[0]): #testing if adding payloads to the end will return 200 ok
            if multi_post_call_test_reply(path, headers, lines, boundaries, payloadslist[0][j], i, 0)[0] == True:
                prob_path_trav_after.append(payloadslist[0][j])
            j = j + 1

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

def common_post_call(path, headers, payloadslist, post_params, original_request, os, dt):
    i = 0

    while i < len(post_params):
        oldpost_params = post_params[:]
        vars = post_params[i].split('=')
        for payload in payloadslist:
            vars = post_params[i].split('=')

            pay_vars = vars[:]
            pay_vars[1] = vars[1] + payload[0]
            pay_params = post_params[:]
            pay_params[i] = '='.join(pay_vars)
            pay_data = '&'.join(pay_params)

            counter_pay_vars = vars[:]
            counter_pay_vars[1] = vars[1] + payload[1]
            counter_pay_params = post_params[:]
            counter_pay_params[i] = '='.join(counter_pay_vars)
            counter_pay_data = '&'.join(counter_pay_params)

            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadsi(path, headers, pay_data, counter_pay_data, original_request, '='.join(vars), 'POST', None, None)
            HTTPRequester.thread_starter(new_thread)
            post_params = oldpost_params[:]
        i = i + 1

def get_call(path, headers, data, payloadslist, original_request, os, dt):
    url, link_params = path.split('?')
    params = link_params.split('&')
    i = 0
    while i < len(params):
        oldparams = params[:]
        var = params[i].split('=')
        for payload in payloadslist:
            var = params[i].split('=')

            pay_vars = var[:]
            pay_vars[1] = var[1] + payload[0]
            pay_params = params[:]
            pay_params[i] = '='.join(pay_vars)
            pay_data = '&'.join(pay_params)
            pay_path = url + '?' + pay_data

            counter_pay_vars = var[:]
            counter_pay_vars[1] = var[1] + payload[1]
            counter_pay_params = params[:]
            counter_pay_params[i] = '='.join(counter_pay_vars)
            counter_pay_data = '&'.join(counter_pay_params)
            counter_pay_path = url + '?' + counter_pay_data

            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadsi(path, headers, pay_data, counter_pay_data, original_request, var, 'GET', pay_path,
                                               counter_pay_path)
            HTTPRequester.thread_starter(new_thread)
            params = oldparams[:]
        i = i + 1

    else:
        # no params to test
        pass