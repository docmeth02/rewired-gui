import platform
from Tkinter import END
from time import sleep
from os.path import expanduser, join, exists
from os import mkdir, sep
from shutil import copyfile, copytree
from logging import getLogger
from rewiredserver.includes import wiredfunctions, wireddb, wiredcertificate


def getPlatformString(parent):
    system = "Unknown OS"
    version = "Unknown Version"
    system = platform.system()

    if system == 'Darwin':
        system = "OS X"
        version = platform.mac_ver()[0]
    if system == 'Linux':
        try:
            distro = platform.linux_distribution()
            version = distro[0] + " " + distro[1]
        except:
            version = "None"
    if system == 'Windows':
        version = platform.win32_ver()[0]
    return system + " " + version + " - Python " + platform.python_version()


def checkPlatform(name):
    if name.upper() == str(platform.system()).upper():
        return 1
    return 0


def initConfig(parent):
    home = False
    config = 0
    home = expanduser("~")
    if not home:
        debugLog(parent, "Unable to find user home dir!")
        return 0
    debugLog(parent, "User Home is: " + home)
    configdir = join(home, ".rewired")
    configfile = join(configdir, "server.conf")
    debugLog(parent, "Config Folder is: " + configdir)
    debugLog(parent, "Config File is: " + configfile)
    if not exists(configdir):
        debugLog(parent, "Creating the configdir")
        try:
            mkdir(configdir)
        except:
            debugLog(parent, "failed to create the configdir!")
            return 0
    else:
        debugLog(parent, "ConfigDir already exists")
    if not exists(join(configdir, 'cert.pem')):
        from socket import gethostname
        if not createCert(join(configdir, 'cert.pem'), gethostname()):
            debugLog(parent, "failed to install default cert!")
    if not exists(join(configdir, 'banner.png')):
        if not saveCopy('data/banner.png', join(configdir, 'banner.png')):
            debugLog(parent, "failed to install default Banner!")
    if not exists(join(configdir, 'server.conf')):
        debugLog(parent, "creating new config file")
        config = wiredfunctions.loadConfig(configfile)
        config['cert'] = join(configdir, 'cert.pem')
        config['serverBanner'] = join(configdir, 'banner.png')
        config['logFile'] = join(configdir, 'server.log')
        config['dbFile'] = join(configdir, 'rewiredDB.db')
        if checkPlatform("Darwin"):
            config['fileRoot'] = "/Users/Shared/Rewired Files"
        if checkPlatform("Linux"):
            config['fileRoot'] = "/opt/rewired/Files"
        if checkPlatform("Windows"):
            config['fileRoot'] = join(home + sep + "Rewired Files")
        config['serverPidFile'] = join(configdir, "server.pid")
        rewriteConfig(config)
    else:
        config = wiredfunctions.loadConfig(configfile)
    parent.configFile = configfile
    if config['trackerDNS'] == '""':
        config['trackerDNS'] = ""
    if not exists(config['dbFile']):
        file = open(config['dbFile'], 'w')
        file.close()
    if not exists(config['fileRoot']):
        try:
            copytree("data/files", config['fileRoot'])
        except:
            debugLog(parent, "Failed to create default File Root")
    parent.logger = getLogger("none")
    debugLog(parent, "initConfig done")
    if not exists(config['logFile']):
        file = open(config['logFile'], "w")
        file.write("Blank Logfile\n")
        file.close()
    return config


def loadData(parent, type):
    db = wireddb.wiredDB(parent.config, parent.logger)
    if not int(type):
        return db.loadGroups()
    return db.loadUsers()


def updateData(parent, data, type):
    db = wireddb.wiredDB(parent.config, parent.logger)
    if not db.updateElement(data, type):
        return 0
    return 1


def deleteData(parent, name, type):
    db = wireddb.wiredDB(parent.config, parent.logger)
    if not db.deleteElement(name, type):
        return 0
    return 1


def rewriteConfig(config):
    try:
        version = str(config['appVersion'])
        name = str(config.pop('appName'))
        config.pop('appVersion')
        config.pop('appName')
        config.pop('banner')
        config.pop('serverStarted')  # this will fail when server has not been run yet
    except KeyError:
        pass
    try:
        config['serverDesc'] = config['serverDesc'].encode('UTF-8')
        config['serverName'] = config['serverName'].encode('UTF-8')
    except:
        pass
    config.write()
    config['appVersion'] = version
    config['appName'] = name
    return 1


def saveCopy(src, dst):
    try:
        copyfile(src, dst)
    except:
        return 0
    return 1


def getCertName(certpath):
    check = wiredcertificate.reWiredCertificate("")
    check.loadPem(certpath)
    return check.getCommonName()


def createCert(certpath, cname):
    try:
        cert = wiredcertificate.reWiredCertificate(str(cname))
        cert.createSignedCert()
        cert.safeAsPem(str(certpath))
    except:
        return 0
    return 1


def debugLog(parent, log):
    if parent.debug:
        try:
            parent.debugbox.insert("1.0", log + "\n")
        except:
            return 0
    return 1
