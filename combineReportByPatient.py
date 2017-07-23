#!/usr/bin/python
# coding=utf-8
'''
Write at 2017.06.29 By Bing.Li
Input1: a tab delimited file contains two cols, col1 is patient ID, col2 id RSIDs which are sorted;
D001	RS1503738TIS
D001	RS1503739PLA
D002	RS1503817TIS
D002	RS1503816PLA
D003	RS1504107TIS
D003	RS1504106PLA
Input2: report file, format is the same with pipeline output
TIS report
PLA report
Output: a tab delimited file which is separated by patient
'''

import sys,getopt,csv

def usage():
    print('''
    python combineReportByPatient.py [option][value]...
    -h or --help
    -i or --rsidFile="RSID,col1=patientID(已排序),col2=RSID(按照组织，血液的顺序，且基线随访按照顺序)"
    -r or --report="report file"
    -o or --output="output file name"
    ''')

if ( len( sys.argv ) == 1 ):
    print('-h or --help for detail')
    sys.exit(1)

#parameters
try:
    options,args = getopt.getopt(sys.argv[1:], "hi:o:r:",["help","rsidFile=","output=","report="])
except getopt.GetoptError:
    sys.exit()

#getopt
for name,value in options:
    if name in ("-h","--help"):
        usage()
        sys.exit(1)
    if name in ("-i","--rsidFile"):
        rsid_file = value
    if name in ("-o","--output"):
        output_file = value
    if name in ("-r","--report"):
        report_file = value

#Patient ID & RSIDs in dict
pRSID_dict = {}
pRSID_list = []
p_r = open(rsid_file)
reader = csv.reader(p_r)
for line in reader:
    #line = line.strip().split(",")
    patient_ID = line[0]
    RSID_now = line[1]
    if patient_ID in pRSID_dict:
        pRSID_dict[patient_ID].extend([RSID_now])
    else:
        pRSID_dict[patient_ID] = [RSID_now]
        pRSID_list.append(patient_ID)
p_r.close()
print 'Patient ID count=',len(pRSID_dict)

#read report and store in dict
report_data = open(report_file,'r')
report_dict = {}
for line in report_data.readlines():
    line = line.strip()
    record = line.split(",")
    if record[0] == "Sample_ID":
        header_half = record[1:5]
        header_half.extend(record[7:27])
        report_dict['headerhalf'] = header_half
    elif record[0] in report_dict:
        sampleID = record[0]
        report_dict[sampleID].extend([line])
    else:
        sampleID = record[0]
        report_dict[sampleID] = [line]
report_data.close()
print "Total report samples are ",len(report_dict)

#for loop for all the patient ID
res = open(output_file,'w')
for pID in pRSID_list:
    samples = pRSID_dict[pID]
    header_half = report_dict['headerhalf']
    header = 'Patient.ID' + '\t' + '\t'.join(header_half) +'\t' + '\t'.join(samples) + '\n'
    res.write(header)
    sep = []
    report_list = []
    for j in range(len(samples)):
        sep.extend([''])
    mut_dict = {}
    for i in range(len(samples)):
        sample = samples[i]
        if sample in report_dict:
            for mutinfo in report_dict[sample]:
                mutinfo = mutinfo.split(",")
                mut = mutinfo[1]+'_'+mutinfo[4]
                if mut in mut_dict:
                    mut_dict[mut][-len(samples) + i] = mutinfo[5]
                else:
                    out_record = mutinfo[1:5]
                    out_record.extend(mutinfo[7:27])
                    out_record.extend(sep)
                    out_record[-len(samples) + i] = mutinfo[5]
                    mut_dict[mut] = out_record
                    report_list.append(mut)
        else:
            continue
    for key in report_list:
        output = pID +'\t' + '\t'.join(mut_dict[key]) + '\n'
        res.write(output)
res.close()

#Finish compare
print 'Samples compare Finished!'

#For those not compared - recall
