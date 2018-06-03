﻿import urllib2
import Thread_types
import time
import PayloadGenerator
import ParameterPollution
import SOAPInjection
import PathTraversal
import DynamicExecution
import urllib

requests_file = None
arr = None
file_string = None
max_threads = None
delay = None
option = None
threads_list = None
os = None
dt = None

def thread_starter(new_thread):
    global delay
    threads_list.append(new_thread)
    new_thread.start()
    time.sleep(delay)


def set_params(option1, max_threads1, delay1, os1, dt1):
    global option, max_threads, delay, os, dt
    max_threads = max_threads1
    option = option1
    delay = delay1
    os = os1
    dt = dt1


def get_call(path, headers):
    try:
        #ua = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        #headers.update(ua)
        req = urllib2.Request(path, headers=headers)
        response = urllib2.urlopen(req)
        return response
    except urllib2.HTTPError as e:
        return e


def post_call(path, data, headers):
    try:
        #ua = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        #headers.update(ua)
        req = urllib2.Request(path, data=data, headers=headers)
        response = urllib2.urlopen(req)
        return response
    except urllib2.HTTPError as e:
        return e


def set_file(file_location):
    global requests_file, file_string
    requests_file = open(file_location, "r")
    file_string = requests_file.read()
    requests_file.close()


def check_max_threads():
    global threads_list, max_threads

    while len(threads_list) == int(max_threads):
        for t in threads_list:
            if not t.isAlive():
                threads_list.remove(t)
        time.sleep(2)


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def HTTP_request():
    global option, threads_list, max_threads, delay, os, dt
    threads_list = []
    requests = file_string.split('<item>')
    requests.pop(0)

    payloadstype = option
    PayloadGenerator.setType(option)
    payloadslist = PayloadGenerator.payloadslist(option)

    for request in requests:

        path = urllib.unquote(find_between(request, '<url><![CDATA[', ']]></url>'))
        raw_request = find_between(request, '"false"><![CDATA[', ']]></request>')
        raw_header, data = raw_request.split('\n\n', 1)
        lines = raw_header.split('\n')
        method = ''
        if 'POST' in lines[0]:
            method = 'POST'
        else:
            if 'GET' in lines[0]:
                method = 'GET'

        headers = {}

        i = 1
        while i < len(lines):
            info = lines[i].split(': ', 1)
            if 'Content-Length' not in info[0]:
                headers.update({info[0]: info[1]})
            i = i + 1

        try:
            if method == 'POST':
                original_request = post_call(path, data, headers)
                if 'multipart/form-data' in headers.get('Content-Type'):
                    boundaries = data.split('\n\n')
                    if payloadstype == 'pp':
                        ParameterPollution.multi_post_call(path, headers, payloadslist, boundaries, original_request)

                    if payloadstype == 'si':
                        SOAPInjection.multi_post_call(path, headers, payloadslist, boundaries, original_request)

                    if payloadstype == 'pt':
                        PathTraversal.multi_post_call(path, headers, payloadslist, boundaries, original_request, os, dt)

                    if payloadstype == 'de':
                        DynamicExecution.multi_post_call(path, headers, payloadslist, boundaries, original_request)

                else:
                    post_params = data.split('&')
                    if payloadstype == 'pp':
                        ParameterPollution.common_post_call(path, headers, payloadslist, post_params, original_request)

                    if payloadstype == 'si':
                        SOAPInjection.common_post_call(path, headers, payloadslist, post_params, original_request)

                    if payloadstype == 'pt':
                        PathTraversal.common_post_call(path, headers, payloadslist, post_params, original_request, os, dt)

                    if payloadstype == 'de':
                        DynamicExecution.common_post_call(path, headers, payloadslist, post_params, original_request)

            if method == 'GET':
                if '?' in path:
                    original_request = get_call(path, headers)
                    if payloadstype == 'pp':
                        ParameterPollution.get_call(path, headers, data, payloadslist, original_request)

                    if payloadstype == 'si':
                        SOAPInjection.get_call(path, headers, data, payloadslist, original_request)

                    if payloadstype == 'pt':
                        PathTraversal.get_call(path, headers, data, payloadslist, original_request, os, dt)

                    if payloadstype == 'de':
                        DynamicExecution.get_call(path, headers, data, payloadslist, original_request)

                else:
                    #no params to test
                    pass


        except urllib2.HTTPError as err:
            print err

