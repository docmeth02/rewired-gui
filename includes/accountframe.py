import Tkinter as tk
import tkMessageBox
import ttk
import hashlib
from includes import guifunctions


class interface():
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame()
        self.innerFrame = ttk.Frame()

    def build(self):
        self.innerFrame.place(in_=self.frame, anchor="c", relx=.5, rely=.5)
        self.accountlist = ttk.Treeview(self.innerFrame, height=18)
        self.accountlist["columns"] = ("accounts")
        self.accountlist.configure(show='tree', selectmode='browse')
        self.accountlist.column("accounts", width=1)
        self.accountlist.heading("accounts", text="")
        self.accountlist.bind('<<TreeviewSelect>>', self.userSelectChanged)
        self.accountlist.grid(row=0, column=0, columnspan=1, sticky=tk.E)
        self.accnb = ttk.Notebook(self.innerFrame, width=325)
        self.info = userinfo(self)
        self.privs = privileges(self)
        self.limits = userlimits(self)
        self.accnb.add(self.info.frame, text='Account Info')
        self.accnb.add(self.privs.frame, text='Privileges')
        self.accnb.add(self.limits.frame, text='Limits')
        self.accnb.grid(row=0, column=2, sticky=tk.S + tk.N)
        self.info.display()
        self.privs.display()
        self.limits.display()

    def insertUser(self, users, groups):
        for aitem in users:
            self.accountlist.insert("", tk.END, str(aitem[0]), text=str(aitem[0]))
        for aitem in groups:
            self.accountlist.insert("", tk.END, str(aitem[0]), text=str(aitem[0]))
        try:
            self.accountlist.selection_set(self.accountlist.get_children()[0])
        except:
            pass

    def userSelectChanged(self, arg):
        # Load user data for selected user into the gui
        selection = 0
        self.info.typeMarker = 0
        for auser in self.parent.users:
            if auser[0] == self.accountlist.selection()[0]:
                selection = auser
                self.info.typeMarker = 1
                break
        for agroup in self.parent.groups:
            if agroup[0] == self.accountlist.selection()[0]:
                selection = agroup
                break
        self.info.username.config(state=tk.NORMAL)
        self.info.username.delete(0, tk.END)
        self.info.username.insert(0, selection[0])
        self.info.username.config(state=tk.DISABLED)
        self.info.acctype.config(state=tk.NORMAL)
        if self.info.typeMarker:
            #user account
            self.info.type.set("User")
            self.info.password.config(state=tk.NORMAL)
            self.info.password.delete(0, tk.END)
            self.info.password.insert(0, "PASSWORDDIDNOTCHANGE")
            self.info.grouplist.config(state=tk.NORMAL)
            self.info.passhash = auser[1]
            if auser[2] != '':
                self.info.group.set(auser[2])
                self.disablePrivs()
            else:
                self.info.group.set("None")
                self.enablePrivs()
        else:
            #group account
            self.info.type.set("Group")
            self.info.passhash = ''
            self.info.password.config(state=tk.NORMAL)
            self.info.password.delete(0, tk.END)
            self.info.password.config(state=tk.DISABLED)
            self.info.grouplist.config(state=tk.DISABLED)
            self.info.group.set("None")
            self.enablePrivs()

        self.info.acctype.config(state=tk.DISABLED)
        if selection[2] != '':
            privs = self.getGroupPrivs(selection[2]).split(chr(28))
        else:
            privs = selection[4].split(chr(28))
        if not privs:
            return 0
        if len(privs) != 23:
            return 0  # something is wrong here
        self.privs.getuserinfo.set(privs[0])
        self.privs.postnews.set(privs[2])
        self.privs.broadcast.set(privs[1])
        self.privs.clearnews.set(privs[3])
        self.privs.settopic.set(privs[22])
        self.privs.download.set(privs[4])
        self.privs.createfolders.set(privs[7])
        self.privs.upload.set(privs[5])
        self.privs.movechange.set(privs[8])
        self.privs.uploadanyhere.set(privs[6])
        self.privs.delete.set(privs[9])
        self.privs.viewdbox.set(privs[10])
        self.privs.createacc.set(privs[11])
        self.privs.kick.set(privs[15])
        self.privs.editacc.set(privs[12])
        self.privs.ban.set(privs[16])
        self.privs.deleteacc.set(privs[13])
        self.privs.cantbkicked.set(privs[17])
        self.privs.elevateprivs.set(privs[14])
        self.privs.MaxDownloads.set(privs[20])
        self.privs.MaxUploads.set(privs[21])
        self.limits.uplimit.delete(0, tk.END)
        self.limits.uplimit.insert(0, int(privs[19]) / 1024)
        self.limits.downlimit.delete(0, tk.END)
        self.limits.downlimit.insert(0, int(privs[18]) / 1024)
        return 1

    def getGroupPrivs(self, group):
        for agroup in self.parent.groups:
            if agroup[2] == group:
                return agroup[4]
        return 0

    def grouplistchanged(self, *args):
        if self.info.typeMarker:
            # is a user
            if self.info.group.get() == 'None':
                self.enablePrivs()
            else:
                self.disablePrivs()
            return 1
        # must be a group
        self.enablePrivs()
        return 1

    def saveUser(self, **args):
        item = []
        #build privstring
        privmask = str(self.privs.getuserinfo.get()) + chr(28)
        privmask += str(self.privs.broadcast.get()) + chr(28)
        privmask += str(self.privs.postnews.get()) + chr(28)
        privmask += str(self.privs.clearnews.get()) + chr(28)
        privmask += str(self.privs.download.get()) + chr(28)
        privmask += str(self.privs.upload.get()) + chr(28)
        privmask += str(self.privs.uploadanyhere.get()) + chr(28)
        privmask += str(self.privs.createfolders.get()) + chr(28)
        privmask += str(self.privs.movechange.get()) + chr(28)
        privmask += str(self.privs.delete.get()) + chr(28)
        privmask += str(self.privs.viewdbox.get()) + chr(28)
        privmask += str(self.privs.createacc.get()) + chr(28)
        privmask += str(self.privs.editacc.get()) + chr(28)
        privmask += str(self.privs.deleteacc.get()) + chr(28)
        privmask += str(self.privs.elevateprivs.get()) + chr(28)
        privmask += str(self.privs.kick.get()) + chr(28)
        privmask += str(self.privs.ban.get()) + chr(28)
        privmask += str(self.privs.cantbkicked.get()) + chr(28)
        if self.limits.downlimit.get() == '':
            self.limits.downlimit.insert(0, 0)
        if self.limits.uplimit.get() == '':
            self.limits.uplimit.insert(0, 0)
        privmask += str(int(self.limits.downlimit.get()) * 1024) + chr(28)
        privmask += str(int(self.limits.uplimit.get()) * 1024) + chr(28)
        privmask += str(self.privs.MaxDownloads.get()) + chr(28)
        privmask += str(self.privs.MaxUploads.get()) + chr(28)
        privmask += str(self.privs.settopic.get())
        item.insert(0, self.info.username.get())
        if self.info.typeMarker:
            #user
            # get the password
            if self.info.password.get() == 'PASSWORDDIDNOTCHANGE':
                password = self.info.passhash
            else:
                newpass = hashlib.sha1()
                newpass.update(self.info.password.get())
                password = newpass.hexdigest()
                if self.info.password.get() == '':
                    password = ''  # empty password needs to be an empty string!
            # get group membership
            if self.info.group.get() == 'None':
                item.insert(2, '')  # no group
            else:
                item.insert(2, str(self.info.group.get()))

        else:
            # group
            item.insert(2, str(self.info.username.get()))
            password = ''
        item.insert(1, password)
        item.insert(3, privmask)
        if not guifunctions.updateData(self.parent, item, self.info.typeMarker):
            print "UPDATE Failed"
        self.parent.reloadAccounts()
        return 1

    def deleteItem(self, *args):
        # first get confirmation
        if self.info.typeMarker:
            # user
            name = self.info.username.get()
            if name == 'admin':
                tkMessageBox.showinfo("Not allowed", "Deleting the admin user is not allowed!")
                return 0
            if not tkMessageBox.askyesno(message='Are you sure you want to delete user ' + str(name) + '?',\
                                        icon='question', title='Confirm deletion'):
                return 0
        else:
            #this is a group, we need to be sure its not in use ...
            name = self.info.username.get()
            for auser in self.parent.users:
                if auser[2] == name:
                    tkMessageBox.showinfo("Group is still in use!", "User " + str(auser[0]) +\
                                          " is still a member of group " + str(name) + "!")
                    return 0
            if not tkMessageBox.askyesno(message='Are you sure you want to delete group ' + str(name) +\
                                         '?', icon='question', title='Confirm deletion'):
                return 0
        # now delete the item
        if not guifunctions.deleteData(self.parent, name, self.info.typeMarker):
            print "UPDATE Failed"
            return 0
        self.parent.reloadAccounts()
        return 1

    def disablePrivs(self):
        self.privs.CBgetuserinfo.config(state=tk.DISABLED)
        self.privs.CBpostnews.config(state=tk.DISABLED)
        self.privs.CBbroadcast.config(state=tk.DISABLED)
        self.privs.CBclearnews.config(state=tk.DISABLED)
        self.privs.CBsettopic.config(state=tk.DISABLED)
        self.privs.CBdownload.config(state=tk.DISABLED)
        self.privs.CBcreatefol.config(state=tk.DISABLED)
        self.privs.CBupload.config(state=tk.DISABLED)
        self.privs.CBmovechange.config(state=tk.DISABLED)
        self.privs.CBuploadanyw.config(state=tk.DISABLED)
        self.privs.CBdelete.config(state=tk.DISABLED)
        self.privs.CBviewdb.config(state=tk.DISABLED)
        self.privs.CBacccreate.config(state=tk.DISABLED)
        self.privs.CBkick.config(state=tk.DISABLED)
        self.privs.CBeditacc.config(state=tk.DISABLED)
        self.privs.CBbanuser.config(state=tk.DISABLED)
        self.privs.CBdelacc.config(state=tk.DISABLED)
        self.privs.CBcantbkick.config(state=tk.DISABLED)
        self.privs.CBelevprivs.config(state=tk.DISABLED)

    def enablePrivs(self):
        self.privs.CBgetuserinfo.config(state=tk.NORMAL)
        self.privs.CBpostnews.config(state=tk.NORMAL)
        self.privs.CBbroadcast.config(state=tk.NORMAL)
        self.privs.CBclearnews.config(state=tk.NORMAL)
        self.privs.CBsettopic.config(state=tk.NORMAL)
        self.privs.CBdownload.config(state=tk.NORMAL)
        self.privs.CBcreatefol.config(state=tk.NORMAL)
        self.privs.CBupload.config(state=tk.NORMAL)
        self.privs.CBmovechange.config(state=tk.NORMAL)
        self.privs.CBuploadanyw.config(state=tk.NORMAL)
        self.privs.CBdelete.config(state=tk.NORMAL)
        self.privs.CBviewdb.config(state=tk.NORMAL)
        self.privs.CBacccreate.config(state=tk.NORMAL)
        self.privs.CBkick.config(state=tk.NORMAL)
        self.privs.CBeditacc.config(state=tk.NORMAL)
        self.privs.CBbanuser.config(state=tk.NORMAL)
        self.privs.CBdelacc.config(state=tk.NORMAL)
        self.privs.CBcantbkick.config(state=tk.NORMAL)
        self.privs.CBelevprivs.config(state=tk.NORMAL)


class userinfo():
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame()
        self.infoframe = ttk.Frame()  # instanciate it here this time and reference to it later
        self.type = tk.StringVar(self.infoframe)
        self.type.set("User")
        self.group = tk.StringVar(self.infoframe)
        self.group.set("None")

    def display(self):
        infoframe = self.infoframe
        infoframe.place(in_=self.frame, anchor="c", relx=.5, rely=.5)
        typelabel = ttk.Label(infoframe, text="Type:")
        typelabel.grid(row=0, column=0, sticky=tk.E, pady=12)
        self.acctype = ttk.OptionMenu(infoframe, self.type, '', "User", "Group")
        self.acctype.config(width=15)
        self.acctype.grid(row=0, column=1)
        infospacer = ttk.Separator(infoframe)
        infospacer.grid(row=1, column=0, columnspan=2, sticky=tk.E + tk.W, pady=12)
        infonamelabel = ttk.Label(infoframe, text="Name:")
        infonamelabel.grid(row=2, column=0, sticky=tk.E, pady=12)
        self.username = tk.Entry(infoframe)
        self.username.grid(row=2, column=1)
        infopasslabel = ttk.Label(infoframe, text="Password:")
        infopasslabel.grid(row=3, column=0, sticky=tk.E, pady=12)
        self.password = tk.Entry(infoframe, show='*')
        self.password.grid(row=3, column=1)
        infogrouplabel = ttk.Label(infoframe, text="Group:")
        infogrouplabel.grid(row=4, column=0, sticky=tk.E, pady=12)
        fields = []
        for agroup in self.parent.parent.groups:
            fields.append(agroup[0])
        fields.insert(0, 'None')
        fields.insert(0, '')
        self.grouplist = ttk.OptionMenu(infoframe, self.group, command=self.parent.grouplistchanged, *fields)
        self.grouplist.config(width=15)
        self.grouplist.grid(row=4, column=1)
        self.savebutton = ttk.Button(infoframe, text='Save', command=self.parent.saveUser)
        self.savebutton.grid(row=5, column=0, sticky=tk.W, padx=5)
        self.deletebutton = ttk.Button(self.infoframe, text='Delete', command=self.parent.deleteItem)
        self.deletebutton.grid(row=5, column=1, sticky=tk.E, padx=5)


class privileges():
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame()
        self.typeMarker = -1
        self.passhash = ''

        self.getuserinfo = tk.IntVar()
        self.postnews = tk.IntVar()
        self.broadcast = tk.IntVar()
        self.clearnews = tk.IntVar()
        self.settopic = tk.IntVar()
        self.download = tk.IntVar()
        self.createfolders = tk.IntVar()
        self.upload = tk.IntVar()
        self.movechange = tk.IntVar()
        self.uploadanyhere = tk.IntVar()
        self.delete = tk.IntVar()
        self.viewdbox = tk.IntVar()
        self.createacc = tk.IntVar()
        self.kick = tk.IntVar()
        self.editacc = tk.IntVar()
        self.ban = tk.IntVar()
        self.deleteacc = tk.IntVar()
        self.cantbkicked = tk.IntVar()
        self.elevateprivs = tk.IntVar()
        self.MaxDownloads = tk.IntVar()
        self.MaxUploads = tk.IntVar()

    def display(self):
        privfont = ("Lucia Grande", 10)
        privframe = ttk.Frame()
        privframe.place(in_=self.frame, anchor="c", relx=.5, rely=.5)
        basiclabel = ttk.Label(privframe, text="Basic:")
        basiclabel.grid(row=0, column=0, sticky=tk.E)
        self.CBgetuserinfo = ttk.Checkbutton(privframe, text="Get User Info", variable=self.getuserinfo)
        self.CBgetuserinfo.grid(row=0, column=1, sticky=tk.W)
        self.CBpostnews = ttk.Checkbutton(privframe, text="Post News", variable=self.postnews)
        self.CBpostnews.grid(row=0, column=2, sticky=tk.W)
        self.CBbroadcast = ttk.Checkbutton(privframe, text="Broadcast", variable=self.broadcast)
        self.CBbroadcast.grid(row=1, column=1, sticky=tk.W)
        self.CBclearnews = ttk.Checkbutton(privframe, text="Clear News", variable=self.clearnews)
        self.CBclearnews.grid(row=1, column=2, sticky=tk.W)
        self.CBsettopic = ttk.Checkbutton(privframe, text="Set Topic", variable=self.settopic)
        self.CBsettopic.grid(row=2, column=1, sticky=tk.W)
        privspacer = ttk.Separator(privframe)
        privspacer.grid(row=3, column=0, columnspan=3, sticky=tk.E + tk.W, pady=5)
        fileslabel = ttk.Label(privframe, text="Files:")
        fileslabel.grid(row=4, column=0, sticky=tk.E)
        self.CBdownload = ttk.Checkbutton(privframe, text="Download", variable=self.download)
        self.CBdownload.grid(row=4, column=1, sticky=tk.W)
        self.CBcreatefol = ttk.Checkbutton(privframe, text="Create Folders", variable=self.createfolders)
        self.CBcreatefol.grid(row=4, column=2, sticky=tk.W)
        self.CBupload = ttk.Checkbutton(privframe, text="Upload", variable=self.upload)
        self.CBupload.grid(row=5, column=1, sticky=tk.W)
        self.CBmovechange = ttk.Checkbutton(privframe, text="Move & Change", variable=self.movechange)
        self.CBmovechange.grid(row=5, column=2, sticky=tk.W)
        self.CBuploadanyw = ttk.Checkbutton(privframe, text="Upload Anywhere", variable=self.uploadanyhere)
        self.CBuploadanyw.grid(row=6, column=1, sticky=tk.W)
        self.CBdelete = ttk.Checkbutton(privframe, text="Delete", variable=self.delete)
        self.CBdelete.grid(row=6, column=2, sticky=tk.W)
        self.CBviewdb = ttk.Checkbutton(privframe, text="View Drop Boxes", variable=self.viewdbox)
        self.CBviewdb.grid(row=7, column=1, sticky=tk.W)
        privspacer2 = ttk.Separator(privframe)
        privspacer2.grid(row=8, column=0, columnspan=3, sticky=tk.E + tk.W, pady=5)
        acclabel = ttk.Label(privframe, text="Accounts:")
        acclabel.grid(row=9, column=0, sticky=tk.E)
        self.CBacccreate = ttk.Checkbutton(privframe, text="Create Accounts", variable=self.createacc)
        self.CBacccreate.grid(row=9, column=1, sticky=tk.W)
        self.CBkick = ttk.Checkbutton(privframe, text="Kick Users", variable=self.kick)
        self.CBkick.grid(row=9, column=2, sticky=tk.W)
        self.CBeditacc = ttk.Checkbutton(privframe, text="Edit Accounts", variable=self.editacc)
        self.CBeditacc.grid(row=10, column=1, sticky=tk.W)
        self.CBbanuser = ttk.Checkbutton(privframe, text="Ban Users", variable=self.ban)
        self.CBbanuser.grid(row=10, column=2, sticky=tk.W)
        self.CBdelacc = ttk.Checkbutton(privframe, text="Delete Accounts", variable=self.deleteacc)
        self.CBdelacc.grid(row=11, column=1, sticky=tk.W)
        self.CBcantbkick = ttk.Checkbutton(privframe, text="Cannot Be Kicked", variable=self.cantbkicked)
        self.CBcantbkick.grid(row=11, column=2, sticky=tk.W)
        self.CBelevprivs = ttk.Checkbutton(privframe, text="Elevate Privileges", variable=self.elevateprivs)
        self.CBelevprivs.grid(row=12, column=1, sticky=tk.W)


class userlimits():
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame()

    def display(self):
        userlimits = ttk.Frame()
        userlimits.place(in_=self.frame, anchor="c", relx=.5, rely=.5)
        downllabel = ttk.Label(userlimits, text="Download:")
        downllabel.grid(row=1, column=0, sticky=tk.E, pady=5)
        self.downlimit = tk.Entry(userlimits, width=5)
        self.downlimit.grid(row=1, column=1, sticky=tk.W, pady=5)
        downlkblabel = ttk.Label(userlimits, text="KB/s")
        downlkblabel.grid(row=1, column=2, sticky=tk.W, pady=5)
        upllabel = ttk.Label(userlimits, text="Uploads:")
        upllabel.grid(row=2, column=0, sticky=tk.E, pady=5)
        self.uplimit = tk.Entry(userlimits, width=5)
        self.uplimit.grid(row=2, column=1, sticky=tk.W, pady=5)
        uplkblabel = ttk.Label(userlimits, text="KB/s")
        uplkblabel.grid(row=2, column=2, sticky=tk.W, pady=5)
