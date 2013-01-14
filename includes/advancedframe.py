import Tkinter as tk
import ttk


class interface():
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame()
        self.trackertoggle = tk.IntVar()
        self.indextoggle = tk.IntVar()
        self.bandwidthValues = {"100000": "1M DSL/Cable", "1000000": "10M LAN", "10000000": "100M LAN"}

    def build(self):
        self.innerFrame = ttk.Frame()
        self.innerFrame.place(in_=self.frame, anchor="c", relx=.5, rely=.5)
        register = ttk.Checkbutton(self.innerFrame, text="Register With Tracker", variable=self.trackertoggle)
        register.grid(row=0, column=1, sticky=tk.W, pady=5, columnspan=2)
        trackerlabel = ttk.Label(self.innerFrame, text="Tracker Url: ")
        trackerlabel.grid(row=1, column=0, sticky=tk.E, pady=5)
        self.trackerurl = tk.Entry(self.innerFrame, width=30)
        self.trackerurl.insert(0, "wired.zankasoftware.com")
        self.trackerurl.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        bandwidthlabel = ttk.Label(self.innerFrame, text="Bandwidth: ")
        bandwidthlabel.grid(row=2, column=0, sticky=tk.E, pady=5)
        self.bandwidth = tk.StringVar(self.innerFrame)
        # create fileds from dict
        fields = self.bandwidthValues.values()
        fields.sort(key=str.lower)
        fields.reverse()
        fields.insert(0, '')  # fix first field not displayed bug
        self.serverspeed = ttk.OptionMenu(self.innerFrame, self.bandwidth, *fields)
        self.serverspeed.config(width=15)
        self.serverspeed.grid(row=2, column=1, sticky=tk.W, columnspan=2)
        trackspacer = ttk.Separator(self.innerFrame)
        trackspacer.grid(row=3, column=0, columnspan=3, sticky=tk.E + tk.W, pady=15)
        self.index = ttk.Checkbutton(self.innerFrame, text="Index Server Files", variable=self.indextoggle)
        self.index.grid(row=4, column=1, sticky=tk.W, pady=5, columnspan=2)
        indextimelabel = ttk.Label(self.innerFrame, text="Index Interval: ")
        indextimelabel.grid(row=5, column=0, sticky=tk.E, pady=5)
        self.indexinterval = tk.Entry(self.innerFrame, width=12)
        self.indexinterval.insert(0, 600)
        self.indexinterval.grid(row=5, column=1, sticky=tk.W + tk.E, pady=5)
        indexseclabel = ttk.Label(self.innerFrame, text=" Seconds")
        indexseclabel.grid(row=5, column=2, sticky=tk.W, pady=5)
        daemonspacer = ttk.Separator(self.innerFrame)
        daemonspacer.grid(row=6, column=0, columnspan=3, sticky=tk.E + tk.W, pady=15)
        bandwidthlabel = ttk.Label(self.innerFrame, text="Install re:wired as a launch daemon:")
        bandwidthlabel.grid(row=7, column=0, sticky=tk.E, pady=5, columnspan=2)
        daemonstatus = ttk.Label(self.innerFrame, text="Daemon not installed.", font=("Lucida Grande", 15))
        daemonstatus.grid(row=8, column=0, columnspan=3)
        daemoninstall = ttk.Button(self.innerFrame, text='Install', state=tk.DISABLED)
        daemoninstall.grid(row=9, column=0, sticky=tk.E, pady=5)
        daemonuninstall = ttk.Button(self.innerFrame, text='Uninstall', state=tk.DISABLED)
        daemonuninstall.grid(row=9, column=1, padx=5)
        daemonupdate = ttk.Button(self.innerFrame, text='Update', state=tk.DISABLED)
        daemonupdate.grid(row=9, column=2, sticky=tk.W, padx=5)
        self.advsave = ttk.Button(self.innerFrame, text='Save', command=self.saveConf)
        self.advsave.grid(row=10, column=0, columnspan=5, pady=15)

    def setServerBandwidth(self, speed):
        for abandwidth, label in self.bandwidthValues.items():
            if int(speed) == int(abandwidth):
                self.bandwidth.set(label)
                return 1
        print "BW fallback!"
        self.bandwidth.set("10M LAN")
        return 0

    def saveConf(self):
        speed = 0
        for value, key in self.bandwidthValues.items():
            if key == self.bandwidth.get():
                speed = value
        if not speed:
            return 0
        self.parent.config['trackerRegister'] = self.trackertoggle.get()
        self.parent.config['trackerUrl'] = self.trackerurl.get()
        self.parent.config['trackerBandwidth'] = speed
        self.parent.config['doIndex'] = self.indextoggle.get()
        self.parent.config['indexInterval'] = self.indexinterval.get()
        self.parent.rewriteConfig()  # write to file
        self.parent.populate()  # repaint
        return 1
