import HTTPRequester
from threading import Thread
import PathTraversal
import time
import DynamicExecution

class Threadde1(Thread):
    def __init__(self, path, headers, lines, param, payload, i, req_type, original_request, checkstring, url):
        Thread.__init__(self)
        self.path = path
        self.headers = headers
        self.lines = lines
        self.param_exploited = param
        self.original_request = original_request
        self.reqtype = req_type
        self.payload = payload
        self.checkstring = checkstring
        self.url = url
        self.i = i

    def run(self):
        response = ''
        result = []
        if self.reqtype == 'multi_POST':
            result = DynamicExecution.multi_post_call_test_reply(self.path, self.headers, self.lines, self.param_exploited, self.payload, self.i, self.original_request, self.checkstring)
        else:
            if self.reqtype == 'POST' :
                result = DynamicExecution.common_post_call_test_reply(self.path, self.headers, self.lines, self.param_exploited, self.payload, self.i, self.original_request, self.checkstring)
            else:
                if self.reqtype == 'GET':
                    result = DynamicExecution.get_call_test_reply(self.url, self.headers, self.lines, self.param_exploited, self.payload, self.i, self.original_request, self.checkstring)
        if result[0] != False:
            print '[+] DYNAMIC EXECUTION FOUND: '
            print '[+]PATH: ' + self.path
            print '[+]LOCATION: '+ self.lines[0] + "=" + self.lines[1]
            print '[+]PAYLOAD: ' + self.payload
            print '[+]REQUEST TYPE: '+ self.reqtype
            for x in self.headers:
                print x + ': ' + self.headers.get(x)
            print "----------------------------------------------------------------------------------------------\n"

class Threadpp(Thread):
    def __init__(self, path, data, headers, original_request, param_exploited, reqtype, gibberish_data, gibberish_numb_data):
        Thread.__init__(self)
        if reqtype == 'POST':
            self.gibberish_response = HTTPRequester.post_call(path, gibberish_data, headers)
            self.gibberish_numb_response = HTTPRequester.post_call(path, gibberish_numb_data, headers)
        else:
            self.gibberish_response = HTTPRequester.get_call(gibberish_data, headers)
            self.gibberish_numb_response = HTTPRequester.get_call(gibberish_numb_data, headers)
        self.path = path
        self.data = data
        self.headers = headers
        self.original_request = original_request
        self.param_exploited = param_exploited
        self.reqtype = reqtype

    def run(self):
        response = ''
        if self.gibberish_response.getcode() != self.original_request.getcode() or self.gibberish_response.headers.get('content-length') != self.original_request.headers.get('content-length') or \
                self.gibberish_numb_response.getcode() != self.original_request.getcode() or self.gibberish_numb_response.headers.get('content-length') != self.original_request.headers.get('content-length'):
            if self.reqtype == 'POST':
                response = HTTPRequester.post_call(self.path, self.data, self.headers)
            if self.reqtype == 'GET':
                response = HTTPRequester.get_call(self.path, self.headers)
            if self.original_request.getcode() == response.getcode():
                if self.original_request.headers.get('content-length') == response.headers.get('content-length'):
                    print "PARAMETER POLLUTION: "
                    print "LOCATION " + self.param_exploited
                    print "REQUEST TYPE:" + self.reqtype
                    print "PRINTING REQUEST: "
                    print self.path
                    print self.data
                    for x in self.headers:
                        print x + ': ' + self.headers.get(x)
                    print "----------------------------------------------------------------------------------------------\n"
        else:
            #probably not exploitable
            pass

class Threadsi(Thread):
    def __init__(self, path, headers, data_pay, data_counter_pay, original_request, param_exploited, reqtype, pay_path, counter_pay_path):
        Thread.__init__(self)
        if reqtype == 'POST':
            self.pay_response = HTTPRequester.post_call(path, data_pay, headers)
            self.counter_pay_response = HTTPRequester.post_call(path, data_counter_pay, headers)
        else:
            self.pay_response = HTTPRequester.get_call(pay_path, headers)
            self.counter_pay_response = HTTPRequester.get_call(counter_pay_path, headers)
        self.path = path
        self.headers = headers
        self.original_request = original_request
        self.param_exploited = param_exploited
        self.data_pay = data_pay
        self.data_counter_pay = data_counter_pay
        self.reqtype = reqtype

    def run(self):
        response = ''
        if self.pay_response.getcode() != self.counter_pay_response.getcode():
            print 'SOAP INJECTION: '
            print 'HTTP REPLY CODE DIVERGED: '
            self.message_function()

        else:
            if self.pay_response.headers.get('content-length') != self.counter_pay_response.headers.get('content-length'):
                print 'SOAP INJECTION: '
                print 'HTTP CONTENT-LENGTH CODE DIVERGED: '
                self.message_function()

            else:
                #probably not exploitable
                pass

    def message_function(self):
        print 'HTTP REPLY CODE : ' + self.pay_response.getcode + ' and ' + self.counter_pay_response.getcode()
        print 'HTTP CONTENT-LENGTH ' + self.pay_response.headers.get('content-length') + ' and ' + \
              self.counter_pay_response.headers.get('content-length')
        print 'LOCATION: ' + self.param_exploited
        print 'REQUEST TYPE: ' + self.reqtype
        print 'PRINTING REQUEST: '
        print 'PATH :' + self.path
        print 'FIRST PAYLOAD DATA: ' + self.data_pay
        print 'SECOND PAYLOAD DATA: ' + self.data_counter_pay
        for x in self.headers:
            print x
            ': ' + self.headers.get(x)
        print "----------------------------------------------------------------------------------------------\n"

class Threadpt(Thread):
    def __init__(self, path, headers, prob_path_trav_before, prob_path_trav_after, original_request, param_exploited,
                 reqtype, windows_payloads, linux_payloads, os, delay, aux_params_to_rebuild_req):
        Thread.__init__(self)
        self.path = path
        self.headers = headers
        self.original_request = original_request
        self.param_exploited = param_exploited
        self.reqtype = reqtype
        self.prob_path_trav_before = prob_path_trav_before
        self.prob_path_trav_after = prob_path_trav_after
        self.aux_params_to_rebuild_req = aux_params_to_rebuild_req
        self.windows_payloads = windows_payloads
        self.linux_payloads = linux_payloads
        self.os = os
        self.delay = delay

    def run(self):
        print 'PARAMETER EXPLOITABLE FOUND'
        print 'PATH: ' + self.path
        print 'PARAM: ' + self.param_exploited
        print 'PAYLOADS RETURNED 200 OK: '
        for pay in self.prob_path_trav_after:
            print pay
        for pay in self.prob_path_trav_before:
            print pay
        print '[+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+]'
        print 'PROBING COMMON FILE PATHS'
        if self.os == 'b' or self.os == 'w':
            if self.reqtype == 'multi_POST':
                for pay in self.windows_payloads:
                    test = PathTraversal.multi_post_call_test_reply(self.aux_params_to_rebuild_req[0], self.aux_params_to_rebuild_req[1],
                                                     self.aux_params_to_rebuild_req[2], self.aux_params_to_rebuild_req[3],
                                                         pay, self.aux_params_to_rebuild_req[4],
                                                         self.aux_params_to_rebuild_req[5])
                    time.sleep(self.delay)
                    if test[0] == True and abs(int(test[2]) - int(self.original_request.headers.get('content-length'))) > 1000 and int(test[2]) > 20:
                        print '[+][+][+][+][+][+][+][+][+][+][+]'
                        print 'PATH TRAVERSAL FOUND'
                        print 'PATH: ' + self.path
                        print 'REQUEST: ' + self.reqtype
                        print 'PARAM: ' + self.param_exploited
                        print 'Content-Length Payload Request: ' + str(int(test[2]))
                        print 'Content-Length Original Request: ' + self.original_request.headers.get(
                            'content-length')
                        print 'ON: ' + test[1]

            else:
                if self.reqtype == 'POST':
                    for pay in self.windows_payloads:
                        test = PathTraversal.common_post_call_test_reply(self.aux_params_to_rebuild_req[0],
                                                                        self.aux_params_to_rebuild_req[1],
                                                                        self.aux_params_to_rebuild_req[2],
                                                                        self.aux_params_to_rebuild_req[3],
                                                                        pay, self.aux_params_to_rebuild_req[4],
                                                                        self.aux_params_to_rebuild_req[5])
                        time.sleep(self.delay)
                        if test[0] == True and abs(
                                int(test[2]) - int(self.original_request.headers.get('content-length'))) > 1000 and int(test[2]) > 20:
                            print '[+][+][+][+][+][+][+][+][+][+][+]'
                            print 'PATH TRAVERSAL FOUND'
                            print 'PATH: ' + self.path
                            print 'REQUEST: ' + self.reqtype
                            print 'PARAM: ' + self.param_exploited
                            print 'Content-Length Payload Request: ' + str(int(test[2]))
                            print 'Content-Length Original Request: ' + self.original_request.headers.get(
                                'content-length')
                            print 'ON: ' + test[1]

                else:
                    if self.reqtype == 'GET':
                        for pay in self.windows_payloads:
                            test = PathTraversal.get_call_test_reply(self.aux_params_to_rebuild_req[0],
                                                                             self.aux_params_to_rebuild_req[1],
                                                                             self.aux_params_to_rebuild_req[2],
                                                                             self.aux_params_to_rebuild_req[3],
                                                                             pay, self.aux_params_to_rebuild_req[4],
                                                                             self.aux_params_to_rebuild_req[5],
                                                                             self.aux_params_to_rebuild_req[6])
                            time.sleep(self.delay)
                            if test[0] == True and abs(int(test[2]) - int(
                                    self.original_request.headers.get('content-length'))) > 1000 and int(test[2]) > 20:
                                print '[+][+][+][+][+][+][+][+][+][+][+]'
                                print 'PATH TRAVERSAL FOUND'
                                print 'PATH: ' + self.path
                                print 'REQUEST: ' + self.reqtype
                                print 'PARAM: ' + self.param_exploited
                                print 'Content-Length Payload Request: ' + str(int(test[2]))
                                print 'Content-Length Original Request: ' + self.original_request.headers.get(
                                    'content-length')
                                print 'ON: ' + test[1]

        if self.os == 'b' or self.os == 'l':
            if self.reqtype == 'multi_POST':
                for pay in self.linux_payloads:
                    test = PathTraversal.multi_post_call_test_reply(self.aux_params_to_rebuild_req[0], self.aux_params_to_rebuild_req[1],
                                                     self.aux_params_to_rebuild_req[2], self.aux_params_to_rebuild_req[3],
                                                         pay, self.aux_params_to_rebuild_req[4],
                                                         self.aux_params_to_rebuild_req[5])
                    time.sleep(self.delay)
                    if test[0] == True and abs(
                            int(test[2]) - int(self.original_request.headers.get('content-length'))) > 1000 and int(test[2]) > 20:
                        print '[+][+][+][+][+][+][+][+][+][+][+]'
                        print 'PATH TRAVERSAL FOUND'
                        print 'PATH: ' + self.path
                        print 'REQUEST: ' + self.reqtype
                        print 'PARAM: ' + self.param_exploited
                        print 'Content-Length Payload Request: ' + str(int(test[2]))
                        print 'Content-Length Original Request: ' + self.original_request.headers.get(
                            'content-length')
                        print 'ON: ' + test[1]

            else:
                if self.reqtype == 'POST':
                    for pay in self.windows_payloads:
                        test = PathTraversal.common_post_call_test_reply(self.aux_params_to_rebuild_req[0],
                                                                        self.aux_params_to_rebuild_req[1],
                                                                        self.aux_params_to_rebuild_req[2],
                                                                        self.aux_params_to_rebuild_req[3],
                                                                        pay, self.aux_params_to_rebuild_req[4],
                                                                        self.aux_params_to_rebuild_req[5])
                        time.sleep(self.delay)
                        if test[0] == True and abs(
                                int(test[2]) - int(self.original_request.headers.get('content-length'))) > 1000 and int(test[2]) > 20:
                            print '[+][+][+][+][+][+][+][+][+][+][+]'
                            print 'PATH TRAVERSAL FOUND'
                            print 'PATH: ' + self.path
                            print 'REQUEST: ' + self.reqtype
                            print 'PARAM: ' + self.param_exploited
                            print 'Content-Length Payload Request: ' + str(int(test[2]))
                            print 'Content-Length Original Request: ' + self.original_request.headers.get(
                                'content-length')
                            print 'ON: ' + test[1]

                else:
                    if self.reqtype == 'GET':
                        for pay in self.windows_payloads:
                            test = PathTraversal.get_call_test_reply(self.aux_params_to_rebuild_req[0],
                                                                             self.aux_params_to_rebuild_req[1],
                                                                             self.aux_params_to_rebuild_req[2],
                                                                             self.aux_params_to_rebuild_req[3],
                                                                             pay, self.aux_params_to_rebuild_req[4],
                                                                             self.aux_params_to_rebuild_req[5],
                                                                             self.aux_params_to_rebuild_req[6])
                            time.sleep(self.delay)
                            if test[0] == True and abs(int(test[2]) - int(
                                    self.original_request.headers.get('content-length'))) > 1000 and int(test[2]) > 20:
                                print '[+][+][+][+][+][+][+][+][+][+][+]'
                                print 'PATH TRAVERSAL FOUND'
                                print 'PATH: ' + self.path
                                print 'REQUEST: ' + self.reqtype
                                print 'PARAM: ' + self.param_exploited
                                print 'Content-Length Payload Request: ' + str(int(test[2]))
                                print 'Content-Length Original Request: ' + self.original_request.headers.get(
                                    'content-length')
                                print 'ON: ' + test[1]
        print '--------------------------------------------------------------------------------------------------------'