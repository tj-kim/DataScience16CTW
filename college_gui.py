import Tkinter as tk
import college as c
import college_map as cm

class College(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryvr = tk.StringVar()
        self.labelvr = tk.StringVar()

        self.entrywr = tk.StringVar()
        self.labelwr = tk.StringVar()

        self.entrymt = tk.StringVar()
        self.labelmt = tk.StringVar()

        self.entrymc = tk.StringVar()
        self.labelmc = tk.StringVar()

        self.optiondiv = tk.StringVar()
        self.labeldiv = tk.StringVar()

        self.optionpp = tk.StringVar()
        self.labelpp = tk.StringVar()

        self.entrymajor = tk.StringVar()
        self.labelmajor = tk.StringVar()

        self.entrypop = tk.StringVar()
        self.optionpop= tk.StringVar()
        self.labelpop = tk.StringVar()

        self.label_SATVR = tk.Label(self,textvariable=self.labelvr)
        self.label_SATVR.grid(column=0,row=0,sticky='W')
        self.labelvr.set("SAT Reading")
        self.entry_SATVR = tk.Entry(self,textvariable=self.entryvr)
        self.entry_SATVR.grid(column=1,columnspan = 2, row=0,sticky='EW')

        self.label_SATWR = tk.Label(self,textvariable=self.labelwr)
        self.label_SATWR.grid(column=0,row=1,sticky='W')
        self.labelwr.set("SAT Writing")
        self.entry_SATWR = tk.Entry(self,textvariable=self.entrywr)
        self.entry_SATWR.grid(column=1,columnspan = 2,row=1,sticky='EW')

        self.label_SATMT = tk.Label(self,textvariable=self.labelmt)
        self.label_SATMT.grid(column=0,row=2,sticky='W')
        self.labelmt.set("SAT Math")
        self.entry_SATMT = tk.Entry(self,textvariable=self.entrymt)
        self.entry_SATMT.grid(column=1,columnspan = 2,row=2,sticky='EW')

        #Diversity
        self.labeldiv.set("Diversity")
        div = ['high','medium','low']
        self.label_div = tk.Label(self,textvariable=self.labeldiv)
        self.label_div.grid(column=0,row=3,sticky='W')
        self.optiondiv.set(div[0])
        self.option_div = tk.OptionMenu(self, self.optiondiv, *div)
        self.option_div.grid(column=1,columnspan = 2,row=3,sticky='EW')

        #Public Private
        self.labelpp.set("Public/Private")
        pp = ['both', 'public', 'private']
        self.label_pp = tk.Label(self,textvariable=self.labelpp)
        self.label_pp.grid(column=0,row=4,sticky='W')
        self.optionpp.set(pp[0])
        self.option_pp = tk.OptionMenu(self, self.optionpp, *pp)
        self.option_pp.grid(column=1,columnspan = 2,row=4,sticky='EW')

        #Maximum Cost
        self.labelmc.set("Maximum Cost")
        self.label_MC = tk.Label(self,textvariable=self.labelmc)
        self.label_MC.grid(column=0,row=5,sticky='W')
        self.entry_MC = tk.Entry(self,textvariable=self.entrymc)
        self.entry_MC.grid(column=1,columnspan = 2, row=5,sticky='EW')

        #Major
        self.labelmajor.set("Major")
        self.label_major = tk.Label(self,textvariable=self.labelmajor)
        self.label_major.grid(column=0,row=6,sticky='W')
        self.entrymajor.set(u'separate different major by ;')
        self.entry_major = tk.Entry(self,textvariable=self.entrymajor)
        self.entry_major.grid(column=1,columnspan = 2, row=6,sticky='EW')

        #Population
        pop = ['less than','more than']
        self.labelpop.set("Population")
        self.label_pop = tk.Label(self,textvariable=self.labelpop)
        self.label_pop.grid(column=0,row=7,sticky='W')
        self.optionpop.set(pop[0])
        self.option_pop = tk.OptionMenu(self, self.optionpop, *pop)
        self.option_pop.grid(column=1,row=7,sticky='EW')
        self.entry_pop = tk.Entry(self,textvariable=self.entrypop)
        self.entry_pop.grid(column=2,row=7,sticky='EW')



        button = tk.Button(self,text=u"Search",
                                command=self.OnButtonClick)
        button.grid(column=1,row=10)

        # self.entry.bind("<Return>", self.OnPressEnter)
        # self.entryVariable.set(u"Enter text here.")

        # self.resultVariable = tk.StringVar()
        # self.result = tk.Label(self,textvariable=self.resultVariable,
        #                       anchor="w",fg="Black", bg = 'White')
        # self.result.grid(column=0,row=5,columnspan=2,sticky='EW')
        # self.resultVariable.set(u"Result")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        # self.resultVariable.set('Reading:'+self.entry_SATVR.get()+'Writing:'+self.entry_SATWR.get()+'Math:'+self.entry_SATMT.get())
        self.update()
        self.geometry(self.geometry())       

    def OnButtonClick(self):
        collegelist =  c.get_result(
            vr = float(self.entry_SATVR.get()), 
            wr = float(self.entry_SATWR.get()), 
            mt = float(self.entry_SATMT.get()),
            pubprv = self.optionpp.get(),
            div = self.optiondiv.get(),
            maxcost = float(self.entry_MC.get()),
            majstr = self.entry_major.get(),
            pop = float(self.entry_pop.get()),
            popchoice = self.optionpop.get()
            )
        # self.resultVariable.set(flist)
        cm.build_map(collegelist)

if __name__ == "__main__":
    app = College(None)
    app.title('college planner')
    app.mainloop()
