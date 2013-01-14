import Tkinter as tk
import ttk
import tkFileDialog
from includes import guifunctions
from socket import gethostname


class interface():
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame()
        self.innerFrame = ttk.Frame()
        style = ttk.Style()
        style.configure("RED.Label", foreground="#E62E00")
        style.configure("GREEN.Label", foreground="#248F24")

    def build(self):
        self.innerFrame.place(in_=self.frame, anchor="c", relx=.5, rely=.5)
        namelabel = ttk.Label(self.innerFrame, text="Name:")
        namelabel.grid(row=0, column=0, sticky=tk.E, pady=12)
        self.servername = tk.Entry(self.innerFrame)
        self.servername.insert(0, "A re:wired Server")
        self.servername.grid(row=0, column=1, columnspan=1, sticky=tk.W + tk.E)
        portlabel = ttk.Label(self.innerFrame, text="  Port:")
        portlabel.grid(row=0, column=2, sticky=tk.E)
        self.port1 = tk.Entry(self.innerFrame, width=6, validate='focus', validatecommand=self.verifyPort)
        self.port1.insert(0, "2000")
        self.port1.grid(row=0, column=3, sticky=tk.W)
        self.port2 = tk.Entry(self.innerFrame, width=6)
        self.port2.insert(0, "2001")
        self.port2.grid(row=0, column=4, sticky=tk.W)
        self.port2.config(state="readonly")
        desclabel = ttk.Label(self.innerFrame, text="Description:")
        desclabel.grid(row=1, column=0, sticky=tk.E, pady=12)
        self.description = tk.Entry(self.innerFrame)
        self.description.insert(0, "Another super awesome re:wired Server")
        self.description.grid(row=1, column=1, columnspan=3, sticky=tk.W + tk.E)
        bannerlabel = ttk.Label(self.innerFrame, text="Banner File:")
        bannerlabel.grid(row=2, column=0, sticky=tk.E, pady=12)
        self.banner = tk.Entry(self.innerFrame)
        self.banner.insert(0, "")
        self.banner.grid(row=2, column=1, columnspan=3, sticky=tk.W + tk.E, pady=10)
        bannerchooser = ttk.Button(self.innerFrame, text='re:Select', command=self.askfile, width=8)
        bannerchooser.grid(row=2, column=4)
        setspacer = ttk.Separator(self.innerFrame)
        setspacer.grid(row=3, column=0, columnspan=5, sticky=tk.E + tk.W, pady=12)
        rootlabel = ttk.Label(self.innerFrame, text="File Directory:")
        rootlabel.grid(row=4, column=0, sticky=tk.E, pady=12)
        self.rootdir = tk.Entry(self.innerFrame)
        self.rootdir.insert(0, "")
        self.rootdir.grid(row=4, column=1, columnspan=3, sticky=tk.W + tk.E, pady=10)
        rootchooser = ttk.Button(self.innerFrame, text='re:Select', command=self.askdirectory, width=8)
        rootchooser.grid(row=4, column=4)
        setspacer2 = ttk.Separator(self.innerFrame)
        setspacer2.grid(row=5, column=0, columnspan=5, sticky=tk.E + tk.W, pady=12)
        certlabel = ttk.Label(self.innerFrame, text="Certificate:")
        certlabel.grid(row=6, column=0, sticky=tk.E, pady=12)
        self.certcname = ttk.Label(self.innerFrame)
        self.certcname.grid(row=6, column=1, columnspan=3, sticky=tk.W)
        self.hostnlabel = ttk.Label(self.innerFrame)
        self.hostnlabel.grid(row=7, column=1, columnspan=3, sticky=tk.W)
        self.createcert = ttk.Button(self.innerFrame, text='re:Create', width=8, command=self.newCert)
        self.createcert.config(state=tk.DISABLED)
        self.createcert.grid(row=6, column=4, rowspan=1)
        self.settsave = ttk.Button(self.innerFrame, text='Save', command=self.saveConf)
        self.settsave.grid(row=8, column=0, columnspan=5, pady=15)
        self.checkCert()

    def saveConf(self):
        self.parent.config['serverName'] = self.servername.get()
        self.parent.config['port'] = self.port1.get()
        self.parent.config['serverDesc'] = self.description.get()
        self.parent.config['serverBanner'] = self.banner.get()
        self.parent.config['fileRoot'] = self.rootdir.get()
        self.parent.rewriteConfig()  # write to file
        self.parent.populate()  # repaint
        return 1

    def verifyPort(self):
        port = self.port1.get()
        try:
            port = int(self.port1.get())
        except:
            self.port1.delete(0, tk.END)
            self.port1.insert(0, "2000")
            return False
        self.port2.config(state=tk.NORMAL)
        self.port2.delete(0, tk.END)
        self.port2.insert(0, port + 1)
        self.port2.config(state='readonly')
        return port

    def askfile(self):
        filename = 0
        filename = tkFileDialog.askopenfilename(filetypes=[('PNG File', '.png')])
        if filename:
            self.banner.delete(0, tk.END)
            self.banner.insert(0, filename)
            return 1
        return 0

    def askdirectory(self):
        dirname = 0
        dirname = tkFileDialog.askdirectory()
        if dirname:
            self.rootdir.delete(0, tk.END)
            self.rootdir.insert(0, dirname)
            return 1
        return 0

    def checkCert(self):
        certname = guifunctions.getCertName(self.parent.config['cert'])
        hostname = gethostname()
        self.hostnlabel.config(text="Hostname: " + hostname)
        self.certcname.config(text="issued for " + str(certname))
        if certname != hostname:
            self.certcname.config(style="RED.Label")
            self.createcert.config(state=tk.NORMAL)
            return 1
        self.createcert.config(state=tk.DISABLED)
        self.certcname.config(style="GREEN.Label")
        return 1

    def newCert(self):
        if not guifunctions.createCert(self.parent.config['cert'], gethostname()):
        #error msg here
            self.checkCert()
            return 0
        self.checkCert()
        return 1
