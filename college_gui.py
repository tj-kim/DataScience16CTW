import Tkinter as tk
import college as c

class College(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryvrVariable = tk.StringVar()
        self.entrywrVariable = tk.StringVar()
        self.entrymtVariable = tk.StringVar()
        self.labelvrVariable = tk.StringVar()
        self.labelwrVariable = tk.StringVar()
        self.labelmtVariable = tk.StringVar()

        self.label_SATVR = tk.Label(self,textvariable=self.labelvrVariable)
        self.label_SATVR.grid(column=0,row=0,sticky='W')
        self.labelvrVariable.set("SAT Reading")
        self.entry_SATVR = tk.Entry(self,textvariable=self.entryvrVariable)
        self.entry_SATVR.grid(column=1,row=0,sticky='EW')

        self.label_SATWR = tk.Label(self,textvariable=self.labelwrVariable)
        self.label_SATWR.grid(column=0,row=1,sticky='W')
        self.labelwrVariable.set("SAT Writing")
        self.entry_SATWR = tk.Entry(self,textvariable=self.entrywrVariable)
        self.entry_SATWR.grid(column=1,row=1,sticky='EW')

        self.label_SATMT = tk.Label(self,textvariable=self.labelmtVariable)
        self.label_SATMT.grid(column=0,row=2,sticky='W')
        self.labelmtVariable.set("SAT Math")
        self.entry_SATMT = tk.Entry(self,textvariable=self.entrymtVariable)
        self.entry_SATMT.grid(column=1,row=2,sticky='EW')

        button = tk.Button(self,text=u"Search",
                                command=self.OnButtonClick)
        button.grid(column=1,row=3)

        # self.entry.bind("<Return>", self.OnPressEnter)
        # self.entryVariable.set(u"Enter text here.")

        self.resultVariable = tk.StringVar()
        self.result = tk.Label(self,textvariable=self.resultVariable,
                              anchor="w",fg="Black", bg = 'White')
        self.result.grid(column=0,row=5,columnspan=2,sticky='EW')
        self.resultVariable.set(u"Result")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.resultVariable.set('Reading:'+self.entry_SATVR.get()+'Writing:'+self.entry_SATWR.get()+'Math:'+self.entry_SATMT.get())
        self.update()
        self.geometry(self.geometry())       

    def OnButtonClick(self):
        flist =  c.get_result(float(self.entry_SATVR.get()), float(self.entry_SATWR.get()), float(self.entry_SATMT.get()))
        self.resultVariable.set(flist)

if __name__ == "__main__":
    app = College(None)
    app.title('college planner')
    app.mainloop()
