
import HTTPRequester
import Thread_types
import re
import zlib

def multi_post_call(path, headers, payloadslist, boundaries, original_request):
    i = 1

    while i < len(boundaries):
        oldboundaries = boundaries[:]
        lines = boundaries[i].splitlines()
        oldline = lines[0][:]

        #gotta identify the region where it gets substituted
        pay_line0 = lines[:]
        payload_to_get_region = "bar1337FOO1337bar"
        pay_line0[1] = payload_to_get_region
        pay_boundaries0 = boundaries[:]
        pay_boundaries0[i] = '\n'.join(pay_line0)
        pay_data0 = '\n\n'.join(pay_boundaries0)
        response_compare = HTTPRequester.post_call(path, pay_data0, headers)
        response_html = response_compare.read()
        if response_compare.headers.get('Content-Encoding') != None:
            if 'gzip' in response_compare.headers.get('Content-Encoding'):
                response_html = zlib.decompress(response_html, 16 + zlib.MAX_WBITS)
        occurrances = [m.start() for m in re.finditer(payload_to_get_region, response_html)]
        list_regions = []
        for occ in occurrances:
            list_regions.append([response_html[(occ-20):occ], response_html[(occ+len(payload_to_get_region)):((occ+len(payload_to_get_region))+20)]])


        j = 0
        while j < len(payloadslist[0]):
            pay_line1 = lines[:]
            pay_line1[1] = payloadslist[0][j]
            pay_boundaries1 = boundaries[:]
            pay_boundaries1[i] = '\n'.join(pay_line1)
            pay_data1 = '\n\n'.join(pay_boundaries1)
            HTTPRequester.check_max_threads() #check if all the threads are being used
            new_thread = Thread_types.Threadti(path, headers, pay_data1, original_request, pay_line1, 'POST', None, 0, list_regions)
            HTTPRequester.thread_starter(new_thread)
            lines[0] = oldline
            boundaries = oldboundaries
            j = j + 1

        j = 0
        while j < len(payloadslist[1]):
            pay_line2 = lines[:]
            pay_line2[1] = payloadslist[1][j]
            pay_boundaries2 = boundaries[:]
            pay_boundaries2[i] = '\n'.join(pay_line2)
            pay_data2 = '\n\n'.join(pay_boundaries2)

            HTTPRequester.check_max_threads() #check if all the threads are being used
            new_thread = Thread_types.Threadti(path, headers, pay_data2, original_request, pay_line2, 'POST', None, 1, list_regions)
            HTTPRequester.thread_starter(new_thread)
            lines[0] = oldline
            boundaries = oldboundaries
            j = j + 1
        i = i + 1

def common_post_call(path, headers, payloadslist, post_params, original_request):
    i = 0
    #shoud work with json and XML
    try:
        while i < len(post_params):
            oldpost_params = post_params[:]
            vars0 = post_params[i].split('=', 1)
            if len(vars0) == 1:
                vars0.append("fillparam")
            pay_vars0 = vars0[:]
            payload_to_get_region = "bar1337FOO1337bar"
            pay_vars0[1] = payload_to_get_region
            pay_params0 = post_params[:]
            pay_params0[i] = '='.join(pay_vars0)
            pay_data0 = '&'.join(pay_params0)
            response_compare = HTTPRequester.post_call(path, pay_data0, headers)
            response_html = response_compare.read()
            if response_compare.headers.get('Content-Encoding') != None:
                if 'gzip' in response_compare.headers.get('Content-Encoding'):
                    response_html = zlib.decompress(response_html, 16 + zlib.MAX_WBITS)
            occurrances = [m.start() for m in re.finditer(payload_to_get_region, response_html)]
            list_regions = []
            for occ in occurrances:
                list_regions.append([response_html[(occ - 20):occ], response_html[(occ + len(payload_to_get_region)):(
                            (occ + len(payload_to_get_region)) + 20)]])

            j = 0
            while j < len(payloadslist[0]):
                payload = payloadslist[0][j]
                vars1 = post_params[i].split('=')
                if len(vars1) == 1:
                    vars1.append("fillparam")
                pay_vars1 = vars1[:]
                pay_vars1[1] = payload
                pay_params1 = post_params[:]
                pay_params1[i] = '='.join(pay_vars1)
                pay_data1 = '&'.join(pay_params1)


                HTTPRequester.check_max_threads()
                new_thread = Thread_types.Threadti(path, headers, pay_data1, original_request, '='.join(pay_vars1), 'POST', None, 0, list_regions)
                HTTPRequester.thread_starter(new_thread)
                post_params = oldpost_params[:]
                j = j + 1

            j = 0
            while j < len(payloadslist[1]):
                payload = payloadslist[1][j]
                vars2 = post_params[i].split('=')
                if len(vars2) == 1:
                    vars2.append("fillparam")
                pay_vars2 = vars2[:]
                pay_vars2[1] = payload
                pay_params2 = post_params[:]
                pay_params2[i] = '='.join(pay_vars2)
                pay_data2 = '&'.join(pay_params2)


                HTTPRequester.check_max_threads()
                new_thread = Thread_types.Threadti(path, headers, pay_data2, original_request, '='.join(pay_vars2), 'POST', None, 1, list_regions)
                HTTPRequester.thread_starter(new_thread)
                post_params = oldpost_params[:]
                j = j + 1
            i = i + 1
    except Exception as msg:
        print msg
        print post_params

def get_call(path, headers, data, payloadslist, original_request):
    url, link_params = path.split('?', 1)
    params = link_params.split('&')
    i = 0
    while i < len(params):
        oldparams = params[:]
        var0 = params[i].split('=', 1)
        if len(var0) == 1:
            var0.append("fillparam")
        pay_vars0 = var0[:]
        payload_to_get_region = "bar1337FOO1337bar"
        pay_vars0[1] = payload_to_get_region
        pay_params0 = params[:]
        pay_params0[i] = '='.join(pay_vars0)
        pay_data0 = '&'.join(pay_params0)
        pay_path0 = url + '?' + pay_data0
        response_compare = HTTPRequester.get_call(pay_path0, headers)
        response_html = response_compare.read()
        if response_compare.headers.get('Content-Encoding') != None:
            if 'gzip' in response_compare.headers.get('Content-Encoding'):
                response_html = zlib.decompress(response_html, 16 + zlib.MAX_WBITS)
        occurrances = [m.start() for m in re.finditer(payload_to_get_region, response_html)]
        list_regions = []
        for occ in occurrances:
            list_regions.append([response_html[(occ - 20):occ], response_html[(occ + len(payload_to_get_region)):(
                    (occ + len(payload_to_get_region)) + 20)]])

        j = 0
        while j < len(payloadslist[0]):
            payload = payloadslist[0][j]
            var1 = params[i].split('=')
            if len(var1) == 1:
                var1.append("fillparam")
            pay_vars1 = var1[:]
            pay_vars1[1] = payload
            pay_params1 = params[:]
            pay_params1[i] = '='.join(pay_vars1)
            pay_data1 = '&'.join(pay_params1)
            pay_path1 = url + '?' + pay_data1


            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadti(path, headers, pay_data1, original_request, pay_params1[i], 'GET', pay_path1,
                                                0, list_regions)
            HTTPRequester.thread_starter(new_thread)
            params = oldparams[:]
            j = j + 1

        j = 0
        while j < len(payloadslist[1]):
            payload = payloadslist[1][j]
            var2 = params[i].split('=')
            if len(var2) == 1:
                var2.append("fillparam")
            pay_vars2 = var2[:]
            pay_vars2[1] = payload
            pay_params2 = params[:]
            pay_params2[i] = '='.join(pay_vars2)
            pay_data2 = '&'.join(pay_params2)
            pay_path2 = url + '?' + pay_data2


            HTTPRequester.check_max_threads()
            new_thread = Thread_types.Threadti(path, headers, pay_data2, original_request, pay_params2[i], 'GET', pay_path2,
                                                0, list_regions)
            HTTPRequester.thread_starter(new_thread)
            params = oldparams[:]
            j = j + 1
        i = i + 1

    else:
        # no params to test
        pass