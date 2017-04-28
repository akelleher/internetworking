#!/usr/bin/env python

import time, BaseHTTPServer, os, sys, datetime, re
from subprocess import check_output

PORT_NUMBER = 80

#---------------------------------------------------------------------------------------------
# FUNCTION DEFINITIONS
#---------------------------------------------------------------------------------------------

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/csv")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/csv")
        s.end_headers()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Get current timestamp
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        out = check_output(['df', '-h', '/'])
        out = out.decode('utf-8')
        out = out.split(' ')
        usage = out[25]
        
        iwlist =  check_output(['iwlist', 'wlan0', 'scan']).splitlines()
        temp = check_output(['cat', '/sys/class/thermal/thermal_zone0/temp'])
        temp = temp.decode('utf-8')
        temp =int(temp)/1000
        networks = ""
        for line in iwlist:
            if re.search("ESSID:", line):
		networks+='"'
                networks+=(line.strip())[7:]
                networks+=' '
        s.wfile.write("timestamp,hostname,cpuTemp,diskUsage,networks\n%s,%s,%s,%s,%s\n" %(str(timestamp), hostname,temp, usage, networks))
        #print ("Temperature is %.2f" % temp)


# --------------------------------------------------------------------------
# MAIN PROGRAM BEGINS HERE
# --------------------------------------------------------------------------

PORT_NUMBER = 80 # Standard HTTP
  


if __name__ == '__main__':

    hostname = check_output(['cat', '/etc/hostname']) # Pull system hostname
    hostname = (hostname.decode('utf-8')).strip()   # Convert to text and strip whitespace

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(('', PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (hostname, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(('', PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (hostname, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (hostname, PORT_NUMBER)
