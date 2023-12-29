from email.mime.image import MIMEImage
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
from tkinter import Spinbox
from tkinter import OptionMenu
import json
from tkinter.ttk import Combobox
import xml
import traceback
from datetime import datetime
import subprocess
import sys
import xml.etree.ElementTree as ET
import json
import os
ROOT_DIR = os.path.abspath(os.curdir)

#Json read
def read_file(path):
    with open(path, "r") as rf:
        values = json.load(rf)
    return values

MOI_json = read_file('./MOI.json')
settings_json = read_file('./settings.json')
SelectedTC = read_file('./Testcase.json')
Testcnf = read_file('./TestConfig.json')
chapterslist = []

for chap in Testcnf:
    if len(Testcnf[chap]) != 0:
        chapterslist.append(chap)
# print(chapterslist)

#--- functions -----
parent = Tk()  
parent.title("C2 Test Automation")
parent.geometry("1200x500")  
parent.resizable(False,False)
bg = PhotoImage(file = "./img/bg.png")

Goldenjsonpath = StringVar()
Goldenjsonpath.set(settings_json['Golden_path'])
GenProjectpath = StringVar()
GenProjectpath.set(settings_json['Generated_path'])

TesterIP =StringVar()
TesterIP.set(settings_json['TesterInfo']['TesterIP'])

VifPaths =StringVar()
VifPaths.set(settings_json['TesterInfo']['VIFPath'])

ProjectName =StringVar()
ProjectName.set(settings_json['TesterInfo']['ProjectName'])

myFont = font.Font(family='Calibri', size=14, weight='bold')
myFont_value = font.Font(family='Calibri', size=14)
myFont_value2 = font.Font(family='Calibri', size=12)
myFont_value3 = font.Font(family='Calibri', size=10)

#---Add frame---
SM1_frame = Frame(parent,height=500,width=100,bg="#23275C", bd=1,relief=FLAT)
SM1_frame.place(x=0,y=0)
SM2_frame = Frame(parent,height=500,width=150,bg="#FFFFFF", bd=1,relief=FLAT)
SM2_frame.place(x=100,y=0)
SM3_frame = Frame(parent,height=500,width=550,bg="#D9D9D9", bd=1,relief=FLAT)
SM3_frame.place(x=250,y=0)
MOIALL = IntVar()
MOIPDM = IntVar()
MOIUSBC = IntVar()
MOISPT = IntVar()
MOIQC3 = IntVar()
MOIQC4 = IntVar()
MOITPT = IntVar()
MOIDP = IntVar()
MOIOEM = IntVar()
MOIQC3v12 = IntVar()
MOIIEC = IntVar()

ChapAll = IntVar()
ChPHY = IntVar()
ChPROT = IntVar()
ChPOW = IntVar()
ChEPOW = IntVar()
ChFRS = IntVar()
ChUSB4 = IntVar()


selectedtc = StringVar()
selectedtc.set("--")
Tesecaselist = StringVar()

CLAll = IntVar()
CL1A = IntVar()
CL1F = IntVar()

CLRUNAll = IntVar()
CLRUN1A = IntVar()
CLRUN1F = IntVar()

#controls--start
def XMLcomparsion():
    os.system('py ./CompareDetails.py')
    messagebox.showinfo("Update info", "Report Generated!.")

def XMLsummary():
    os.system('py ./summary.py')
    messagebox.showinfo("Update info", "Report Generated!.")
#---create UI for Input path
def open_file():
    global Grespath
    filename = filedialog.askopenfile(mode='r', filetypes=[('JSON Files', '*.json')])
    if filename:
        Grespath.set(filename.name)

def open_file_json():
    global Projectpath
    #global TClistFromJson
    filename = filedialog.askopenfile(mode='r', filetypes=[('JSON Files', '*.json')])
    if filename:
        Projectpath.set(filename.name)
    #update to json
    path = str(Projectpath.get()).replace('/',"\\")
    settings_json['Golden_path']=path
    with open('settings.json', "w") as outfile:
        json.dump(settings_json, outfile)
    #createoffValUI()
    messagebox.showinfo("Update info", "Project Path :"+path+" has been updated.")

def open_file_Goldjson(UpdtElmt):
    filename = filedialog.askopenfile(mode='r', filetypes=[('XML Files', '*.xml')])
    if filename:
        UpdtElmt.set(filename.name)
    #update to json
    path = str(UpdtElmt.get()).replace('/',"\\")
    settings_json['Golden_path']=path
    with open('settings.json', "w") as outfile:
       json.dump(settings_json, outfile)
    messagebox.showinfo("Update info", "Golden Json file :"+path+" has been updated.")

def open_file_Generatedjson(UpdtElmt):
    filename = filedialog.askopenfile(mode='r', filetypes=[('XML Files', '*.xml')])
    if filename:
        UpdtElmt.set(filename.name)
    #update to json
    path = str(UpdtElmt.get()).replace('/',"\\")
    settings_json['Generated_path'] = path
    with open('settings.json', "w") as outfile:
       json.dump(settings_json, outfile)
    messagebox.showinfo("Update info", "Generated Json file :"+path+" has been updated.")

#---XML file input from user---
def createJsonCompUI():
    if len(SM3_frame.winfo_children()) > 0:
        for wdgt in SM3_frame.winfo_children():
            wdgt.destroy()
    Label(SM3_frame,text="Generated XML Path:",width=10,font=myFont).grid(row=1,column=1)
    Entry(SM3_frame,textvariable=GenProjectpath,width=40,font=myFont_value).grid(row=1,column=2)
    Button(SM3_frame, text="Browse",font=myFont, command=lambda: open_file_Generatedjson(GenProjectpath)).grid(row=1,column=3)
    #Label(SM3_frame,text="*Defaulty updated with Recently ran tests project path",font=myFont_value3).grid(row=2,column=2)

    Label(SM3_frame,text="Golden XML Path:",width=10,font=myFont).grid(row=3,column=1)
    Entry(SM3_frame,textvariable=Goldenjsonpath,width=40,font=myFont_value).grid(row=3,column=2)
    Button(SM3_frame, text="Browse",font=myFont, command=lambda: open_file_Goldjson(Goldenjsonpath)).grid(row=3,column=3)
    Button(SM3_frame,text="XML Comparison",font=myFont, command=XMLcomparsion).grid(row=5,column=2)
    Button(SM3_frame,text="XML Summary",font=myFont, command=XMLsummary).grid(row=6,column=2)

#--SM1 Button functions-------------------------------
def loadipbtn():
    if len(SM2_frame.winfo_children()) > 0:
        for wdgt in SM2_frame.winfo_children():
            wdgt.destroy()
    if len(SM3_frame.winfo_children()) > 0:
        for wdgt in SM3_frame.winfo_children():
            wdgt.destroy()
    TCIP_btn = Button(SM2_frame,text="Test Inputs",bd=1,background="#FFFFFF", command=createTestInput)
    TCIP_btn.place(x=0,y=1,width=150,height=30)
    path_btn = Button(SM2_frame,text="Update Paths",bd=1,background="#FFFFFF")
    path_btn.place(x=0,y=30,width=150,height=30)


def createTestInput():
    if len(SM3_frame.winfo_children()) > 0:
        for wdgt in SM3_frame.winfo_children():
            wdgt.destroy()
    Label(SM3_frame,text="Tester IP:",width=10,font=myFont).grid(row=1,column=1)
    Entry(SM3_frame,textvariable=TesterIP,width=40,font=myFont_value).grid(row=1,column=2)
    Label(SM3_frame,text="VIF Path:",width=10,font=myFont).grid(row=2,column=1)
    Entry(SM3_frame,textvariable=VifPaths,width=40,font=myFont_value).grid(row=2,column=2)
    Label(SM3_frame,text="Project Name:",width=10,font=myFont).grid(row=3,column=1)
    Entry(SM3_frame,textvariable=ProjectName,width=40,font=myFont_value).grid(row=3,column=2)

    Button(SM3_frame,text="Connect",font=myFont,command=SaveTesterinfo).grid(row=1,column=4)
    Button(SM3_frame, text="Load VIF",font=myFont, command=lambda: open_file_VIFfile(VifPaths)).grid(row=2,column=4)
    Button(SM3_frame, text="Save",font=myFont, command=lambda: SaveProjectinfo(ProjectName)).grid(row=3,column=4)

#Project Name    
def SaveProjectinfo(ProjectName):
    global settings_json
    settings_json['TesterInfo']['ProjectName'] = str(ProjectName.get())

    with open('settings.json','w') as outfile:
        json.dump(settings_json,outfile)
    messagebox.showinfo("Update info","Project Name Updated") 


#Tester info
def SaveTesterinfo():
    global settings_json
    settings_json['TesterInfo']['TesterIP'] = str(TesterIP.get())

    with open('settings.json','w') as outfile:
        json.dump(settings_json,outfile)
    messagebox.showinfo("Update info","Tester IP Address updated") 

#Vif path
def open_file_VIFfile(UpdtElmt):
    filename = filedialog.askopenfile(mode='r', filetypes=[('XML Files', '*.xml')])
    if filename:
        UpdtElmt.set(filename.name)
    #update to json
    path = str(UpdtElmt.get()).replace('/',"\\")
    settings_json['TesterInfo']['VIFPath']=path
    #get DUT type
    treeVIF = ET.parse(path)
    GDroot = treeVIF.getroot()
    for child in GDroot[9]:
    # print(child.tag)
        if 'PD_Port_Type' in child.tag:
            settings_json['TesterInfo']['DUTType'] = child.text
    with open('settings.json', "w") as outfile:
       json.dump(settings_json, outfile)
    messagebox.showinfo("Update info", "VIF file :"+path+" has been updated.")
    

def loadrunbtn():
    if len(SM2_frame.winfo_children()) > 0:
        for wdgt in SM2_frame.winfo_children():
            wdgt.destroy()
    if len(SM3_frame.winfo_children()) > 0:
        for wdgt in SM3_frame.winfo_children():
            wdgt.destroy()
    path_btn = Button(SM2_frame,text="Test Selection",bd=1,background="#FFFFFF",font=myFont,command=MOIselection)
    path_btn.place(x=0,y=0,width=150,height=30)
    ListTC_btn = Button(SM2_frame,text="List Tests",bd=1,background="#FFFFFF",font=myFont,command=Testcaseselection)
    ListTC_btn.place(x=0,y=30,width=150,height=30)
    RunTC_btn = Button(SM2_frame,text="Run Test",bd=1,background="#FFFFFF",font=myFont,command=RUNTests)
    RunTC_btn.place(x=0,y=60,width=150,height=30)
                    
def ALL_MOI():
    if MOIALL.get() == 1:    
        MOIPDM.set(1)
        MOIUSBC.set(1)
        MOISPT.set(1)
        MOIQC3.set(1)
        MOIQC4.set(1)
        MOITPT.set(1)
        MOIDP.set(1)
        MOIOEM.set(1)
        MOIQC3v12.set(1)
        MOIIEC.set(1)
    else:
        MOIPDM.set(0)
        MOIUSBC.set(0)
        MOISPT.set(0)
        MOIQC3.set(0)
        MOIQC4.set(0)
        MOITPT.set(0)
        MOIDP.set(0)
        MOIOEM.set(0)
        MOIQC3v12.set(0)
        MOIIEC.set(0)

def deselect_ALL():
    MOIALL.set(0) if 0 in [MOIPDM.get(),MOIUSBC.get(),MOISPT.get(),MOIQC3.get(),MOIQC4.get(),MOITPT.get(),MOIDP.get(),MOIOEM.get(),MOIQC3v12.get(),MOIIEC.get()] else  MOIALL.set(1)

def loadrpbtn():
    if len(SM2_frame.winfo_children()) > 0:
        for wdgt in SM2_frame.winfo_children():
            wdgt.destroy()
    if len(SM3_frame.winfo_children()) > 0:
        for wdgt in SM3_frame.winfo_children():
            wdgt.destroy()
    GenRep_btn =  Button(SM2_frame,text="Generate",bd=1,background="#FFFFFF",font=myFont)
    GenRep_btn.place(x=0,y=1,width=150,height=30)
    OffVal_btn = Button(SM2_frame,text="Offline Validation",bd=1,background="#FFFFFF",font=myFont)
    OffVal_btn.place(x=0,y=30,width=150,height=30)
    Button(SM2_frame,text="XML Comparison",bd=1,background="#FFFFFF",font=myFont,command=createJsonCompUI).place(x=0,y=60,width=150,height=30)

def MOIselection():
    if len(SM3_frame.winfo_children()) > 0:
        for wdgt in SM3_frame.winfo_children():
            wdgt.destroy()
    PhaseLB = Label(SM3_frame,text="Select MOI :",font=myFont).grid(row=1,column=1)
    SM3_phase_frame = Frame(SM3_frame,height=5,width=37,relief=FLAT)
    SM3_phase_frame.grid(row=1,column=2,columnspan=1)
    Checkbutton(SM3_phase_frame,text='ALL',font=myFont_value2,variable=MOIALL,command=ALL_MOI).grid(row=1,column=1,sticky=W)
    Checkbutton(SM3_phase_frame,text='Power Delivery 3.1 Tests ',font=myFont_value2,variable=MOIPDM,command=deselect_ALL).grid(row=2,column=1,sticky=W)
    Checkbutton(SM3_phase_frame,text='USB-C Functional',font=myFont_value2,variable=MOIUSBC,command=deselect_ALL).grid(row=3,column=1,sticky=W)
    Checkbutton(SM3_phase_frame,text='Source Power Tests',font=myFont_value2,variable=MOISPT,command=deselect_ALL).grid(row=4,column=1,sticky=W)
    Checkbutton(SM3_phase_frame,text='Quick Charger 3.0',font=myFont_value2,variable=MOIQC3,command=deselect_ALL).grid(row=2,column=2,sticky=W)
    Checkbutton(SM3_phase_frame,text='Quick Charge 4',font=myFont_value2,variable=MOIQC4,command=deselect_ALL).grid(row=3,column=2,sticky=W)
    Checkbutton(SM3_phase_frame,text='Thunderbolt Power Tests',font=myFont_value2,variable=MOITPT,command=deselect_ALL).grid(row=4,column=2,sticky=W)
    Checkbutton(SM3_phase_frame,text='DisplayPort Alternate Mode',font=myFont_value2,variable=MOIDP,command=deselect_ALL).grid(row=5,column=2,sticky=W)
    Checkbutton(SM3_phase_frame,text='Custom OEM Tests-v1.0',font=myFont_value2,variable=MOIOEM,command=deselect_ALL).grid(row=2,column=3,sticky=W)
    Checkbutton(SM3_phase_frame,text='QC3+ Tests-v1.2',font=myFont_value2,variable=MOIQC3v12,command=deselect_ALL).grid(row=3,column=3,sticky=W)
    Checkbutton(SM3_phase_frame,text='IEC Functional Safety Tests',font=myFont_value2,variable=MOIIEC,command=deselect_ALL).grid(row=4,column=3,sticky=W)

    TC_btn = Button(SM3_frame,text="Generate Tests",font=myFont, command=GenerateTCexe).grid(row=3,column=2)

def GenerateTCexe():
    global TCP_values
    MOI =[]
    #get selected MOI
    if MOIPDM.get() ==1 : MOI.append('1')
    if MOIUSBC.get() ==1 : MOI.append('2')
    if MOISPT.get() ==1 : MOI.append('3')
    if MOIQC3.get() ==1 : MOI.append('4')
    if MOIQC4.get() ==1 : MOI.append('5')
    if MOITPT.get() ==1 : MOI.append('6')
    if MOIDP.get() ==1 : MOI.append('7')
    if MOIOEM.get() ==1 : MOI.append('8')
    if MOIQC3v12.get() ==1 : MOI.append('9')
    if MOIIEC.get() ==1 : MOI.append('10')
    moili = ':'.join(MOI)
    os.system(f'"py ./updateTCjson.py" %s'% str(':'.join(MOI)))
     
def Testcaseselection():
    if len(SM3_frame.winfo_children()) > 0:
        for wdgt in SM3_frame.winfo_children():
            wdgt.destroy()
    testcaselist = []
    CoilSel_lb = Label(SM3_frame,text="Select Testcase :",font=myFont,width=15,anchor=E).grid(row=2,column=2)
    CoilSel_lb_Cb = Combobox(SM3_frame,textvariable=selectedtc,width=32,font=myFont_value,values=chapterslist,state="readonly")
    CoilSel_lb_Cb.grid(row=2,column=3)
    TestsLB = Listbox(SM3_frame,font=myFont,width=70,height=15,selectmode=MULTIPLE,listvariable=Tesecaselist)
    TestsLB.grid(row=4,column=3)
    scrollbar = Scrollbar(SM3_frame,orient=VERTICAL)
    scrollbar.config(command = TestsLB.yview)
    scrollbar.grid(row=4,column=4,sticky='ns')
    CoilSel_lb_Cb.bind("<<ComboboxSelected>>",LoadMOITest)
    kepsel_btn = Button(SM3_frame,text="Keep Selected",font=myFont,width=15, command= lambda: KeepSelected(TestsLB))
    kepsel_btn.grid(row=8,column=3)
    rmsel_btn = Button(SM3_frame,text="Remove Selected",font=myFont,width=15, command= lambda: RemoveSelected(TestsLB))
    rmsel_btn.grid(row=18,column=3)
    

def LoadMOITest(ts):
    global Tesecaselist
    if selectedtc.get() != "--":
        Tesecaselist.set(value=Testcnf[selectedtc.get()])
def KeepSelected(TestsLB):
    SelectedTC = read_file('Testcase.json')
    TCstatus = read_file('Tcstatus.json')
    index = TestsLB.curselection()
    print(index)
    if len(index)>0:
        testcases = [TestsLB.get(i) for i in index]
        availabletc = str(Tesecaselist.get()).replace('(','').replace(')','').replace(" '",'').replace("'",'').split(',')
        if '' in availabletc: availabletc.remove('')
        ns_tests = list(set(availabletc) - set(testcases))
        #print(ns_tests)
        if len(ns_tests) > 0:
            Chap = selectedtc.get()
            for tc in ns_tests:
                Testcnf[Chap].remove(tc)
                del TCstatus[tc]
            with open('TestConfig.json', "w") as outfile:
                json.dump(Testcnf, outfile)  
            with open('Tcstatus.json', "w") as outfile:
                json.dump(TCstatus, outfile)  
            LoadMOITest("ts")
            messagebox.showinfo("Update info:","Removed the Unselected Testcases.")
        else: messagebox.showinfo("Update info:","No Unselected Testcases to remove.")
    else: messagebox.showinfo("Update info:","Select a Testcase.")
def RemoveSelected(TestsLB):
    SelectedTC = read_file('Testcase.json')
    TCstatus = read_file('Tcstatus.json')
    index = TestsLB.curselection()
    print(index)
    if len(index)>0:
        testcases = [TestsLB.get(i) for i in index]
        availabletc = str(Tesecaselist.get()).replace('(','').replace(')','').replace(" '",'').replace("'",'').split(',')
        if '' in availabletc: availabletc.remove('')
        selected_tests = list(set(availabletc) - set(testcases))
        #print(selected_tests)
        if len(selected_tests) > 0:
            Chap = selectedtc.get()
            for tc in selected_tests:
                Testcnf[Chap].remove(tc)
                del TCstatus[tc]
            with open('TestConfig.json', "w") as outfile:
                json.dump(Testcnf, outfile)  
            with open('Tcstatus.json', "w") as outfile:
                json.dump(TCstatus, outfile)  
            LoadMOITest("ts")
        messagebox.showinfo(f"Update info:","Removed the Selected Testcases.")
    else: messagebox.showinfo("Update info:","Select a Testcase.")

def RUNTests():
     if len(SM3_frame.winfo_children()) > 0:
        for wdgt in SM3_frame.winfo_children():
            wdgt.destroy()
     PhaseLC = Label(SM3_frame,text="Select Chapter :",font=myFont).grid(row=1,column=1)
     SM3_phase_frame = Frame(SM3_frame,height=5,width=37,relief=FLAT)
     SM3_phase_frame.grid(row=1,column=2,columnspan=1)
     Checkbutton(SM3_phase_frame,text='ALLChapters',font=myFont_value2,variable=ChapAll,command=ALL_Chapters).grid(row=1,column=1,sticky=W)
     Checkbutton(SM3_phase_frame,text='Physical ',font=myFont_value2,variable=ChPHY,command=deselect_ALL).grid(row=2,column=1,sticky=W)
     Checkbutton(SM3_phase_frame,text='Protocol',font=myFont_value2,variable=ChPROT,command=deselect_ALL).grid(row=3,column=1,sticky=W)
     Checkbutton(SM3_phase_frame,text='Power',font=myFont_value2,variable=ChPOW,command=deselect_ALL).grid(row=4,column=1,sticky=W)
     Checkbutton(SM3_phase_frame,text='Extended Power',font=myFont_value2,variable=ChEPOW,command=deselect_ALL).grid(row=2,column=2,sticky=W)
     Checkbutton(SM3_phase_frame,text='FRS',font=myFont_value2,variable=ChFRS,command=deselect_ALL).grid(row=3,column=2,sticky=W)
     Checkbutton(SM3_phase_frame,text='USB4',font=myFont_value2,variable=ChUSB4,command=deselect_ALL).grid(row=4,column=2,sticky=W)
     
     Button(SM3_frame,text="Run_test",font=myFont, command=Run_Test).grid(row=3,column=2)

def ALL_Chapters():
    if ChapAll.get() == 1:    
        ChPHY.set(1)
        ChPROT.set(1)
        ChPOW.set(1)
        ChEPOW.set(1)
        ChFRS.set(1)
        ChUSB4.set(1)
    else:
        ChPHY.set(0)
        ChPROT.set(0)
        ChPOW.set(0)
        ChEPOW.set(0)
        ChFRS.set(0)
        ChUSB4.set(0)
def deselect_ALL():
    ChapAll.set(0) if 0 in [ChPHY.get(),ChPROT.get(),ChPOW.get(),ChEPOW.get(),ChFRS.get(),ChUSB4.get()] else  ChapAll.set(1)

#Start Execution
def Run_Test():
    chpaterlist =[]
    if ChPHY.get()==1 : chpaterlist.append('Physical')
    if ChPROT.get()==1 : chpaterlist.append('Protocol')
    if ChPOW.get()==1 : chpaterlist.append('Power')
    if ChEPOW.get()==1 : chpaterlist.append('Extended Power')
    if ChFRS.get()==1 : chpaterlist.append('FRS')  
    if ChUSB4.get()==1 : chpaterlist.append('USB4')
    os.system(f'"py ./Runtest.py" %s'% str(':'.join(chpaterlist)))

#Controls -end
#---ADD buttons for SM1----
ipbtn = PhotoImage(file="./img/ipbtn.png")
ip_button = Button(parent, image=ipbtn, relief=RAISED,background="#23275C",bd=0,command=loadipbtn)
ip_button.place(x=30,y=50)
runbtn = PhotoImage(file="./img/runbtn.png")
run_button = Button(parent, image=runbtn, relief=RAISED,background="#23275C",bd=0,command=loadrunbtn)
run_button.place(x=30,y=120)

rpbtn = PhotoImage(file="./img/rpbtn.png")
rp_button = Button(parent, image=rpbtn, relief=RAISED,background="#23275C",bd=0,command=loadrpbtn)
rp_button.place(x=30,y=190)

stbtn = PhotoImage(file="./img/stbtn.png")
st_button = Button(parent, image=stbtn, relief=RAISED,background="#23275C",bd=0)
st_button.place(x=30,y=260)

grllogo = PhotoImage(file="./img/grl.png")
grllogo_frame = Frame(parent,height=50,width=80,background="#23275C", bd=1,relief=FLAT)
grllogo_frame.place(x=10,y=440)
lb =Label(grllogo_frame,image=grllogo,width=80,background="#23275C",height=50)
lb.pack()
parent.mainloop()  