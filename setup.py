# Features available at http://studiotech.tk/projects/SimpleBukkit/details.txt

import sys, os, datetime, time

class SimpleBukkitSetup:
    
    def __init__(self):
        now = datetime.datetime.now()
        timestamp = now.strftime("%I-%H-%Y-%m-%d")
        self.config = {}
        self.config["logfile"] = timestamp
        if os.path.exists("Logs") == True and os.path.isdir("Logs") == True:
            self.logFile = open("Logs/" + timestamp + ".txt", "w")
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

        if os.path.exists("server.py") == False or os.path.isifile("server.py") == False:
            self.Log("Could not find server.py - Aborting!",3)

            time.sleep(5)
            
            sys.exit(1)

        
        if os.path.exists("allowed-ips.txt") == False or os.path.isfile("allowed-ips.txt") == False:
            self.Log("Could not find allowed-ips.txt",2)
            tempFile = open("allowed-ips.txt","w")
            tempFile.close()

        if os.path.exists("config.txt") == False or os.path.isfile("config.txt") == False:
            self.Log("Could not find main configuration file!",2)
            self.Log("Created new configuration file.",1)
            tempFile = open("config.txt","w")
            tempFile.write("whitelisted: off")
            tempFile.write("port: 25564")
            tempFile.close()
        
        self.Log("All files accounted for.",1)
        self.setUpConfig()
        
    def setUpConfig(self):
        
        self.Log("Configuring web server...",1)
        
        configFile = open("config.txt","r")
        contents = configFile.readlines()

        if contents[0] == "whitelisted: on":
            self.config["whitelist"] = "on"
            ipFile = open("allowed-ips.txt","r")
            self.config["allowed-ips"] = ipFile.readlines()
            ipFile.close()
        else:
            self.Log("For more security, turn on whitelist.",2)

        if contents[1][0:5] == "port:":
            self.config["port"] = contents[1][5:]
            self.Log("Setting port to %s." % self.config['port'],2)
        else:
            self.config["port"] = "25564"
            self.Log("No port found; setting to default (25564)",2)

        self.Log("Configuration complete.",1)

        self.Log("Handing process over to server.py",2)

        os.system("python server.py %s" % self.config)
        
        sys.exit()
   

    

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
        
        

SimpleBukkitSetup = SimpleBukkitSetup()
