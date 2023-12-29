import xml.etree.ElementTree as ET
import json
import sys
from numpy import piecewise
import xlsxwriter
argu = sys.argv
#create object for golden XML file 
with open("settings.json", "r") as readfile:
    settings = json.load(readfile)
treeGolden = ET.parse(settings['Golden_path'])
GDroot = treeGolden.getroot()
#create object for generated XML
treeGenerated = ET.parse(settings['Generated_path'])
GRroot = treeGenerated.getroot()
print("GR : ",settings['Generated_path'])
print("GD : ",settings['Golden_path'])
#################methods########################
def GetAllAppConditions():
    condli = {}
    MaxCondCount = 0
    for child in GDroot[1][0][3][12][0]:
        if child.tag =='test': 
            # print(child.get('tcID'))
            cncnt = 0
            for condition in child.find('conditions'):
                cncnt+=1
                #add conditions
                if condition.get('conditionID') not in condli :
                    condli[condition.get('conditionID')]={}
                    condli[condition.get('conditionID')]['checks']=[]
                #add checks for conditions
                ckcnt = 0
                if condition.find('checks'):
                    for checks in condition.find('checks'):
                        ckcnt +=1
                        if checks.get('checkID') not in condli[condition.get('conditionID')]:
                            condli[condition.get('conditionID')]['checks'].append(checks.get('checkID'))
                condli[condition.get('conditionID')]['MaxChkCount'] = ckcnt
            if cncnt > MaxCondCount : MaxCondCount=cncnt
    checksli = []
    for con in condli:
        exp =[1,0]
        if condli[con]['MaxChkCount'] not in exp:
            checksli.append(condli[con]['MaxChkCount'])
    checksli.sort(reverse=True)
    return [condli,MaxCondCount,checksli]
def UpdateResults(row,col,value,WS):
    # print(value,row,col)
    if value == 'pass':
        Ws.merge_range(row,col,row+1,col,value,Pass_frmt)
        # Ws.write(row,col,value,Pass_frmt)
    elif value =='fail':
        Ws.merge_range(row,col,row+1,col,value,Fail_frmt)
        # Ws.write(row,col,value,Fail_frmt)
    elif value in ['NA','n/a']:
        Ws.merge_range(row,col,row+1,col,value,INCL_frmt)
        # Ws.write(row,col,value,INCL_frmt)
#create a workbook
Reprot_loc='./'
Wb = xlsxwriter.Workbook(Reprot_loc+'_CTS_Summary_Report2.xlsx')
#Formats 
Heading1 = Wb.add_format({'bold': True, 'font_color': '#FFFFFF','bg_color':'#833C0C','center_across':True,'border':True})
Heading2 = Wb.add_format({'bold': True, 'font_color': '#000000','bg_color':'#F4B084','center_across':True,'border':True})
Heading3 = Wb.add_format({'bold': True, 'font_color': '#000000','bg_color':'#F8CBAD','center_across':True,'border':True})

Pass_frmt = Wb.add_format({'font_color': '#000000','bg_color':'#00B050','border':True})
PassClr = Wb.add_format({'font_color': '#00B050'})
FailClr = Wb.add_format({'font_color': '#FF0000'})
default_frmt = Wb.add_format()
Fail_frmt = Wb.add_format({'font_color': '#000000','bg_color':'#FF0000','border':True})
INCL_frmt = Wb.add_format({'font_color': '#000000','bg_color':'#F79646','border':True})
NA_frmt =  Wb.add_format({'font_color': '#000000','bg_color':'#BFBFBF','border':True,'center_across':True})
exp_frmt = Wb.add_format({'font_color': '#000000','bg_color':'#F79646','border':True,'center_across':True})
#Add sheet to workbook
Ws = Wb.add_worksheet('Comparison')
#Headers
Header1 = ["ChapterID","ChapterName","DUTName","DUTID","SWVersion"]
Header2 = ["Sno","Testcase ID","Testcase Name"]
ResHeader = ["Golden","Generated","Compare"]
ResHeader2 = ["Name","Total_Checks_Count","Pass_Checks_Count","Fail_Checks_Count"]
ResHeader3 = ["Check #","GDRUN","GRRUN","Compare"]
res = GetAllAppConditions()
# print(res)
conditiondict = res[0]
maxchecks = res[1]
CondiHeader = []
### Headers ####################################################################
row =0
col =0
#fill side headers to be added
#fill Headers
row+=2
for i in Header2:
    Ws.write(row,col, i,Heading3)
    col+=1
Ws.merge_range(row-2,0,row-1,col-1,"Header",Heading1)
#Fill TC Result
for i in ResHeader:
    Ws.write(row,col, i,Heading3)
    col+=1
Ws.merge_range(row-2,col-3,row-1,col-1,"Test Result",Heading1)
#Update conditions are checks headers
id = 1
chkid = 0
value=1
totalchecks = 0
checksli = res[2]
while id <= maxchecks:
    Ws.merge_range(row,col,row-2,col,f"Condition {id} & Checks",Heading1)
    col+=1
    id+=1
# Fill Values
row+=1
sno = 1
for child in GDroot[1][0][3][12][0]:
    col=0
    Comp ={}
    #To get Testcases 
    if child.tag =='test':
        #Header
        # print(sno,child.get('tcID'),child[0].text,child[1].get('value'))
        Ws.merge_range(row,col,row+1,col,sno)
        # Ws.write(row,col,sno)
        col+=1
        Ws.merge_range(row,col,row+1,col,child.get('tcID'))
        print(child.get('tcID'))
        # Ws.write(row,col,child.get('tcID'))
        col+=1
        Ws.merge_range(row,col,row+1,col,child[0].text)
        # Ws.write(row,col,child[0].text)
        #results 
        col+=1
        UpdateResults(row,col,child[1].get('value').replace(' ',''),Ws)
        #search the test from generated xml
        for GRchild in GRroot[1][0][3][12][0]:
            if GRchild.tag =='test' and GRchild.get('tcID') == child.get('tcID'):
                col+=1
                UpdateResults(row,col,GRchild[1].get('value').replace(' ',''),Ws)
                #TC result compare
                col+=1
                Comp[GRchild.get('tcID')] = 'pass' if child[1].get('value') == GRchild[1].get('value') else 'fail'
                UpdateResults(row,col,Comp[child.get('tcID')],Ws)
                #check for conditions , Get golden Test condition header in xml
                conditionlimits = 0
                condi_cks ={}
                chks ={}
                for cond in child.find('conditions'):
                    rowcnt=0
                    # Get checks for generated
                    condi_cks['gd_cname'] = cond.get('conditionID')
                    condi_cks['gd_result'] = cond[0].get('value').replace(' ','')
                    condi_cks['gr_result'] ='NA'
                    condi_cks['gd_tcnt'] = 0
                    condi_cks['gr_tcnt'] = 0
                    condi_cks['gd_pcnt'] = 0
                    condi_cks['gr_pcnt'] = 0
                    condi_cks['gd_fcnt'] = 0
                    condi_cks['gr_fcnt'] = 0
                    for GRcond in GRchild.find('conditions'):
                        if cond.get('conditionID')==GRcond.get('conditionID'):
                            condi_cks['gr_result'] = GRcond[0].get('value').replace(' ','')
                            #check for conditions
                            if cond.find('checks'):
                                chkid =0
                                for chk in cond.find('checks'):
                                    chks[chkid] = {}
                                    chks[chkid]['ckname'] = chk.get('checkID')
                                    chks[chkid]['ckgd_res'] = 'P' if 'pass' in chk[0].get('value') else 'F'
                                    chks[chkid]['ckgr_res'] = 'NA'
                                    condi_cks['gd_tcnt']+=1
                                    if 'pass' in chk[0].get('value'):condi_cks['gd_pcnt']+=1
                                    elif 'fail' in chk[0].get('value'):condi_cks['gd_fcnt']+=1
                                    for GRchk in GRcond.find('checks'): 
                                        if chk.get('checkID')==GRchk.get('checkID'):
                                            # print(chkid,chk.get('checkID'),GRchk[0].get('value'),chk[0].get('value'))
                                            condi_cks['gr_tcnt']+=1
                                            if 'pass' in GRchk[0].get('value'):condi_cks['gr_pcnt']+=1
                                            elif 'fail' in GRchk[0].get('value'):condi_cks['gr_fcnt']+=1
                                            chks[chkid]['ckgr_res'] = 'P' if 'pass' in GRchk[0].get('value') else 'F'
                                            break
                                    chkid+=1
                            break
                    # print(condi_cks,chks)
                    #Update checks
                    col+=1
                    ComRslt = 'pass' if condi_cks['gd_result'] == condi_cks['gr_result'] else 'fail'
                    segments = [condi_cks['gd_cname']+'|'+condi_cks['gd_result']+':'+condi_cks['gr_result']+':',ComRslt,default_frmt,'|']
                    if ComRslt == 'pass':
                        segments.insert(1,PassClr)
                    else: segments.insert(1,FailClr)
                    Ws.write_rich_string(row,col,*segments)
                    # rowcnt+=1
                    CHKsegments =['Checks:|TC '+str(condi_cks['gd_tcnt'])+':'+str(condi_cks['gr_tcnt'])+':','| PC '+str(condi_cks['gd_pcnt'])+':'+str(condi_cks['gr_pcnt'])+':','| FC '+str(condi_cks['gd_fcnt'])+':'+str(condi_cks['gr_fcnt'])+':','|']
                    #total Count
                    TCcomp = 'P' if condi_cks['gd_tcnt'] == condi_cks['gr_tcnt'] else 'F'
                    if TCcomp=='P':
                        CHKsegments.insert(1,PassClr)
                    else:
                        CHKsegments.insert(1,FailClr)
                    CHKsegments.insert(2,TCcomp)
                    #Pass count
                    PCcomp = 'P' if condi_cks['gd_pcnt'] == condi_cks['gr_pcnt'] else 'F'
                    if PCcomp=='P':
                        CHKsegments.insert(4,PassClr)
                    else:
                        CHKsegments.insert(4,FailClr)
                    CHKsegments.insert(5,PCcomp)
                    #Fail Count
                    FCcomp = 'P' if condi_cks['gd_fcnt'] == condi_cks['gr_fcnt'] else 'F'
                    if FCcomp=='P':
                        CHKsegments.insert(7,PassClr)
                    else:
                        CHKsegments.insert(7,FailClr)
                    CHKsegments.insert(8,FCcomp)
                    Ws.write_rich_string(row+1,col,*CHKsegments)
                    #check for unmatches
                    #print(TCcomp,PCcomp,FCcomp)
                    if 'F' in [TCcomp, PCcomp, FCcomp]:
                        Ws.merge_range(row + 2, 0, row + 2, 5, "*Found Unmatched checks", INCL_frmt)
                        #list checks and values
                        CHKdepthSeg =[]
                        for i in chks:
                            CHKdepthSeg.append('|'+str(chks[i]['ckname'])+':'+str(chks[i]['ckgd_res'])+':'+str(chks[i]['ckgr_res'])+':')
                            comres = 'P' if chks[i]['ckgd_res']==chks[i]['ckgr_res'] else 'F'
                            if comres =='P':
                                CHKdepthSeg.append(PassClr)
                                CHKdepthSeg.append(comres)
                            elif comres =='F':
                                CHKdepthSeg.append(FailClr)
                                CHKdepthSeg.append(comres)
                        CHKdepthSeg.append('|')   
                        rowcnt+=1
                        Ws.write_rich_string(row+2,col,*CHKdepthSeg,INCL_frmt)
        row = row +(2+rowcnt)
        sno+=1
#Fill Result values
Ws.autofit()
Wb.close()
