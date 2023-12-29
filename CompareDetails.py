import xml.etree.ElementTree as ET
import json
import xlsxwriter

# Read settings from settings.json
with open("settings.json", "r") as readfile:
    settings = json.load(readfile)

treeGolden = ET.parse(settings['Golden_path'])
GDroot = treeGolden.getroot()

treeGenerated = ET.parse(settings['Generated_path'])
GRroot = treeGenerated.getroot()

def GetAllAppConditions():
    condli = {}
    MaxCondCount = 0
    for child in GDroot[1][0][3][12][0]:
        if child.tag == 'test':
            cncnt = 0
            for condition in child.find('conditions'):
                cncnt += 1
                if condition.get('conditionID') not in condli:
                    condli[condition.get('conditionID')] = {}
                    condli[condition.get('conditionID')]['checks'] = []
                ckcnt = 0
                if condition.find('checks'):
                    for checks in condition.find('checks'):
                        ckcnt += 1
                        if checks.get('checkID') not in condli[condition.get('conditionID')]:
                            condli[condition.get('conditionID')]['checks'].append(checks.get('checkID'))
                condli[condition.get('conditionID')]['MaxChkCount'] = ckcnt
            if cncnt > MaxCondCount:
                MaxCondCount = cncnt
    checksli = []
    for con in condli:
        exp = [1, 0]
        if condli[con]['MaxChkCount'] not in exp:
            checksli.append(condli[con]['MaxChkCount'])
    checksli.sort(reverse=True)
    return [condli, MaxCondCount, checksli]

def UpdateResults(row, col, value, WS):
    if value == 'pass':
        WS.write(row, col, value, Pass_frmt)
    elif value == 'fail':
        WS.write(row, col, value, Fail_frmt)
    elif value in ['NA', 'n/a']:
        WS.write(row, col, value, INCL_frmt)

# Create a workbook
Report_loc = './_CTS_Validation_Report.xlsx'
Wb = xlsxwriter.Workbook(Report_loc)

# Formats
Heading1 = Wb.add_format({'bold': True, 'font_color': '#FFFFFF', 'bg_color': '#833C0C', 'center_across': True, 'border': True})
Heading3 = Wb.add_format({'bold': True, 'font_color': '#000000', 'bg_color': '#F8CBAD', 'center_across': True, 'border': True})
Pass_frmt = Wb.add_format({'font_color': '#000000', 'bg_color': '#00B050', 'border': True})
Fail_frmt = Wb.add_format({'font_color': '#000000', 'bg_color': '#FF0000', 'border': True})
INCL_frmt = Wb.add_format({'font_color': '#000000', 'bg_color': '#F79646', 'border': True})
exp_frmt = Wb.add_format({'font_color': '#000000', 'bg_color': '#F79646', 'border': True, 'center_across': True})

# Add a sheet to the workbook
Ws = Wb.add_worksheet('Comparison')

# Headers
Header1 = ["ChapterID", "ChapterName", "DUTName", "DUTID", "SWVersion"]
Header2 = ["Sno", "Testcase ID", "Testcase Name"]
ResHeader = ["GRRUN", "GDRUN", "Compare"]
ResHeader2 = ["Condition #", "GRRUN", "GDRUN", "Compare"]
ResHeader3 = ["Check #", "GRRUN", "GDRUN", "Compare"]

res = GetAllAppConditions()
conditiondict = res[0]
maxchecks = res[1]
checksli = res[2]

# Write the headers
row = 0
col = 0

# Fill side headers
row += 2
for i in Header2:
    Ws.write(row, col, i, Heading3)
    col += 1
Ws.merge_range(row - 2, 0, row - 1, col - 1, "Header", Heading1)

for i in ResHeader:
    Ws.write(row, col, i, Heading3)
    col += 1
Ws.merge_range(row - 2, col - 3, row - 1, col - 1, "Test Result", Heading1)

id = 1
chkid = 0
value = 1
totalchecks = 0

while id <= maxchecks:
    for i in ResHeader2:
        if i == 'Condition #':
            i = str(i) + str(id)
        Ws.write(row, col, i, Heading3)
        col += 1

    if chkid < len(checksli):
        value = checksli[chkid]
        cid = 1

        while cid <= value:
            for i in ResHeader3:
                if i == 'Check #':
                    i = str(i) + str(cid)
                Ws.write(row, col, i, Heading3)
                col += 1
            cid += 1

        chkid += 1
        totalchecks = totalchecks + cid
        Ws.merge_range(row - 1, col - (4 * cid), row - 1, col - 1, f"Condition #{id} with applicable checks", Heading1)
    else:
        totalchecks = totalchecks + 1
        Ws.merge_range(row - 1, col - 4, row - 1, col - 1, f"Condition #{id} with applicable checks", Heading1)
    id += 1

Ws.merge_range(row - 2, col - (4 * totalchecks), row - 2, col - 1, "Testcase Condition and Assertion Checks", Heading1)

# Fill values
row += 1
sno = 1

for child in GDroot[1][0][3][12][0]:
    col = 0
    Comp = {}

    if child.tag == 'test':
        Ws.write(row, col, sno)
        col += 1
        Ws.write(row, col, child.get('tcID'))
        col += 1
        Ws.write(row, col, child[0].text)
        col += 1
        UpdateResults(row, col, child[1].get('value').replace(' ', ''), Ws)
        col += 1

        for GRchild in GRroot[1][0][3][12][0]:
            if GRchild.tag == 'test' and GRchild.get('tcID') == child.get('tcID'):
                col += 1
                UpdateResults(row, col, GRchild[1].get('value').replace(' ', ''), Ws)
                col += 1
                Comp[GRchild.get('tcID')] = 'pass' if child[1].get('value') == GRchild[1].get('value') else 'fail'
                UpdateResults(row, col, Comp[GRchild.get('tcID')], Ws)

        id = 1
        chkid = 0
        while id <= maxchecks:
            col += 1
            if id in child[2] and id in GRchild[2]:
                UpdateResults(row, col, 'pass', Ws)
                col += 1
                UpdateResults(row, col, 'pass', Ws)
                col += 1
                UpdateResults(row, col, 'pass', Ws)
                cid = 1
                if chkid < len(checksli):
                    value = checksli[chkid]
                    while cid <= value:
                        col += 1
                        UpdateResults(row, col, 'pass', Ws)
                        col += 1
                        UpdateResults(row, col, 'pass', Ws)
                        col += 1
                        UpdateResults(row, col, 'pass', Ws)
                        cid += 1
                    chkid += 1
                else:
                    col += 1
                    UpdateResults(row, col, 'pass', Ws)
                    col += 1
                    UpdateResults(row, col, 'pass', Ws)
                    col += 1
                    UpdateResults(row, col, 'pass', Ws)
            else:
                UpdateResults(row, col, 'fail', Ws)
                col += 1
                UpdateResults(row, col, 'fail', Ws)
                col += 1
                UpdateResults(row, col, 'fail', Ws)
                cid = 1
                if chkid < len(checksli):
                    value = checksli[chkid]
                    while cid <= value:
                        col += 1
                        UpdateResults(row, col, 'fail', Ws)
                        col += 1
                        UpdateResults(row, col, 'fail', Ws)
                        col += 1
                        UpdateResults(row, col, 'fail', Ws)
                        cid += 1
                    chkid += 1
                else:
                    col += 1
                    UpdateResults(row, col, 'fail', Ws)
                    col += 1
                    UpdateResults(row, col, 'fail', Ws)
                    col += 1
                    UpdateResults(row, col, 'fail', Ws)

            id += 1

        sno += 1
        row += 1

# Save the workbook
Wb.close()
