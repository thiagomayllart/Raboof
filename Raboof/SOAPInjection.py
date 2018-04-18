
import HTTPRequester
import Thread_types

def multi_post_call(path, headers, payloadslist, boundaries, original_request):
    i = 1

    while i < len(boundaries):
        oldboundaries = boundaries[:]
        lines = boundaries[i].splitlines()
        oldline = lines[0][:]

        j = 0
        while j < len(payloadslist):
            pay_line = lines[:]
            pay_line[1] = lines[1] + payloadslist[j][0]
            pay_boundaries = boundaries[:]
            pay_boundaries[i] = '\n'.join(pay_line)
            pay_data = '\n\n'.join(pay_boundaries)
            pay_response = HTTPRequester.post_call(path, pay_data, headers)

            counter_pay_line = lines[:]
            counter_pay_line[1] = lines[1] + payloadslist[j][1]
            counter_pay_boundaries = boundaries[:]
            counter_pay_boundaries[i] = '\n'.join(counter_pay_line)
            counter_pay_data = '\n\n'.join(counter_pay_boundaries)
            counter_pay_response = HTTPRequester.post_call(path, counter_pay_data, headers)

            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadsi(path, headers, pay_data, counter_pay_data, original_request, lines[0], 'POST', pay_response, counter_pay_response)
            HTTPRequester.thread_starter(new_thread)
            lines[0] = oldline
            j = j + 1
            boundaries = oldboundaries
        i = i + 1

def common_post_call(path, headers, payloadslist, post_params, original_request):
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
            pay_response = HTTPRequester.post_call(path, pay_data, headers)

            counter_pay_vars = vars[:]
            counter_pay_vars[1] = vars[1] + payload[1]
            counter_pay_params = post_params[:]
            counter_pay_params[i] = '='.join(counter_pay_vars)
            counter_pay_data = '&'.join(counter_pay_params)
            counter_pay_response = HTTPRequester.post_call(path, counter_pay_data, headers)

            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadsi(path, headers, pay_data, counter_pay_data, original_request, '='.join(vars), 'POST', pay_response, counter_pay_response)
            HTTPRequester.thread_starter(new_thread)
            post_params = oldpost_params[:]
        i = i + 1

def get_call(path, headers, data, payloadslist, original_request):
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
            pay_response = HTTPRequester.get_call(pay_path, headers)

            counter_pay_vars = var[:]
            counter_pay_vars[1] = var[1] + payload[1]
            counter_pay_params = params[:]
            counter_pay_params[i] = '='.join(counter_pay_vars)
            counter_pay_data = '&'.join(counter_pay_params)
            counter_pay_path = url + '?' + counter_pay_data
            counter_pay_response = HTTPRequester.get_call(counter_pay_path, headers)

            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadsi(path, headers, pay_data, counter_pay_data, original_request, var, 'GET', pay_response,
                                               counter_pay_response)
            HTTPRequester.thread_starter(new_thread)
            params = oldparams[:]
        i = i + 1

    else:
        # no params to test
        pass