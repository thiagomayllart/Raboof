import sys
import HTTPRequester
import PayloadGenerator

requests_location = None
option = None
max_threads = None
delay = None
os = None
dt = 0

def present():
    global option, os, dt
    if option == 'so':
        print '[+] Testing for Soap Injection: '

    if option == 'pp':
        print '[+] Testing for HTTP Parameter Pollution '

    if option == 'ti':
        print '[+] Testing for Template Injection '

    if option == 'sr':
        print '[+] Testing for Serializing/Deserializing Vulnerability '

    if option == 'op':
        print '[+] Testing for Oracle Padding Vulnerability '

    print '[+] FILE: ' + str(requests_location)
    print '[+] Threads: ' + str(max_threads)
    print '[+] Delay between requests: ' + str(delay)
    print '-------------------------------------------------------------------------------------------------------'


def usage():
    help = "You must use Burp Suite to get a file with all the requests you want to probe \n" \
           "1) -f -> file location \n" \
           "2) -o -> option. Use 'so' to test for soap injection or 'pp' to test for parameter polution \n" \
           "3) -th -> quantity of threads" \
           "4) -dl -> delay\n"
    return help


def setOptions(arguments1):
    global requests_location, option, max_threads, delay, os
    arguments = ' '.join(arguments1)
    requests_location = arguments.split("-f", 1)[1].split(" ")[1]
    option = arguments.split("-o", 1)[1].split(" ")[1]
    if '-th' not in arguments:
        max_threads = 1
    else:
        max_threads = int(arguments.split("-th", 1)[1].split(" ")[1])
    if '-dl' not in arguments:
        delay = 0
    else:
        delay = arguments.split("-dl", 1)[1].split(" ")[1]


def get_params():
    global requests_location, option
    params = [requests_location, option]
    return params

def main():
    global requests_location, option, max_threads, delay, os, dt
    try:
        setOptions(sys.argv[1:])
    except Exception as msg:
        print usage()
        sys.exit()
    present()
    HTTPRequester.set_file(requests_location)
    HTTPRequester.set_params(option, max_threads, delay, os, int(dt))
    HTTPRequester.HTTP_request()

main()