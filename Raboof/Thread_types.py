import HTTPRequester
from threading import Thread
import time
import zlib
import base64
import sys
import json
from dicttoxml import dicttoxml
import jellyfish
import urllib2

class Threadxxe(Thread):

    def __init__(self, path, headers, payloadslist, params, original_request, reqtype):
        Thread.__init__(self)
        self.path = path
        self.headers = headers
        self.original_request = original_request #original_request is just the response, without read() called
        self.reqtype = reqtype
        self.html = self.original_request.read()
        self.params = params
        self.payloadslist = payloadslist


        if self.original_request.headers.get('Content-Encoding') != None:
            if 'gzip' in self.original_request.headers.get('Content-Encoding'):
                self.html = zlib.decompress(self.html, 16 + zlib.MAX_WBITS)

    def run(self):
        new_headers = self.headers
        new_path = self.path
        new_params = self.params
        if 'xml' in self.headers.get('Content-type'):
            print '\033[92m [+] FOUND XML Request Type: '
            print '[+] Manipulate it GOGOGO!!\033[0m'
            print '[+] Request type: ' + self.reqtype
            if self.reqtype == 'GET':
                print '[+] Path: ' + self.path + self.params
            else:
                print '[+] Path: ' + self.path
            print "[+] HEADERS: "
            for x in self.headers:
                print x + ': ' + self.headers.get(x)

        #test case 1: convert to xml
        code_status_org = self.original_request.getcode()
        code_status_org = list(code_status_org)
        req_test = ""
        found_anything = 0
        found_xxe = 0
        if code_status_org[0] == '2' or code_status_org[0] == '3':
            new_headers.update({'Content-type': 'application/xml'})
            if 'POST' in self.reqtype:
                resp_test = HTTPRequester.post_call(new_path, new_params, new_headers)
                code_status_test = req_test.getcode()
                code_status_test = list(code_status_test)
                resp_test_html = req_test.read()
                if resp_test.headers.get('Content-Encoding') != None:
                    if 'gzip' in resp_test.headers.get('Content-Encoding'):
                        resp_test_html = zlib.decompress(resp_test_html, 16 + zlib.MAX_WBITS)
                if code_status_test[0] == '5':
                    if "XML" in resp_test_html:
                        print '\033[33m [+] Possible XML Parsing ERROR - Content-Type to application/xml'
                        print 'Check if XML is really supported \033[0m'
                        found_anything = 1

                try:
                    new_params = dicttoxml(json.loads(self.params), attr_type=False)
                    resp_test2 = HTTPRequester.post_call(new_path, new_params, new_headers)

                except Exception as msg:
                    #not json
                    new_dict = {}
                    new_params = new_params.split("&")
                    for var_val in new_params:
                        var, val = var_val.split("=")
                        new_dict[var] = val
                    new_params = dicttoxml(new_dict)
                    resp_test2 = HTTPRequester.post_call(new_path, new_params, new_headers)

                if self.original_request.getcode() == resp_test2.code():
                    # analyze similarity
                    resp_test2_html = resp_test2.read()
                    if 'gzip' in resp_test2.headers.get('Content-Encoding'):
                        resp_test2_html = zlib.decompress(self.html, 16 + zlib.MAX_WBITS)
                    similarity_index = jellyfish.jaro_distance(self.html, resp_test2_html)

                    # YOU CAN TUNE THE SIMILARITY INDEX - IT COMPARES HOW SIMILAR THE HTML RESPONSES ARE
                    if similarity_index > 0.89:
                        found_xxe = 1
                        print '\033[92m [+] Point of XXE FOUND'
                        print 'Manipulate the parameters with external entities\033[0m'
                        print "[+] PATH: " + new_path
                        print "[+] REQUEST TYPE: " + self.reqtype
                        print '[+] POST PARAMETERS: ' + new_params
                        print "\033[92m [+] HEADERS: "
                        for x in new_headers:
                            print x + ': ' + new_headers.get(x)
                        print "\033[0m ----------------------------------------------------------------------------------------------\n"

            if 'GET' in self.reqtype:
                resp_test = HTTPRequester.get_call(new_path+new_params, new_headers)
                code_status_test = req_test.getcode()
                code_status_test = list(code_status_test)
                resp_test_html = req_test.read()
                if resp_test.headers.get('Content-Encoding') != None:
                    if 'gzip' in resp_test.headers.get('Content-Encoding'):
                        resp_test_html = zlib.decompress(resp_test_html, 16 + zlib.MAX_WBITS)
                if code_status_test[0] == '5':
                    if "XML" in resp_test_html or "Exception" in resp_test2_html:
                        print '\033[33m [+] Possible XML Parsing ERROR\033[0m - \033[1m Content-Type set to application/xml \033[0m'
                        print '\033[33mCheck if XML is really supported \033[0m'
                        found_anything = 1
                # not json
                new_dict = {}
                new_params = new_params.split("&")
                for var_val in new_params:
                    var, val = var_val.split("=")
                    new_dict[var] = val
                new_params = dicttoxml(new_dict)
                resp_test2 = HTTPRequester.post_call(new_path, new_params, new_headers)

                if self.original_request.getcode() == resp_test2.code():
                    # analyze similarity
                    resp_test2_html = resp_test2.read()
                    if 'gzip' in resp_test2.headers.get('Content-Encoding'):
                        resp_test2_html = zlib.decompress(self.html, 16 + zlib.MAX_WBITS)
                    similarity_index = jellyfish.jaro_distance(self.html, resp_test2_html)

                    # YOU CAN TUNE THE SIMILARITY INDEX - IT COMPARES HOW SIMILAR THE HTML RESPONSES ARE
                    if similarity_index > 0.89:
                        found_xxe = 1
                        print '\033[92m [+] Point of XXE FOUND'
                        print 'Manipulate the parameters with external entities\033[0m'
                        print "[+] PATH: " + new_path
                        print "[+] REQUEST TYPE: " + self.reqtype
                        print '[+] POST PARAMETERS: ' + new_params
                        print "\033[92m [+] HEADERS: "
                        for x in new_headers:
                            print x + ': ' + new_headers.get(x)
                        print "\033[0m ----------------------------------------------------------------------------------------------\n"

                    else:
                        if "XML" in resp_test2_html or "Exception" in resp_test2_html:
                            print '\033[33m [+] Possible XML Parsing ERROR\033[0m - \033[1mForged XML Request \033[0m'
                            print '\033[33mCheck if XML is really supported \033[0m'

        if found_anything == 1 and found_xxe == 0:
            if 'POST' in self.reqtype:
                print "[+] PATH: " + self.path
                print "[+] REQUEST TYPE: " + self.reqtype
                print '[+] POST PARAMETERS: ' + self.params
                print "[+] HEADERS: "
                for x in self.headers:
                    print x + ': ' + self.headers.get(x)
                print "[+] RESPONSE: "
                print resp_test2_html
            if 'GET' in self.reqtype:
                print "[+] PATH: " + self.path + self.params
                print "[+] REQUEST TYPE: " + self.reqtype
                print "[+] HEADERS: "
                for x in self.headers:
                    print x + ': ' + self.headers.get(x)
                print "[+] RESPONSE: "
                print resp_test2_html
            print "----------------------------------------------------------------------------------------------\n"

class Threadop(Thread):

    def __init__(self, path, headers, payloadslist, params, original_request, reqtype):
        Thread.__init__(self)
        self.path = path
        self.headers = headers
        self.original_request = original_request
        self.reqtype = reqtype
        self.html = self.original_request.read()
        self.params = params
        self.payloadslist = payloadslist

        self.found_on_cookie = {}

        if self.original_request.headers.get('Content-Encoding') != None:
            if 'gzip' in self.original_request.headers.get('Content-Encoding'):
                self.html = zlib.decompress(self.html, 16 + zlib.MAX_WBITS)


    def run(self):
        #get the cookies
        found_anything = 0
        cookies = self.headers.get('Cookie')
        cookies = cookies.split(";")
        for cookie in cookies:
            multiple = 0
            variable, value = cookie.split("=", 1)
            original_value = value
            while self.isBase64(value) and value != "" and value != None:
                value = base64.b64decode(value)
            hex_string = self.get_hex(value)
            bytesize = self.get_byte_size(hex_string)
            if bytesize != 0:
                if bytesize % 16 == 0:
                    found_anything = 1
                    multiple = 16
                else:
                    if bytesize % 8 == 0:
                        found_anything = 1
                        multiple = 8
                if multiple == 16 or multiple == 8:
                    original_value = original_value+';\033[0m \033[94mmultiple of '+str(multiple)
                    self.found_on_cookie[cookie] = original_value
        if found_anything == 1:
            print "[+] POSSIBLE COOKIE USING CBC CIPHER FOUND"
            print "[+] PATH: " + self.path
            print "[+] REQUEST TYPE: " + self.reqtype
            if self.reqtype == 'POST':
                print '[+] POST PARAMETERS: ' + self.params
            print "[+] HEADERS: "
            for x in self.headers:
                print x + ': ' + self.headers.get(x)
            print "[+] Printing Possibly Vulnerable Cookies: "
            for i,j in self.found_on_cookie.items():
                print("\033[92m "+i+": "+j+"\n \033[0m")

            print "----------------------------------------------------------------------------------------------\n"

    def get_hex(selfs,s):
        hex = "".join("{:02x}".format(ord(c)) for c in s)
        return hex

    def get_byte_size(self, s):
        return len(s)/2

    def isBase64(self, s):
        try:
            return base64.b64encode(base64.b64decode(s)) == s
        except Exception:
            return False

class Threadsr(Thread):


    def __init__(self, path, headers, payloadslist, params, original_request, reqtype):
        Thread.__init__(self)
        self.path = path
        self.headers = headers
        self.original_request = original_request
        self.reqtype = reqtype
        self.html = self.original_request.read()
        self.params = params
        self.payloadslist = payloadslist

        self.search_on_response_java = payloadslist[0]
        self.search_on_response_csharp = payloadslist[1]
        self.search_on_header_response = payloadslist[2]
        self.search_on_content_type = payloadslist[3]
        self.search_on_response = payloadslist[4]

        if self.original_request.headers.get('Content-Encoding') != None:
            if 'gzip' in self.original_request.headers.get('Content-Encoding'):
                self.html = zlib.decompress(self.html, 16 + zlib.MAX_WBITS)


    def define_tests(self, payloadslist):
        global search_on_response_java, search_on_response_csharp, search_on_header_response, search_on_content_type, search_on_response
        search_on_response_java = payloadslist[0]
        search_on_response_csharp = payloadslist[1]
        search_on_header_response = payloadslist[2]
        search_on_content_type = payloadslist[3]
        search_on_response = payloadslist[4]

    def run(self):
        #Analyzing response:
        found_on_response = []
        found_on_request_get = []
        found_on_request_post = []
        found_on_response_header = []
        found_on_request_header = []
        found_on_content_type_req = []
        found_on_content_type_resp = []

        # Analyzing response:
        for test in self.search_on_response_java:
            if test in self.html:
                found_on_response.append(test)
        for test in self.search_on_response_csharp:
            if test in self.html:
                found_on_response.append(test)
        for test in self.search_on_header_response:
            if test in self.html:
                found_on_response.append(test)
        for test in self.search_on_response:
            if test in self.html:
                found_on_response.append(test)

        #Analyzing response_headers:
        for test in self.search_on_header_response:
            for i,j in self.original_request.headers.items():
                if test in j:
                    found_on_response_header.append(test)

        #Analyzing response header content-type:
        if self.original_request.headers.get('Content-Type') != None:
            for test in self.search_on_content_type:
                if test in self.original_request.headers.get('Content-Type'):
                    found_on_content_type_resp.append(test)

        # Analyzing request params:
        if self.reqtype == 'GET':
            for test in self.search_on_header_response:
                if test in self.path:
                    found_on_request_get.append(test)

        if self.reqtype == 'POST':
            for test in self.search_on_header_response:
                if test in self.params:
                    found_on_request_post.append(test)

        #Analyzing request headers:
        for test in self.search_on_header_response:
            for i,j in self.headers.items():
                if test in j:
                    found_on_request_header.append(test)

        #Analyzing request Content-Type:
        if self.headers.get('Content-Type') != None:
            for test in self.search_on_content_type:
                if test in self.headers.get('Content-Type'):
                    found_on_content_type_req.append(test)

        found_anything = 0
        if self.reqtype == 'GET':
            if len(found_on_request_get) > 0:
                found_anything = 1
                print '[+] Found Serialization Pattern on GET REQUEST Parameters: '
                print '[+] Patterns: '
                for i in found_on_request_get:
                    print i
            if len(found_on_request_header) > 0:
                found_anything = 1
                print '[+] Found Serialization Pattern on GET REQUEST Header: '
                print '[+] Patterns: '
                for i in found_on_request_header:
                    print i
            if len(found_on_content_type_req) > 0:
                found_anything = 1
                print '[+] Found Serialization Pattern on GET REQUEST Content-Type: '
                print '[+] Patterns: '
                for i in found_on_content_type_req:
                    print i

        if self.reqtype == 'POST':
            if len(found_on_request_post) > 0:
                found_anything = 1
                print '[+] Found Serialization Pattern on POST DATA Parameters: '
                print '[+] Patterns: '
                for i in found_on_request_post:
                    print i
            if len(found_on_request_header) > 0:
                found_anything = 1
                print '[+] Found Serialization Pattern on POST REQUEST Header: '
                print '[+] Patterns: '
                for i in found_on_request_header:
                    print i
            if len(found_on_content_type_req) > 0:
                found_anything = 1
                print '[+] Found Serialization Pattern on POST REQUEST Content-Type: '
                print '[+] Patterns: '
                for i in found_on_content_type_req:
                    print i


        if len(found_on_response) > 0:
            found_anything = 1
            print '[+] Found Serialization Pattern on HTTP Response: '
            print '[+] Patterns: '
            for i in found_on_response:
                print i

        if len(found_on_response_header) > 0:
            found_anything = 1
            print '[+] Found Serialization Pattern on HTTP Response Header: '
            print '[+] Patterns: '
            for i in found_on_response_header:
                print i

        if len(found_on_content_type_resp):
            found_anything = 1
            print '[+] Found Serialization Pattern on HTTP Response Content-Type: '
            print '[+] Patterns: '
            for i in found_on_content_type_resp:
                print i

        if found_anything == 1:
            print '[+] REQUEST TYPE: ' + self.reqtype
            print '[+] PATH: ' + self.path
            for x in self.headers:
                print x + ': ' + self.headers.get(x)
            if self.reqtype == 'POST':
                print '[+] DATA: ' + self.params

            print "----------------------------------------------------------------------------------------------\n"

class Threadti(Thread):
    def __init__(self, path, headers, data_pay, original_request, param_exploited, reqtype, pay_path, template_inj_type_test, list_regions):
        Thread.__init__(self)
        if reqtype == 'POST':
            self.pay_response = HTTPRequester.post_call(path, data_pay, headers)
        else:
            self.pay_response = HTTPRequester.get_call(pay_path, headers)
        self.path = path
        self.headers = headers
        self.original_request = original_request
        self.param_exploited = param_exploited
        self.data_pay = data_pay
        self.template_inj_test = template_inj_type_test
        self.reqtype = reqtype
        self.list_regions = list_regions
        self.html = self.pay_response.read()
        if self.pay_response.headers.get('Content-Encoding') != None:
            if 'gzip' in self.pay_response.headers.get('Content-Encoding'):
                self.html = zlib.decompress(self.html, 16 + zlib.MAX_WBITS)

    def run(self):
        for regions in self.list_regions:
                out_payload = HTTPRequester.find_between(self.html, regions[0], regions[1])
                if self.template_inj_test == 0:
                    if '49' in out_payload:
                        print '[+] POINT OF TEMPLATE INJECTION FOUND'
                        print '[+] LOCATION: ' + self.param_exploited
                        print '[+] OUTPUT RESULT: ' + out_payload
                        print '[+] REQUEST TYPE: ' + self.reqtype
                        print '[+] PRINTING REQUEST: '
                        print self.path
                        print self.data_pay
                        for x in self.headers:
                            print x + ': ' + self.headers.get(x)
                        print "----------------------------------------------------------------------------------------------\n"
                if self.template_inj_test == 1:
                    if '7777777' in out_payload:
                        print '[+] POINT OF TEMPLATE INJECTION FOUND'
                        print '[+] LOCATION: ' + self.param_exploited
                        print '[+] OUTPUT RESULT: ' + out_payload
                        print '[+] REQUEST TYPE: ' + self.reqtype
                        print '[+] PRINTING REQUEST: '
                        print self.path
                        print self.data_pay
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
