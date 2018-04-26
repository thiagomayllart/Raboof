
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
            gibberish_line = lines[:]
            gibberish_line[1] = lines[1] + "gibberish"
            gibberish_boundaries = boundaries[:]
            gibberish_boundaries[i] = '\n'.join(gibberish_line)
            gibberish_data = '\n\n'.join(gibberish_boundaries)

            gibberish_numb_line = lines[:]
            gibberish_numb_line[1] = lines[1] + "777"
            gibberish_numb_boundaries = boundaries[:]
            gibberish_numb_boundaries[i] = '\n'.join(gibberish_numb_line)
            gibberish_numb_data = '\n\n'.join(gibberish_numb_boundaries)

            lines[0] = lines[0] + payloadslist[j]
            boundaries[i] = '\n'.join(lines)
            data = '\n\n'.join(boundaries)
            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadpp(path, data, headers, original_request, lines[0], 'POST',
                                               gibberish_data, gibberish_numb_data)
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

            gibberish_vars = vars[:]
            gibberish_vars[1] = vars[1] + "gibberish"
            gibberish_params = post_params[:]
            gibberish_params[i] = '='.join(gibberish_vars)
            gibberish_data = '&'.join(gibberish_params)

            gibberish_numb_vars = vars[:]
            gibberish_numb_vars[1] = vars[1] + "777"
            gibberish_numb_params = post_params[:]
            gibberish_numb_params[i] = '='.join(gibberish_numb_vars)
            gibberish_numb_data = '&'.join(gibberish_numb_params)

            vars[1] = vars[1] + payload
            post_params[i] = '='.join(vars)
            data = '&'.join(post_params)
            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadpp(path, data, headers, original_request, '='.join(vars), 'POST',
                                               gibberish_data, gibberish_numb_data)
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

            gibberish_vars = var[:]
            gibberish_vars[1] = var[1] + "gibberish"
            gibberish_params = params[:]
            gibberish_params[i] = '='.join(gibberish_vars)
            gibberish_data = '&'.join(gibberish_params)
            gibberish_path = url + '?' + gibberish_data

            gibberish_numb_vars = var[:]
            gibberish_numb_vars[1] = var[1] + "777"
            gibberish_numb_params = params[:]
            gibberish_numb_params[i] = '='.join(gibberish_numb_vars)
            gibberish_numb_data = '&'.join(gibberish_numb_params)
            gibberish_numb_path = url + '?' + gibberish_numb_data

            var[1] = var[1] + payload
            var = '='.join(var)
            params[i] = var
            params = '&'.join(params)
            path = url + '?' + params
            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadpp(path, data, headers, original_request, var, 'GET', gibberish_path,
                                               gibberish_numb_path)
            HTTPRequester.thread_starter(new_thread)
            params = oldparams[:]
        i = i + 1

    else:
        # no params to test
        pass