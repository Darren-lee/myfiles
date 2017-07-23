#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,getopt,time,subprocess

def usage():
    print('''
    python ReportDownload.py [option][value]...
    -h or --help
    -i or --rsidFile="RSID list文件，一行一个ID"
    -o or --output="输出文件前缀'"
    -d or --date="日期，用于记录检索所有report的节点"
    -p or --path="要查找的包含'*_report.drug'文件的路径,默认/share/data/robots/PROJECT/report/"
    -n or --name="查找的文件pattern,默认查找'*_report.drug'"
    -t or --type="查找并输出的数据类型，默认为'reportDrug',备选如'QC'等"
    ''')

if ( len( sys.argv ) == 1 ):
    print('-h or --help for detail')
    sys.exit(1)

#parameters
try:
    options,args = getopt.getopt(sys.argv[1:], "hi:o:d:p:n:t:",["help","rsidFile=","path=","output=",
                                                                  "date=","name=","type="])
except getopt.GetoptError:
    sys.exit()

#Default
filedate = time.strftime('%Y%m%d',time.localtime(time.time()))
mut_output = 'mutation'
searchpath = '/share/data/robots/PROJECT/report/'
pattern = '*_report.drug'
type = 'reportDrug'

#getopt
for name,value in options:
    if name in ("-h","--help"):
        usage()
        sys.exit(1)
    if name in ("-i","--rsidFile"):
        rsidsFile = value
    if name in ("-o","--output"):
        mut_output = value
    if name in ("-d","--date"):
        filedate = value
    if name in ("-p","--path"):
        searchpath = value
    if name in ("-n","--name"):
        pattern = value
    if name in ("-t","--type"):
        type = value


#some output filename
emptyFile = str(mut_output)+"_"+type+"_empty_"+str(filedate)+".txt"
outputFile = str(mut_output) + "_"+type+"_" + str(filedate) + ".txt"
ignoredList = str(mut_output) + "_"+type+"_id_na_" + str(filedate) + ".txt"
projectListFile = str(mut_output) + "_"+type+"_paths_" + str(filedate) + ".txt"

#find all the _report.drug files in the given path
command = "find " + searchpath + " -type f -name '" + str(pattern) + "' -print > " + projectListFile
subprocess.call(command, shell=True)
print("Searching all files finished!" + '\n')

# Read all the project list and store rsid into a dict, with its value the exact location
projectlists = open(projectListFile, 'r')
projects = {}
for record in projectlists.readlines():
    records = record.strip().split('/')
    pro = records[-1].split('_')[0]
    location = record.strip()
    if pro in projects > 0:
        projects[pro] = [projects[pro],location]
    else:
        projects[pro] = location
projectlists.close()

# Read raid one by one and judge whether its in the above dict, if yes write it ,if not output it to anothe file
rsids = open(rsidsFile, 'r')
mut_res = open(outputFile, "w+")
na_ids = open(ignoredList, "w+")
empty_drug = open(emptyFile,"w+")
s=0
for id in rsids.readlines():
    id = id.strip()
    if id in projects:
        filename = projects[id]
        if filename.startswith('/'):
            mutdata = open(filename, 'r')
        else:
            mutdata = open(filename[0], 'r')
            print(filename)

        k=0
        for mut in mutdata.readlines():
            if mut.startswith('#'):
                continue
            else:
                if mut.startswith('RS'):
                    mut_res.write(mut)
                    k+=1
                elif s == 0:
                    mut_res.write(mut)
                    s+=1
                else:
                    continue
        print(id + " Finished!")
        mutdata.close()
        if k ==0:
            empty_drug.write(id+'\n')
    else:
        na_ids.write(id + '\n')
rsids.close()
mut_res.close()
na_ids.close()
empty_drug.close()