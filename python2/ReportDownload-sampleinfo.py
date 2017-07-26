#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,getopt,time,subprocess

def usage():
    print('''
    python ReportDownload-4.py [option][value]...
    -h or --help
    -i or --rsidFile="RSID list文件，一行一个ID"
    -o or --output="输出文件前缀'"
    -d or --date="日期，用于记录检索所有report的节点"
    -f or --sample_info="存放sample_info.xls的路径,默认/share/data/robots/PROJECT/sample_info.xls"
    -t or --type="查找并输出的数据类型，默认为'reportDrug',备选'QC'"
    ''')

if ( len( sys.argv ) == 1 ):
    print('-h or --help for detail')
    sys.exit(1)

#parameters
try:
    options,args = getopt.getopt(sys.argv[1:], "hi:o:d:f:t:",["help","rsidFile=","sample_info=","output=",
                                                                  "date=","type="])
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
    if name in ("-d","--date"):
        filedate = value
    if name in ("-f","--sample_info"):
        sampleinfo_file = value
    if name in ("-t","--type"):
        type = value

#some output filename
emptyFile = str(output_prefix)+"_"+type+"_empty_"+str(filedate)+".txt"
outputFile = str(output_prefix) + "_"+type+"_" + str(filedate) + ".txt"
ignoredFile = str(output_prefix) + "_"+type+"_id_na_" + str(filedate) + ".txt"
datapathFile = str(output_prefix) + "_"+type+"_dataPath_" + str(filedate) + ".txt"

#Read sample_info.xls and store all the RSIDs into a dict with its value the exact location of the data file
#Here with the type to be a choose of which file to store into the dict
sam_info = open(sampleinfo_file,'r')
na_ids = open(ignoredFile, "w+")
projects = {}
for record in sam_info.readlines():
    record = record.strip().split('\t')
    sample_id = record[3]
    sample_path = record[0]
    sample_path_half = '/share/data/robots/PROJECT/'
    if (sample_path.startswith('16')):
        res2 = sample_path_half + '2016_analysisData' + '/' + sample_path + '/' + sample_id
    elif (sample_path.startswith('15')):
        res2 = sample_path_half + '2015_analysisData' + '/' + sample_path + '/' + sample_id
    elif(sample_path.startswith('17')):
        res2 = sample_path_half + sample_path + '/' + sample_id
    else:
        continue

    report_path = res2 + '/report/'
    if type == 'reportDrug':
        res1 = report_path + sample_id + '_report.drug'
    elif type == 'QC':
        res1 = report_path + sample_id + '_QC.xls'
    else:
        print 'Parameter: -t only works with reportDrug and QC! Please confirm your input.'
        sys.exit()
    projects[sample_id] = [res1,res2]

sam_info.close()
print len(projects), 'RSID!'

# Read rsid one by one and judge whether its in the above dict, if yes write it ,if not output it to anothe file
rsids = open(rsidsFile, 'r')
mut_res = open(outputFile, "w+")
empty_drug = open(emptyFile,"w+")
data_path = open(datapathFile,"w+")
s=0
for id in rsids.readlines():
    id = id.strip()
    if id in projects:
        filename = projects[id][0]
        datadir = projects[id][1]
        try:
            mutdata = open(filename, 'r')
        except:
            na_ids.write(id + '\n')
            continue
        data_path.write(id + '\t' + datadir + '\n')
        k=0
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
        if k ==0:
            empty_drug.write(id + '\t' + str(lcount) + '\n')
    else:
        na_ids.write(id + '\n')
rsids.close()
mut_res.close()
na_ids.close()
empty_drug.close()
data_path.close()
