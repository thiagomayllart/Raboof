
import HTTPRequester
import Thread_types
import re
import zlib


def multi_post_call(path, headers, payloadslist, boundaries, original_request):
    #boundaries = array of post parameters

    HTTPRequester.check_max_threads() #check if all the threads are being used
    new_thread = Thread_types.Threadxxe(path, headers, payloadslist, boundaries, original_request, 'POST-MULTI')
    HTTPRequester.thread_starter(new_thread)

def common_post_call(path, headers, payloadslist, post_params, original_request):

    HTTPRequester.check_max_threads()
    new_thread = Thread_types.Threadxxe(path, headers, payloadslist, ''.join(post_params), original_request, 'POST')
    HTTPRequester.thread_starter(new_thread)

def get_call(path, headers, data, payloadslist, original_request):
    url, link_params = path.split('?')

    HTTPRequester.check_max_threads()
    new_thread = Thread_types.Threadxxe(url, headers, payloadslist, link_params, original_request, 'GET')
    HTTPRequester.thread_starter(new_thread)
