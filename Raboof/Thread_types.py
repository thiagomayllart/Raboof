import HTTPRequester
from threading import Thread

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