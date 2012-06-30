# Features available at http://studiotech.tk/projects/SimpleBukkit/details.txt

# p = subprocess.popen
# a = subprocess.popen(["python","index.html.py",str(p)])
# In the other file
# b = os.fdopen(int(sys.arv[2]))
# b.readline() or b.write()

import sys, os, datetime, time, socket, subprocess

logFile = None

config = None

class Setup:

    def __init__(self):
        
        now = datetime.datetime.now()
        timestamp = now.strftime("%I-%H-%Y-%m-%d")
        global logFile
        logFile = "Logs/" + timestamp + ".txt"
        self.config = {}
        self.config["logfile"] = timestamp
        self.Log("Created new log file.", 1)
        else:
            os.makedirs("Logs")
            self.logFile = open("Logs/" + timestamp + ".txt", "w")
            self.Log("Logs directory did not exist, so new one was created.", 2)
            self.Log("Created new log file.", 1)
            
        self.Log("Executing startup routine...",1)
        self.checkFiles()

    def checkFiles(self):
        
        self.Log("Checking for required files.",1)
        
        if os.path.exists("allowed-ips.txt") == False or os.path.isfile("allowed-ips.txt") == False:
            self.Log("Could not find allowed-ips.txt",2)
            tempFile = open("allowed-ips.txt","w")
            tempFile.close()

        if os.path.exists("config.txt") == False or os.path.isfile("config.txt") == False:
            self.Log("Could not find main configuration file!",2)
            self.Log("Created new configuration file.",1)
            tempFile = open("config.txt","w")
            tempFile.write("whitelisted: off\n")
            tempFile.write("port: 25564\n")
            tempFile.write("timeout: 3\n")
            tempFile.close()

        if os.path.exists("htmlfiles") == False or os.path.isdir("htmlfiles") == False:
            self.Log("Could not find htmlfiles folder!",3)

        
        self.Log("All files accounted for.",1)
        self.setUpConfig()
        
    def setUpConfig(self):
        
        self.Log("Configuring web server...",1)
        
        configFile = open("config.txt","r")
        contents = configFile.readlines()

        if contents[0][0:15] == "whitelisted: on":
            
            self.config["whitelisted"] = True
            
            ipFile = open("allowed-ips.txt","r")

            if len(ipFile.readlines()) >= 2:

                self.config["allowed-ips"] = ipFile.readlines()

                ipFile.close()

            else:

                self.config["whitelisted"] = False

                self.Log("No IP addresses defined in allowed-ips.txt. Ignoring whitelist.",2)
                
        else:
            self.Log("For more security, turn on whitelist.",2)

        if contents[1][0:5] == "port:":

            if (int(contents[1][5:])):
                self.config["port"] = contents[1][5:].replace(' ', '')
                self.Log("Setting port to %s" % self.config['port'],2)

            else:
                
                self.Log("Port must be an integer.",3)

                self.config["port"] = "25564"
                
                self.Log("No port found; setting to default (25564)",2)
        else:
            self.config["port"] = "25564"
                
            self.Log("No port found; setting to default (25564)",2)


        if contents[2][0:8] == "timeout:":

            if (int(contents[2][8:])):
                
                self.config["timeout"] = int(contents[2][8:].replace(' ', ''))
                
                self.Log("Setting timeout to %s" % self.config['timeout'],2)

            else:
                
                self.Log("Timeout must be an integer.",3)

                self.config["timeout"] = "3"
                
                self.Log("No timeout option found; setting to default (3 seconds)",2)
        else:
            
            self.config["timeout"] = "3"
                
            self.Log("No timeout option found; setting to default (3 seconds)",2)

            

        self.Log("== Configuration complete. ==",2)


        global config

        config = self.config
        
        self.logFile.close()

    def Log(self,text,typeoftext):
            now = datetime.datetime.now()
            timestamp = now.strftime("<%I:%M>")
            if typeoftext == 1:
                prefix = "[INFO] "
            if typeoftext == 2:
                prefix = "[NOTIFY] "
            if typeoftext == 3:
                prefix = "[ERROR] "
            stringToWrite = timestamp + " " + prefix + text
            self.logFile.write(stringToWrite + "\n")
            print(stringToWrite)
            if typeoftext == 3:
                self.logFile.close()
                sys.exit(1)
        

class WebServer:

    def __init__(self,logfile,config):

        self.logfile = logfile
        self.logFile = open(logfile,"a")
        self.config = config
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.Log("Socket created.",1)

        self.mainLoop()

    def mainLoop(self):


        host = socket.gethostname()
        ip = socket.gethostbyname(host)

        def validate_port():

            try:
                
                self.sock.bind((ip,int(self.config["port"])))

            except socket.error:

                self.Log("Failed to bind port.",2)
                self.config["port"] = raw_input("Please try another: ")
                validate_port()

        validate_port()

        self.Log("Socket bound to port %s." % self.config["port"], 2)
        
        self.sock.listen(1)

        self.Log("Now accepting connections.",1)

        self.Log("Entering main server loop.",1)

        while True:
            
            sock, addr = self.sock.accept()

            self.Log("Incoming connection from %s" % str(addr[0]),2)
            

            handler = handle_connection(sock,addr,self.logfile)


    def Log(self,text,typeoftext):
            now = datetime.datetime.now()
            timestamp = now.strftime("<%I:%M>")
            if typeoftext == 1:
                prefix = "[INFO] "
            if typeoftext == 2:
                prefix = "[NOTIFY] "
            if typeoftext == 3:
                prefix = "[ERROR] "
            stringToWrite = timestamp + " " + prefix + text
            self.logFile.write(stringToWrite + "\n")
            print(stringToWrite)
            if typeoftext == 3:
                self.logFile.close()
                sys.exit(1)


class handle_connection:

    def __init__(self,sock,addr,logfile):
      
      self.logFile = open(logfile,"a")
      self.config = config
      self.conn = sock
      self.ip = str(addr[0])
      self.com = self.conn.makefile('rw', 0)

      self.isInWhitelist()

    def isInWhitelist(self):

        if self.config["whitelisted"] == True:

            if self.ip in self.config["allowed-ips"]:

                self.read_request()

            else:

                error401 = open("htmlfiles/401.html", "r")

                error401contents = error401.read()

                error401.close()

                length = len(error401contents)

                self.com.write("HTTP/1.1 403 Forbidden\n")
                self.com.write("Server: SimpleBukkit Web Server\n")
                self.com.write("Content-Length: %s\n" % length)
                self.com.write("Content-Type: text/html\n")
                self.com.write("\n")

                self.com.write(error401contents)

                time.sleep(self.config["timeout"])

                self.Log("Sent 403 Forbidden to  %s" % self.ip,1)

                self.Log("Ended connection with %s" % self.ip,2)

                time.sleep(self.config["timeout"])
                    
                self.com.close()
                self.conn.close()

        else:

            self.read_request()

        
            

    def read_request(self):

        
        line = self.com.readline().strip()
        line = line.split(" ")

        print line

        if line[0] == "GET" or line[0] == "POST":

            fileToGet = line[1][1:]

            if line[1] == "/":
                fileToGet = "index.html"

            if ".html" in fileToGet:

                fileToGet = fileToGet + ".py"

            if os.path.exists("htmlfiles/%s" % fileToGet):

                if ".py" in fileToGet:

                    source = "test"

                    length = len(source)


                else:

                    reader = open("htmlfiles/%s" % fileToGet, "r")

                    source = reader.read()

                    length = len(reader)

                self.com.write("HTTP/1.1 200 OK\n")
                self.com.write("Connection: close\n")
                self.com.write("Server: SimpleBukkit Web Server\n")
                self.com.write("Content-Length: %s\n" % length)
                self.com.write("Content-Type: text/html\n")
                self.com.write("\n")

                self.com.write(source)

                self.Log("Served %s to %s" % (fileToGet, self.ip),1)

            else:

                self.Log("Unable to serve %s to %s: File doesn't exist." % (fileToGet, self.ip), 2)

                self.Log("Sending 404 error message to %s" % self.ip, 1)

                error404 = open("htmlfiles/404.html", "r")

                error404contents = error404.read()

                error404.close()

                length = len(error404contents)

                self.com.write("HTTP/1.1 404 Not Found\n")
                self.com.write("Connection: close\n")
                self.com.write("Server: SimpleBukkit Web Server\n")
                self.com.write("Content-Length: %s\n" % length)
                self.com.write("Content-Type: text/html\n")
                self.com.write("\n")

                self.com.write(error404contents)
            

            time.sleep(self.config["timeout"])

            self.Log("Ended connection with %s" % self.ip,2)
                
            self.com.close()
            self.conn.close()

            
    def Log(self,text,typeoftext):
            now = datetime.datetime.now()
            timestamp = now.strftime("<%I:%M>")
            if typeoftext == 1:
                prefix = "[INFO] "
            if typeoftext == 2:
                prefix = "[NOTIFY] "
            if typeoftext == 3:
                prefix = "[ERROR] "
            stringToWrite = timestamp + " " + prefix + text
            self.logFile.write(stringToWrite + "\n")
            print(stringToWrite)
            if typeoftext == 3:
                self.logFile.close()
                sys.exit(1)



    
Setup = Setup()
WebServer = WebServer(logFile,config)



