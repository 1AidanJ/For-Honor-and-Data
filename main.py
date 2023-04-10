import tkinter
import sqlite3
#import matplotlib
#import pandas
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import askyesno
import tkinter.font as tkfont


# ------------- For Honor & Data ------------#

# A tkinter and sqlite3 stat viewer and database manager
# Divided into tabs, tab 1 constitutes the player profile viewer. Ideally could be 
# expanded with personal statistics on a per character basis
# Tab 2 is the records list, showing a record of every time a player was entered into the database.
# Allows the editing, creation and deletion of new records through demonstrative example tools
# Deletion has support for deleting multiple selections at once.
# Both tabs can be filtered by searching, which searches by similar character in the name field.


conn = sqlite3.connect('FHred.db')
cursor = conn.cursor()

win = tkinter.Tk()
win.geometry("900x500")
win.title("For Honor and Data - Main")
main = Menu(win)

# Sets up the tab system / tab switching
tabMenu = ttk.Notebook(win)
tab1 = ttk.Frame(tabMenu)
#tab2 = ttk.Frame(tabMenu)
tab3 = ttk.Frame(tabMenu)
tabMenu.add(tab1, text='Player List')
#tabMenu.add(tab2, text='Hero Stats')
tabMenu.add(tab3, text='Data Records')
tabMenu.pack(side=TOP, anchor=W)
playerdata = ()


#======================== Tab 1 LIST VIEW ===============================#


class PlayerList(Frame):
    def __init__(self):
        # Initial Setup
        lst = Frame(tab1, relief="sunken", bd=3,
                    width=460, height=500, pady=10)
        lst.pack(side=LEFT, fill=Y, anchor=N)
        lst.pack_propagate(0)
        # forcing proper dimensions with propagate

        header = Frame(lst, relief="sunken",
                       width=460, height=200)
        header.pack()
        label = Label(header, text="For Honor Player List",
                      pady=10, font=tkfont.Font(
                          family='MSPGothic', size=16, weight="bold"))
        label.pack()
        # Setting up the treeview
        yscroll = Scrollbar(tab1, orient=VERTICAL)
        self.tree = ttk.Treeview(lst, columns=("Player ID", "Username", "Platform", "Reputation", "Faction"),
                                 selectmode="extended", yscrollcommand=yscroll.set)
        self.tree.heading("Player ID", text="Player ID", anchor=W)
        self.tree.heading("Username", text="Username", anchor=W)
        self.tree.heading("Platform", text="Platform", anchor=W)
        self.tree.heading("Reputation", text="Reputation", anchor=W)
        self.tree.heading("Faction", text="Faction", anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=80)
        self.tree.column('#2', stretch=NO, minwidth=0, width=120)
        self.tree.column('#3', stretch=NO, minwidth=0, width=100)
        self.tree.column('#4', stretch=NO, minwidth=0, width=80)
        self.tree.column('#5', stretch=NO, minwidth=0, width=60)
        self.tree.pack(expand=True, fill=Y)
        self.tree.pack_propagate(0)
        yscroll.config(command=self.tree.yview)
        yscroll.pack(side=LEFT, fill=Y)
        yscroll.pack_propagate(0)
        self.tree.tag_configure('default', background='grey')
        self.tree.tag_configure('knight', background='yellow')
        self.tree.tag_configure('viking', background='red')
        self.tree.tag_configure('samurai', background='lightgreen')

        self.searchbar = Entry(header, width=30)
        self.searchbar.pack(side=LEFT, anchor=E, padx=10, pady=10)
        searchbutton = Button(
            header, width=10, text="Search", command=self.search)
        searchbutton.pack(side=LEFT, anchor=W, padx=10, pady=10)

        # Filling the treeview
        cursor.execute(
            "SELECT playerID,username,platform,reputation,faction FROM stat GROUP BY username")
        rows = cursor.fetchall()
        self.update(rows)
        self.tree.bind("<<TreeviewSelect>>", self.updateplayerdata)

    def search(self):
        # handles the searchbar's operation
        for item in self.tree.get_children():
            self.tree.delete(item)
        inp = self.searchbar.get()
        cursor.execute(
            "SELECT playerID,username,platform,reputation,faction FROM stat WHERE username LIKE ? GROUP BY username", (str(inp) + '%',))
        rows = cursor.fetchall()
        self.update(rows)

    def update(self, rows):
        # Updates the player list treeview

        for row in rows:
            # Populates tree with specific player data
            ctag = "default"
            if row[4] == 1:
                tag = 'knight'
            elif row[4] == 2:
                tag = 'viking'
            elif row[4] == 3:
                tag = 'samurai'
            else:
                tag = 'default'
            self.tree.insert(parent="", index='end', values=(
                row[0], row[1], row[2], row[3], row[4]), tags=(ctag))

    def updateplayerdata(self, event):
        # calls the PlayerData pointer function. This provides that function with the playername of the selected item in the treeview.
        # Necessary because this is happening cross class.
        global playerdata
        selectid = event.widget.selection()
        select = self.tree.item(selectid)
        playerdata = select.get("values")
        PlayerData.point()


#======================== Tab 1 STAT CARD ===============================#


class PlayerData(Frame):
    def __init__(self):
        global playerdata

        panel = Frame(tab1, relief="raised", bd=3,
                      width=420, height=500, pady=10)
        panel.pack(side=TOP, fill=Y, anchor=N)
        panel.pack_propagate(0)

        self.header = Frame(panel, relief="sunken", width=420, height=100)
        self.namelab = Label(self.header, text='Username:   ',
                             pady=10, font=tkfont.Font(
                                 family='MSPGothic', size=16, weight="bold"))
        self.namelab.pack(expand=True, fill=X, side=LEFT)

        self.header.pack()

        statcardleft = Frame(panel, relief="sunken",
                             width=200, height=400, pady=10)
        statcardleft.pack(side=LEFT, fill=Y, anchor=S)
        statcardleft.pack_propagate(0)

        # Dear god im sorry. Left side of the stat card
        self.platlab = Label(statcardleft, text='Platform: ',
                             pady=10, padx=20, anchor=E, font=tkfont.Font(
                                 family='MSPGothic', size=12))
        self.platlab.pack(side=TOP, anchor=NW)
        self.faclab = Label(statcardleft, text='Faction: ',
                            pady=10, padx=20, anchor=E, font=tkfont.Font(
                                family='MSPGothic', size=12))
        self.faclab.pack(side=TOP, anchor=NW)
        self.replab = Label(statcardleft, text='Total Reputation:   ',
                            pady=10, padx=20, anchor=E, font=tkfont.Font(
                                family='MSPGothic', size=12))
        self.replab.pack(side=TOP, anchor=NW)
        self.killlab = Label(statcardleft, text='Total Kills:   : ',
                             pady=10, padx=20, anchor=E, font=tkfont.Font(
                                 family='MSPGothic', size=12))
        self.killlab.pack(side=TOP, anchor=NW)
        self.deathlab = Label(statcardleft, text='Total Deaths:   ',
                              pady=10, padx=20, anchor=E, font=tkfont.Font(
                                  family='MSPGothic', size=12))
        self.deathlab.pack(side=TOP, anchor=NW)
        self.assistlab = Label(statcardleft, text='Total Assists:   ',
                               pady=10, padx=20, anchor=E, font=tkfont.Font(
                                   family='MSPGothic', size=12))
        self.assistlab.pack(side=TOP, anchor=NW)
        self.winslab = Label(statcardleft, text='Total Wins:   ',
                             pady=10, padx=20, anchor=E, font=tkfont.Font(
                                 family='MSPGothic', size=12))
        self.winslab.pack(side=TOP, anchor=NW)
        self.losslab = Label(statcardleft, text='Total Losses:   ',
                             pady=10, padx=20, anchor=E, font=tkfont.Font(
                                 family='MSPGothic', size=12))
        self.losslab.pack(side=TOP, anchor=NW)
        self.timelab = Label(statcardleft, text='Time Spent:   ',
                             pady=10, padx=20, anchor=E, font=tkfont.Font(
                                 family='MSPGothic', size=12))
        self.timelab.pack(side=TOP, anchor=NW)

        # again, im sorry. Right side of the statcard.
        statcardright = Frame(panel, relief="sunken",
                              width=200, height=400, pady=10)
        statcardright.pack(side=LEFT, fill=Y, anchor=S)
        statcardright.pack_propagate(0)
        self.kdlab = Label(statcardright, text='K / D Ratio: ',
                           pady=10, padx=20, anchor=E, font=tkfont.Font(
                               family='MSPGothic', size=12))
        self.kdlab.pack(side=TOP, anchor=NW)
        self.wllab = Label(statcardright, text='Win / Loss Ratio: ',
                           pady=10, padx=20, anchor=E, font=tkfont.Font(
                               family='MSPGothic', size=12))
        self.wllab.pack(side=TOP, anchor=NW)

    def point():
        # users the playername variable to find the most recent record of the users stats from the database
        # Since there are multiple entries per player, this is important to prevent duplicates and get the most up to date stats for them
        global playerdata
        playername = playerdata[1]
        cursor.execute(
            "SELECT *, MAX(timePlayed) FROM stat WHERE username = ?", (playername,))
        rows = cursor.fetchall()
        playerdata = rows
        right.update()

    def update(self):
        # Updates Labels. Self Explanatory.
        global playerdata
        self.namelab.config(anchor=E, text="Username:   " + playerdata[0][1])
        self.platlab.config(anchor=E, text="Platform:   " + playerdata[0][2])
        self.faclab.config(anchor=E, text="Faction:   "
                           + str(playerdata[0][3]))
        self.replab.config(
            anchor=E, text="Total Reputation:   " + str(playerdata[0][5]))
        self.killlab.config(
            anchor=E, text="Total Kills:   " + str(playerdata[0][6]))
        self.deathlab.config(
            anchor=E, text="Total Deaths:   " + str(playerdata[0][7]))
        self.assistlab.config(
            anchor=E, text="Total Assists:   " + str(playerdata[0][8]))
        self.winslab.config(
            anchor=E, text="Total Wins:   " + str(playerdata[0][9]))
        self.losslab.config(
            anchor=E, text="Total Losses:   " + str(playerdata[0][10]))
        self.timelab.config(
            anchor=E, text="Time Spent:   " + str(playerdata[0][11]))
        self.kdlab.config(
            anchor=E, text="K / D Ratio:   " + str(round((playerdata[0][6]) / (playerdata[0][7]), 2)))
        self.wllab.config(
            anchor=E, text="Win / Loss Ratio:   " + str(round((playerdata[0][9]) / (playerdata[0][10]), 2)))
        print(playerdata)


#======================== Tab 3 ENTRIES ===============================#

class EntryList(Frame):
    def __init__(self):
        # Initial Setup
        entry = Frame(tab3, relief="raised", bd=3,
                      width=880, height=500, pady=10)
        entry.pack(side=LEFT, fill=Y, anchor=N)
        entry.pack_propagate(0)
        # forcing proper dimensions with propagate

        header = Frame(entry, relief="sunken",
                       width=900, height=200)
        header.pack()
        label = Label(header, text="Recorded Player Data Entry List",
                      pady=10, font=tkfont.Font(
                          family='MSPGothic', size=16, weight="bold"))
        label.pack()
        # Setting up the treeview
        yscroll = Scrollbar(tab3, orient=VERTICAL)
        self.entrylist = ttk.Treeview(entry, columns=("Player ID", "Username", "Platform", "Faction", "UTCSeconds", "Reputation", "Kills", "Deaths", "Assists", "Wins", "Losses", "Time Played"),
                                      selectmode="extended", yscrollcommand=yscroll.set)
        self.entrylist.heading("Player ID", text="Player ID", anchor=W)
        self.entrylist.heading("Username", text="Username", anchor=W)
        self.entrylist.heading("Platform", text="Platform", anchor=W)
        self.entrylist.heading("Faction", text="Faction", anchor=W)
        self.entrylist.heading("UTCSeconds", text="UTCSeconds", anchor=W)
        self.entrylist.heading("Reputation", text="Reputation", anchor=W)
        self.entrylist.heading("Kills", text="Kills", anchor=W)
        self.entrylist.heading("Deaths", text="Deaths", anchor=W)
        self.entrylist.heading("Assists", text="Assists", anchor=W)
        self.entrylist.heading("Wins", text="Wins", anchor=W)
        self.entrylist.heading("Losses", text="Losses", anchor=W)
        self.entrylist.heading("Time Played", text="Time Played", anchor=W)
        self.entrylist.column('#0', stretch=NO, minwidth=0, width=0)
        self.entrylist.column('#1', stretch=NO, minwidth=0, width=60)
        self.entrylist.column('#2', stretch=NO, minwidth=0, width=120)
        self.entrylist.column('#3', stretch=NO, minwidth=0, width=60)
        self.entrylist.column('#4', stretch=NO, minwidth=0, width=60)
        self.entrylist.column('#5', stretch=NO, minwidth=0, width=120)
        self.entrylist.column('#6', stretch=NO, minwidth=0, width=70)
        self.entrylist.column('#7', stretch=NO, minwidth=0, width=40)
        self.entrylist.column('#8', stretch=NO, minwidth=0, width=60)
        self.entrylist.column('#9', stretch=NO, minwidth=0, width=50)
        self.entrylist.column('#10', stretch=NO, minwidth=0, width=50)
        self.entrylist.column('#11', stretch=NO, minwidth=0, width=50)
        self.entrylist.column('#12', stretch=NO, minwidth=0, width=80)
        self.entrylist.pack(expand=True, fill=Y)
        self.entrylist.pack_propagate(0)
        yscroll.config(command=self.entrylist.yview)
        yscroll.pack(side=LEFT, fill=Y)
        yscroll.pack_propagate(0)

        # Button functionality in the header. Add, Delete, Search
        editbutton = Button(
            header, width=15, text="Edit Record", command=self.editrecord)
        editbutton.pack(side=LEFT, anchor=W, padx=10, pady=10)
        addbutton = Button(
            header, width=20, text="Create New Record", command=self.addrecord)
        addbutton.pack(side=LEFT, anchor=W, padx=10, pady=10)
        deletebutton = Button(
            header, width=15, text="Delete Record", command=self.deleterecord)
        deletebutton.pack(side=LEFT, anchor=W, padx=10, pady=10)
        self.searchbar = Entry(header, width=30)
        self.searchbar.pack(side=LEFT, anchor=E, padx=10, pady=10)
        searchbutton = Button(
            header, width=10, text="Search", command=self.search)
        searchbutton.pack(side=LEFT, anchor=W, padx=10, pady=10)

        # Filling the treeview
        cursor.execute("SELECT * FROM stat")
        rows = cursor.fetchall()
        self.update(rows)
        #

    def search(self):
        # handles the searchbar's operation
        for item in self.entrylist.get_children():
            self.entrylist.delete(item)
        inp = self.searchbar.get()
        cursor.execute(
            "SELECT * FROM stat WHERE username LIKE ?", (str(inp) + '%',))
        rows = cursor.fetchall()
        self.update(rows)

    def update(self, rows):
        # Updates the player list treeview

        for row in rows:
            # Populates tree with specific player data
            self.entrylist.insert(parent="", index='end', values=(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))

 #---------------- EDIT RECORD -------------------------#

    # Handles most of CRUD
    # Edit record function, add record function, delete record function

    def editrecord(self):
        def verifyedit():
            entry_list = [entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get(
            ), entry7.get(), entry8.get(), entry9.get(), entry10.get(), entry11.get(), entry12.get()]
            if len(entry_list) == 12:
                if '' not in entry_list:
                    statuslabel.config(
                        text="Status: Valid Entry")
                    query = """
                    UPDATE stat
                    SET playerID=?, platform=?, faction=?, UTCSeconds=?, reputation=?, kills=?, deaths=?, assists=?, wins=?, losses=?, timeplayed=?
                    WHERE username=?
                    """
                    entry_list.append(entry_list.pop(
                        1))  # Move username to end of list
                    cursor.execute(query, entry_list)
                    conn.commit()
                    cursor.execute("SELECT * FROM stat")
                    rows = cursor.fetchall()
                    self.update(rows)
                    messagebox.showinfo(
                        "Confirmation", "Your record has been modified.")
            pass

        answer = askyesno(title='Modify Confirmation - Disclaimer',
                          message="Editing records can negatively affect the accuracy of the database and harm its legitimacy as an information source. \n\nThis operation should only be performed for testing and should be reverted soon afterward to ensure proper data preservation. \n\nAre you sure you wish to Modify an existing record?")
        if answer:
            highlighted_entry = self.entrylist.selection()
            value = self.entrylist.item(highlighted_entry, 'values')
            username = value[1]
            cursor.execute("SELECT * FROM stat WHERE username =?", (username,))
            rows = cursor.fetchall()
            top = Toplevel(win)
            top.geometry("250x670")
            top.title("Edit Existing Data Record")
            label1 = Label(top, text="Player ID")
            label1.pack(side=TOP)
            entry1 = Entry(top, width=25)
            entry1.pack(side=TOP, pady=5)
            entry1.insert(0, rows[0][0])

            label2 = Label(top, text="Username")
            label2.pack(side=TOP)
            entry2 = Entry(top, width=25)
            entry2.pack(side=TOP, pady=5)
            entry2.insert(0, rows[0][1])

            label3 = Label(top, text="Platform")
            label3.pack(side=TOP)
            entry3 = Entry(top, width=25)
            entry3.pack(side=TOP, pady=5)
            entry3.insert(0, rows[0][2])

            label4 = Label(top, text="Faction")
            label4.pack(side=TOP)
            entry4 = Entry(top, width=25)
            entry4.pack(side=TOP, pady=5)
            entry4.insert(0, rows[0][3])

            label5 = Label(top, text="UTCSeconds")
            label5.pack(side=TOP)
            entry5 = Entry(top, width=25)
            entry5.pack(side=TOP, pady=5)
            entry5.insert(0, rows[0][4])

            label6 = Label(top, text="Reputation")
            label6.pack(side=TOP)
            entry6 = Entry(top, width=25)
            entry6.pack(side=TOP, pady=5)
            entry6.insert(0, rows[0][5])

            label7 = Label(top, text="Kills")
            label7.pack(side=TOP)
            entry7 = Entry(top, width=25)
            entry7.pack(side=TOP, pady=5)
            entry7.insert(0, rows[0][6])

            label8 = Label(top, text="Deaths")
            label8.pack(side=TOP)
            entry8 = Entry(top, width=25)
            entry8.pack(side=TOP, pady=5)
            entry8.insert(0, rows[0][7])

            label9 = Label(top, text="Assists")
            label9.pack(side=TOP)
            entry9 = Entry(top, width=25)
            entry9.pack(side=TOP, pady=5)
            entry9.insert(0, rows[0][8])

            label10 = Label(top, text="Wins")
            label10.pack(side=TOP)
            entry10 = Entry(top, width=25)
            entry10.pack(side=TOP, pady=5)
            entry10.insert(0, rows[0][9])

            label11 = Label(top, text="Losses")
            label11.pack(side=TOP)
            entry11 = Entry(top, width=25)
            entry11.pack(side=TOP, pady=5)
            entry11.insert(0, rows[0][10])

            label12 = Label(top, text="Time Played")
            label12.pack(side=TOP)
            entry12 = Entry(top, width=25)
            entry12.pack(side=TOP, pady=5)
            entry12.insert(0, rows[0][11])

            gobutton = Button(top, width=10, text="Edit Record",
                              command=verifyedit)
            gobutton.pack(side=TOP, pady=5)
            statuslabel = Label(top, text="Status: ")
            statuslabel.pack(side=BOTTOM, pady=5)
        pass

 #---------------- ADD / CREATE RECORD -------------------------#

    def addrecord(self):

        def verifyadd():
            # Gets all fields of the input boxes, then verifies if they are not blank
            entry_list = [entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get(
            ), entry7.get(), entry8.get(), entry9.get(), entry10.get(), entry11.get(), entry12.get()]
            if len(entry_list) == 12:
                if '' not in entry_list:
                    statuslabel.config(
                        text="Status: Valid Entry")
                    cursor.execute(
                        "INSERT INTO stat (playerID, username, platform, faction, UTCSeconds, reputation, kills, deaths, assists, wins, losses, timeplayed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entry_list)
                    conn.commit()
                    cursor.execute("SELECT * FROM stat")
                    rows = cursor.fetchall()
                    self.update(rows)
                    messagebox.showinfo(
                        "Confirmation", "Your record has been created.")

        # Actual addrecord function begins here
        answer = askyesno(title='Add Confirmation - Disclaimer',
                          message="Adding records can negatively affect the accuracy of the database and harm its legitimacy as an information source. \n\nDo not use this function to alter statistics outside of isolated testing. \n\nAre you sure you wish to create a new record?")
        if answer:
            top = Toplevel(win)
            top.geometry("250x670")
            top.title("New Data Entry Field")
            label1 = Label(top, text="Player ID")
            label1.pack(side=TOP)
            entry1 = Entry(top, width=25)
            entry1.pack(side=TOP, pady=5)
            label2 = Label(top, text="Username")
            label2.pack(side=TOP)
            entry2 = Entry(top, width=25)
            entry2.pack(side=TOP, pady=5)
            label3 = Label(top, text="Platform")
            label3.pack(side=TOP)
            entry3 = Entry(top, width=25)
            entry3.pack(side=TOP, pady=5)
            label4 = Label(top, text="Faction")
            label4.pack(side=TOP)
            entry4 = Entry(top, width=25)
            entry4.pack(side=TOP, pady=5)
            label5 = Label(top, text="UTCSeconds")
            label5.pack(side=TOP)
            entry5 = Entry(top, width=25)
            entry5.pack(side=TOP, pady=5)
            label6 = Label(top, text="Reputation")
            label6.pack(side=TOP)
            entry6 = Entry(top, width=25)
            entry6.pack(side=TOP, pady=5)
            label7 = Label(top, text="Kills")
            label7.pack(side=TOP)
            entry7 = Entry(top, width=25)
            entry7.pack(side=TOP, pady=5)
            label8 = Label(top, text="Deaths")
            label8.pack(side=TOP)
            entry8 = Entry(top, width=25)
            entry8.pack(side=TOP, pady=5)
            label9 = Label(top, text="Assists")
            label9.pack(side=TOP)
            entry9 = Entry(top, width=25)
            entry9.pack(side=TOP, pady=5)
            label10 = Label(top, text="Wins")
            label10.pack(side=TOP)
            entry10 = Entry(top, width=25)
            entry10.pack(side=TOP, pady=5)
            label11 = Label(top, text="Losses")
            label11.pack(side=TOP)
            entry11 = Entry(top, width=25)
            entry11.pack(side=TOP, pady=5)
            label12 = Label(top, text="Time Played")
            label12.pack(side=TOP)
            entry12 = Entry(top, width=25)
            entry12.pack(side=TOP, pady=5)
            gobutton = Button(top, width=10, text="Add Record",
                              command=verifyadd)
            gobutton.pack(side=TOP, pady=5)
            statuslabel = Label(top, text="Status: ")
            statuslabel.pack(side=BOTTOM, pady=5)

 #---------------- DELETE RECORD -------------------------#

    def deleterecord(self):
        answer = askyesno(title='Deletion Confirmation - Disclaimer',
                          message="Deleting records can negatively affect the accuracy of the database and harm its legitimacy as an information source. \n\nThis operation should only be performed for testing and should be reverted soon afterward to ensure proper data preservation. \n\nAre you sure you wish to Delete an existing record?")
        if answer:
            answer = askyesno(title='Confirm Deletion?',
                              message="All highlighted records will be permanently deleted upon confirmation. Are you sure about this?")
            if answer:
                highlighted_ids = self.entrylist.selection()
                for item_id in highlighted_ids:
                    values = self.entrylist.item(item_id, 'values')
                    username = values[1]
                    cursor.execute(
                        "DELETE FROM stat WHERE username = ?", (username,))
                    conn.commit()
                self.entrylist.delete(*highlighted_ids)

        cursor.execute("SELECT * FROM stat")
        rows = cursor.fetchall()
        self.update(rows)

#======================== INSTANTIATING ===============================#


left = PlayerList()
right = PlayerData()
EntryList()
win.config(menu=main)
win.mainloop()
