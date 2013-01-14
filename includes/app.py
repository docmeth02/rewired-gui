import Tkinter as tk
import ttk as ttk
from includes import statusframe, settingsframe, accountframe, advancedframe, guifunctions
import sys
import Queue
import threading
import time
import subprocess
import logging
from os import sep
from platform import python_version, system


class ThreadedApp:
    def __init__(self, master):
        self.lock = threading.Lock()
        self.master = master
        self.queue = Queue.Queue()
        self.gui = gui(self, master, self.queue)
        self.master.createcommand('exit', self.shutdownApp)  # osx
        self.master.protocol('exit', self.shutdownApp)  # osx too
        self.master.protocol('WM_DELETE_WINDOW', self.shutdownApp)
        self.running = 1
        self.serverInstance = 0
        self.serverthread = 0
        self.thread1 = threading.Thread(target=self.logWatcher)
        self.thread1.start()
        self.checkQueue()
        self.serverStatus()

    def shutdownApp(self):
        if self.serverInstance:
            self.stopServer()
        self.running = 0

    def checkQueue(self):
        self.gui.processIncoming()
        if not self.running:
            sys.exit(1)
        self.master.after(250, self.checkQueue)
        return 1

    def serverStatus(self):
        if not self.running:
            return 0  # we're about to quit
        if not self.serverthread:
            #Server appears not to be running
            self.gui.status.startbutton.config(state=tk.NORMAL)
            self.gui.status.stopbutton.config(state=tk.DISABLED)
            self.gui.status.restartbutton.config(state=tk.DISABLED)
            self.gui.status.statuslabel.config(text="re:wired Server is not running")
            self.gui.status.icon.config(image=self.gui.status.icon.imageoff)

        elif self.serverthread.is_alive():
            self.gui.status.startbutton.config(state=tk.DISABLED)
            self.gui.status.stopbutton.config(state=tk.NORMAL)
            self.gui.status.icon.config(image=self.gui.status.icon.imageon)
            self.gui.status.statuslabel.config(text="re:wired Server is running")
            self.gui.status.restartbutton.config(state=tk.NORMAL)
        else:
            self.gui.status.startbutton.config(state=tk.NORMAL)
            self.gui.status.stopbutton.config(state=tk.DISABLED)
            self.gui.status.restartbutton.config(state=tk.DISABLED)
            self.gui.status.statuslabel.config(text="re:wired Server is not running")
            self.gui.status.icon.config(image=self.gui.status.icon.imageoff)

        if self.running:
            threading.Timer(3, self.serverStatus).start()
        return 0

    def reStartServer(self):
        self.gui.status.startbutton.config(state=tk.DISABLED)
        self.gui.status.stopbutton.config(state=tk.DISABLED)
        self.gui.status.restartbutton.config(state=tk.DISABLED)
        self.stopServer()
        time.sleep(1)
        self.startServer()
        return 1

    def startServer(self):
        self.serverthread = threading.Thread(target=self.spawnServer)
        self.serverthread.start()
        return 1

    def stopServer(self):
        if self.serverInstance:
            #self.lock.acquire()
            self.serverInstance.keeprunning = 0
            #self.serverInstance.indexer.keepalive = 0
            #self.serverInstance.tracker.keepalive = 0
            #self.lock.release()
            self.serverInstance.serverShutdown("GUIQuit", None)
            self.logger = logging.getLogger("wiredServer")
            for ahandler in self.logger.handlers:
                try:
                    self.logger.removeHandler(ahandler)
                    ahandler.close()
                    logging.shutdown()
                    del(self.logger)
                except:
                    pass
                return 1
        return 0

    def spawnServer(self):
        try:
            from rewiredserver.includes import rewiredserver
            self.serverInstance = rewiredserver.reWiredServer(False, self.gui.configFile, True)
            self.serverInstance.initialize()
            self.serverInstance.main()
            self.serverInstance = 0
            self.gui.status.appendLog("Server Thread exited\n")
        except:
            return 0
        return 1

    def logWatcher(self):
        try:
            self.logfile = open(self.gui.config["logFile"])
            self.logfile.seek(-1, 2)
        except:
            self.queue.put("Error opening logfile\n")
            return 0
        while self.running:
            where = self.logfile.tell()
            line = self.logfile.readline()
            if not line:
                time.sleep(1)
                self.logfile.seek(where)
            else:
                self.queue.put(line)
        self.logfile.close()
        return 1


class gui:
    def __init__(self, parent, root, queue):
        self.parent = parent
        self.root = root
        self.queue = queue
        self.debug = False
        self.system = system()
        self.root.geometry("%dx%d+%d+%d" % (640, 480, 0, 0))
        self.root.minsize(640, 480)
        self.root.maxsize(640, 480)
        self.root.title('re:wired Server')
        print self.system
        if self.system == 'Windows':
            self.root.wm_iconbitmap('data' + sep + 're-wired.ico')
        if  self.system == 'Darwin':
            self.root.createcommand('tkAboutDialog', self.showabout)  # replace about dialog on osx
            #self.root.createcommand('::tk::mac::ShowPreferences', prefs)
            #Replace Default Menu (check for osx here)
            self.menubar = tk.Menu(self.root)
            self.apple = tk.Menu(self.menubar, tearoff=0)
            self.root.config(menu=self.apple)
        if self.debug:
            self.debug = tk.Toplevel()
            self.debug.geometry("%dx%d+%d+%d" % (480, 480, 650, 0))
            self.debug.title('Debug')
            self.debugbox = tk.Text(self.debug)
            self.debugbox.pack(expand=1, fill=tk.Y)

        #set up everything
        self.config = guifunctions.initConfig(self)
        self.groups = guifunctions.loadData(self, 0)
        self.users = guifunctions.loadData(self, 1)

        #build the main interface
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill='both', expand='yes')

        # create a child frames for each page of the Notebook
        self.status = statusframe.interface(self)
        self.settings = settingsframe.interface(self)
        self.accounts = accountframe.interface(self)
        self.advanced = advancedframe.interface(self)

        # create the pages
        self.nb.add(self.status.frame, text='Status')
        self.nb.add(self.settings.frame, text='Settings')
        self.nb.add(self.accounts.frame, text='Accounts')
        self.nb.add(self.advanced.frame, text='Advanced')
        self.status.build()
        self.status.versionlabel.config(text="re:wired " + self.config['appVersion'] +\
                                        " on " + guifunctions.getPlatformString(self))
        self.settings.build()
        self.accounts.build()
        self.advanced.build()
        self.populate()
        self.initUsers()

    def showabout(self):
        self.root.tk.call('tk::mac::standardAboutPanel')
        return 1

    def startButtonPressed(self):
        self.parent.startServer()
        return 1

    def reStartButtonPressed(self):
        self.parent.reStartServer()
        return 1

    def stopButtonPressed(self):
        self.parent.stopServer()
        return 1

    def populate(self):
        self.settings.servername.delete(0, tk.END)
        self.settings.servername.insert(0, self.config['serverName'])
        self.settings.description.delete(0, tk.END)
        self.settings.description.insert(0, self.config['serverDesc'])
        self.settings.port1.delete(0, tk.END)
        self.settings.port1.insert(0, self.config['port'])
        self.settings.verifyPort()
        self.settings.banner.delete(0, tk.END)
        self.settings.banner.insert(0, self.config['serverBanner'])
        self.settings.rootdir.delete(0, tk.END)
        self.settings.rootdir.insert(0, self.config['fileRoot'])
        self.advanced.trackertoggle.set(self.config['trackerRegister'])
        self.advanced.trackerurl.delete(0, tk.END)
        self.advanced.trackerurl.insert(0, self.config['trackerUrl'])
        self.advanced.indextoggle.set(self.config['doIndex'])
        self.advanced.indexinterval.delete(0, tk.END)
        self.advanced.indexinterval.insert(0, self.config['indexInterval'])
        self.advanced.setServerBandwidth(self.config['trackerBandwidth'])
        return 1

    def reloadAccounts(self):
        #reload the user db
        self.groups = guifunctions.loadData(self, 0)
        self.users = guifunctions.loadData(self, 1)
        #remove account view
        self.nb.forget(self.accounts.frame)
        del(self.accounts)
        # re-add it
        self.accounts = accountframe.interface(self)
        self.nb.insert(2, self.accounts.frame, text='Accounts')
        self.accounts.build()
        self.initUsers()
        self.nb.select(2)
        return 1

    def rewriteConfig(self):
        if not guifunctions.rewriteConfig(self.config):
            return 0
        return 1

    def initUsers(self):
        self.accounts.insertUser(self.users, self.groups)
        return 1

    def processIncoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.status.appendLog(msg)
            except Queue.Empty:
                pass
