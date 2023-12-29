import json
import datetime
import sys
#Json read
def read_file(path):
    with open(path, "r") as rf:
        values = json.load(rf)
    return values
def defaultconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
#define veriables
if len(sys.argv)>1:
    moili=sys.argv[1].split(':')
else: moili = ['1']
chapterli = []
Testinfo = read_file('./Testcase.json')
Testconfig = read_file('./TestConfig.json')
TestStatus = read_file('./Tcstatus.json')
tcstatus ={}
#clear the existing testconfig json file
for elm in Testconfig:
    Testconfig[elm].clear()
for moi in moili:
    if len(Testinfo['MOIChapter'][moi])>0:
        for ch in Testinfo['MOIChapter'][moi]:
            if ch not in chapterli: chapterli.append(ch)
#add to testconfig json files
for TC in Testinfo:
    if 'TC_' in TC:
        if int(Testinfo[TC]['ChapterID']) in chapterli:
            Testconfig[Testinfo['Chapters'][Testinfo[TC]['ChapterID']]].append(Testinfo[TC]['TestName'])
            tcstatus[Testinfo[TC]['TestName']] = 'NotRun'
#add tests to 
#update json files
with open("./TestConfig.json", "w") as outfile:
    json.dump(Testconfig,outfile,default=defaultconverter)
with open("./Tcstatus.json", "w") as outfile:
    json.dump(tcstatus,outfile,default=defaultconverter)

