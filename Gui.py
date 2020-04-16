
# -*- coding: utf-8 -*-

import tkinter
from tkinter import MULTIPLE
from tkinter import Button,Label
from tkinter import Frame
from tkinter import ttk
from Data import Models_Data

class App:
    def __init__(self,master):
        self.master = master
        self.mylist=tkinter.Listbox(self.master,width=40,selectmode=MULTIPLE) 
        self.data = Models_Data()
        self.one = self.data.get_Requirements() 
        self.two = ""  # second panel
        self.three=""  # third panel
        self.tree = ""
        self.result=[]
        self.state = 1
        self.initGui()

    def initGui(self):
        # mylist=tkinter.Listbox(self.master,width=40,selectmode=MULTIPLE) 
        self.mylist.pack()
        for  item  in self.one: #insert the content
            self.mylist.insert(tkinter.END,item) 

        frameButton = Frame(self.master).pack(anchor='s')
        select=ttk.Button(frameButton, text='select', width=8,command=self.select_Button)
        select.pack(side='left',padx=20)
        forward=ttk.Button(frameButton, text='forward', width=8,command=self.forward_Button)
        forward.pack(side='left',padx=20)
        submit=ttk.Button(frameButton, text='submit', width=8,command=self.submit_Button)
        submit.pack(side='left',padx=20)

    def forward_Button(self):
        if self.state==2:
            forward_item =self.one
        elif self.state==3:
            forward_item = self.two
        else:
            return
        self.mylist.delete(0,self.mylist.size())
        for item in forward_item: #insert the content
            self.mylist.insert(tkinter.END,item) 
        self.state-=1

    def treeviewClick(self,event):
        for item in self.tree.selection():
            item_text = self.tree.item(item,"values")
            temp = item_text[1]
            tempid = int(item_text[0])
            if temp in self.label['text']:
                templist = self.label['text'].split(",")
                templist.remove(temp)
                self.label['text']=",".join(templist)
                self.result = list(set(self.result))
                self.result.remove(tempid)
            else:
                self.label['text']+=temp+","
                self.result.append(tempid)


    def select_Last(self,ids):
        securityActivity = tkinter.Tk()
        m_ids = []
        securityActivity.title("securityActivity")
        label = Label(securityActivity,text="")
        tree = ttk.Treeview(securityActivity)      # #creat table ob
        tree["columns"] = ("id","securityActivity", "cost","maintenance","efficiency")     # define the column
        self.tree = tree
        self.label=label
        for n,i in enumerate(tree["columns"]):
            tree.column(i, width=100,anchor='center')
            tree.heading(i, text=i)
        results = self.data.get_OtherData(ids,2)
        for n,i in enumerate(results):
            tree.insert("",n,text=n+1,value=(i.getMess()))
            m_ids.append(i.id)
        # print(m_ids)
        tree.heading("cost",text="cost",command=lambda :self.sort(tree,"cost",False,False,m_ids))
        tree.heading("maintenance",text="maintenance",command=lambda :self.sort(tree,"maintenance",False,False,m_ids))
        tree.heading("efficiency",text="efficiency",command=lambda :self.sort(tree,"efficiency",False,False,m_ids))
        tree.bind('<Double-1>', self.treeviewClick)
        label.pack()
        tree.pack()
        securityActivity.mainloop()


    def select_Button(self):
        selects = self.mylist.curselection()#get the value
        tempList=[]
        for i in selects:
            if self.state==1:
                tempList.append(self.one[i].id)
            elif self.state==2:
                tempList.append(self.two[i].id)
                # return
                # tempList.append(self.two[i].id)
            # elif self.state==3:
            #     self.result.append(self.three[i].id)
        if self.state==3:
            return
        if self.state==2:
            self.select_Last(tempList)
            return
        self.mylist.delete(0,self.mylist.size())
        next_Data = self.data.get_OtherData(tempList,self.state)

        if self.state==1:
            self.two = next_Data
        elif self.state==2:
            self.three = next_Data

        for item in next_Data: #insert the content
            self.mylist.insert(tkinter.END,item) 
        self.state+=1


    def sort(self,tree,col,reverse,flag=True,ids=""):
        # print(col)
        # print(reverse)
        [tree.delete(item) for item in tree.get_children()]
        if flag:
            results = self.data.get_SecurityActivities(self.result,col=col,reverse=reverse)
        else:
            results = self.data.get_SecurityActivities(ids,col=col,reverse=reverse)

        for n,i in enumerate(results):
            if flag:
                tempValue = i.getInfo()
            else:
                tempValue = i.getMess()
            tree.insert("",n,text=n+1,value=(tempValue))
        if flag:
            tree.heading(col,text=col,command=lambda :self.sort(tree,col,not reverse))
        else:
            tree.heading(col,text=col,command=lambda :self.sort(tree,col,not reverse,flag,ids))


    def submit_Button(self):
        res = tkinter.Tk()
        res.title("Final Choice")
        tree = ttk.Treeview(res)      # #creat the table ob
        tree["columns"] = ("requirement", "defense", "securityActivity", "cost","maintenance","efficiency")   #define the Column
        for n,i in enumerate(tree["columns"]):
            tree.column(i, width=100,anchor='center')
            tree.heading(i, text=i)
        tree.heading("cost",text="cost",command=lambda :self.sort(tree,"cost",False))
        tree.heading("maintenance",text="maintenance",command=lambda :self.sort(tree,"maintenance",False))
        tree.heading("efficiency",text="efficiency",command=lambda :self.sort(tree,"efficiency",False))
        results = self.data.get_SecurityActivities(self.result)
        for n,i in enumerate(results):
            tree.insert("",n,text=n+1,value=(i.getInfo()))
        tree.pack()
        res.mainloop()


if __name__ == '__main__':
    win=tkinter.Tk() #creat the window
    win.title("Selection interface")
    App(win)
    win.mainloop() #enter the loop

