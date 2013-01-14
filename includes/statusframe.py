import Tkinter as tk
import ttk


class interface():
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame()
        self.innerFrame = ttk.Frame()

    def build(self):
        self.innerFrame.place(in_=self.frame, anchor="c", relx=.5, rely=.5)
        self.innerFrame.columnconfigure(0, weight=0)
        self.innerFrame.columnconfigure(1, weight=0)
        self.innerFrame.columnconfigure(2, weight=1)
        self.innerFrame.columnconfigure(3, weight=0)
        iconimageon = tk.PhotoImage(file="data/logo_on.gif", width=32, height=32)
        iconimageoff = tk.PhotoImage(file="data/logo_off.gif", width=32, height=32)
        self.icon = ttk.Label(self.innerFrame, image=iconimageoff)
        self.icon.imageon = iconimageon
        self.icon.imageoff = iconimageoff
        self.icon.grid(row=0, column=0, rowspan=2)
        self.statuslabel = ttk.Label(self.innerFrame, text="re:wired Server is not running.",\
                                     font=("Lucida Grande Bold", 15))
        self.statuslabel.grid(row=0, column=1, columnspan=2, sticky=tk.W)
        self.versionlabel = ttk.Label(self.innerFrame, font=("Lucida Grande", 12))
        self.versionlabel.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=10)
        self.startbutton = ttk.Button(self.innerFrame, text='Start', command=self.parent.startButtonPressed)
        self.startbutton.grid(row=2, column=0, sticky=tk.W, padx=5)
        self.startbutton.config(state=tk.DISABLED)
        self.stopbutton = ttk.Button(self.innerFrame, text='Stop', command=self.parent.stopButtonPressed)
        self.stopbutton.config(state=tk.DISABLED)
        self.stopbutton.grid(row=2, column=1, sticky=tk.W, padx=5)
        self.restartbutton = ttk.Button(self.innerFrame, text='re:Start', command=self.parent.reStartButtonPressed)
        self.restartbutton.config(state=tk.DISABLED)
        self.restartbutton.grid(row=2, column=2, sticky=tk.W, padx=5)
        spacer = ttk.Separator(self.innerFrame)
        spacer.grid(row=3, column=0, columnspan=4, sticky=tk.E + tk.W, pady=12)
        self.log = tk.Text(self.innerFrame)
        self.log.configure(width=70, height=18)
        self.log.grid(row=4, column=0, columnspan=3, sticky=tk.N + tk.E + tk.S + tk.W)
        self.scrollbar = tk.Scrollbar(self.innerFrame)
        self.scrollbar.grid(row=4, column=3, sticky=tk.N + tk.S)
        self.log.config(yscrollcommand=self.scrollbar.set)
        self.log.insert(tk.END, "")
        self.scrollbar.config(command=self.log.yview)
        self.log.config(state=tk.DISABLED)
        return 1

    def appendLog(self, log):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, log)
        self.log.yview(tk.END)
        self.log.config(state=tk.DISABLED)
        return 1
