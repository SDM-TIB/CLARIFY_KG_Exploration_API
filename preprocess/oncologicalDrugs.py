# -*- coding: utf-8 -*-


import csv
import bioFalcon
from tqdm import tqdm
import umls



filename='../data/Farmatools_pulmon.csv'
with open(filename, 'r') as file:
    reader = csv.reader(file,delimiter=',')
    rows=list(reader)


rows.pop(0)

newList=[]
errorsList=[]
seen_description=dict()


for row in tqdm(rows):
    if row[2] not in seen_description:
        seen_description[row[2]]=''
    else:
        continue
    #print(row[2])
    cuis=bioFalcon.get_cui_long(row[2])
    if cuis!="":
        for cui in cuis:
            cuiType=umls.get_cui_group(cui[1])
            if cuiType=="Chemicals & Drugs":
                newList.append([row[2],cui[1],umls.get_cui_label(cui[1])])
                
                
                
with open("../data/oncologicalDrugs_final.csv", "w" , encoding='utf-8') as output:
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        for row in newList:
            writer.writerow(row)
            

