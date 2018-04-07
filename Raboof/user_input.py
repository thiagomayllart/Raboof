import sys
import HTTPRequester
import PayloadGenerator

requests_location = None
option = None
max_threads = None
delay = None

def present():
    global option
    if option == 'pp':
        print '[+] Testing for HTTP Parameter Pollution '
        print '[+] FILE: ' + str(requests_location)
        print '[+] Threads: ' + str(max_threads)
        print '[+] Delay between requests: ' + str(delay)
        print '-------------------------------------------------------------------------------------------------------'

def usage():
    help = "You must use Burp Suite to get a file with all the requests you want to probe \n" \
           "1) -f -> file location \n" \
           "2) -o -> option. Use 's' to test for soap injection or 'p' to test for parameter polution \n" \
           "3) -th -> quantity of threads" \
           "4) -dl -> delay\n"
    return help


def setOptions(arguments1):
    global requests_location, option, max_threads, delay
    arguments = ' '.join(arguments1)
    requests_location = arguments.split("-f", 1)[1].split(" ")[1]
    option = arguments.split("-o", 1)[1].split(" ")[1]
    if '-th' not in arguments:
        max_threads = 30
    else:
        max_threads = arguments.split("-th", 1)[1].split(" ")[1]
    if '-dl' not in arguments:
        delay = 0
    else:
        delay = arguments.split("-dl", 1)[1].split(" ")[1]


def get_params():
    global requests_location, option
    params = [requests_location, option]
    return params

def main():
    global requests_location, option, max_threads, delay
    try:
        setOptions(sys.argv[1:])
    except Exception as msg:
        print usage()
        sys.exit()
    HTTPRequester.set_file(requests_location)
    HTTPRequester.set_params(option, max_threads, delay)
    present()
    HTTPRequester.HTTP_request()

main()