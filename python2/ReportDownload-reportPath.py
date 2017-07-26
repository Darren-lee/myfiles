#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,getopt,time,subprocess

def usage():
    print('''
    python ReportDownload-4.py [option][value]...
    -h or --help
    -i or --rsidFile="RSID list文件，一行一个ID"
    -o or --output="输出文件前缀'"
    -s or --server="sh 或者 gz"
    -t or --type="查找并输出的数据类型，默认为'reportDrug',备选'QC'"
    ''')

if ( len( sys.argv ) == 1 ):
    print('-h or --help for detail')
    sys.exit(1)

#parameters
try:
    options,args = getopt.getopt(sys.argv[1:], "hi:o:s:t:",["help","rsidFile=","output=","server=","type="])
except getopt.GetoptError:
    sys.exit()

#Default
filedate = time.strftime('%Y%m%d',time.localtime(time.time()))
output_prefix = 'First'
type = 'reportDrug'
pathfile = ''

#getopt
for name,value in options:
    if name in ("-h","--help"):
        usage()
        sys.exit(1)
    if name in ("-i","--rsidFile"):
        rsidsFile = value
    if name in ("-o","--output"):
        output_prefix = value
    if name in ("-s","--server"):
        server = value
    if name in ("-t","--type"):
        type = value

#some output filename
emptyFile = str(output_prefix)+"_"+type+"_empty_"+str(filedate)+".txt"
outputFile = str(output_prefix) + "_"+type+"_" + str(filedate) + ".txt"
ignoredFile = str(output_prefix) + "_"+type+"_id_na_" + str(filedate) + ".txt"
datapathFile = str(output_prefix) + "_"+type+"_dataPath_" + str(filedate) + ".txt"

#generate the absolute path
if server == 'sh':
    sample_path_half = '/share/home/robots/PROJECT/report/'
elif server == 'gz':
    sample_path_half = '/share/data/robots/PROJECT/report/'
else:
    print 'Parameter: -s only works with sh and gz! Please confirm your input.'
    sys.exit()

# Read rsid one by one and judge whether its in the above dict, if yes write it ,if not output it to anothe file
rsids = open(rsidsFile, 'r')
mut_res = open(outputFile, "w+")
empty_drug = open(emptyFile,"w+")
data_path = open(datapathFile,"w+")
na_ids = open(ignoredFile, "w+")
s=0
for id in rsids.readlines():
    id = id.strip()
    if type == 'reportDrug':
        filename = sample_path_half + id + '/' + id + '_report.drug'
    elif type == 'QC':
        filename = sample_path_half + id + '/' + id + '_QC.xls'
    else:
        print 'Parameter: -t only works with reportDrug and QC! Please confirm your input.'
        sys.exit()

    try:
        mutdata = open(filename, 'r')
    except:
        na_ids.write(id + '\n')
        continue

    data_path.write(id + '\t' + filename + '\n')
    k = 0
    lcount = 0
    for mut in mutdata.readlines():
        lcount += 1
        if mut.startswith('#'):
            continue
        else:
            if mut.startswith('RS'):
                mut_res.write(mut)
                k += 1
            elif s == 0:
                mut_res.write(mut)
                s += 1
            else:
                continue
    print(id + " Finished!")
    mutdata.close()
    if k == 0:
        empty_drug.write(id + '\t' + str(lcount) + '\t' + filename + '\n')

rsids.close()
mut_res.close()
na_ids.close()
empty_drug.close()
data_path.close()
