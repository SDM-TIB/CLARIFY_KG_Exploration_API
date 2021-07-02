# -*- coding: utf-8 -*-

import csv
import bioFalcon
from tqdm import tqdm
import umls



filename='../data/Non-oncologicalDrugs.csv'
with open(filename, 'r') as file:
    reader = csv.reader(file,delimiter=',')
    rows=list(reader)


newList=[]
errorsList=[]
for row in tqdm(rows):
    #print(row[0])
    cui=bioFalcon.get_cui_keyword(row[0])
    if cui!="":
        newList.append([row[0],cui,umls.get_cui_label(cui)])
    else:
        errorsList.append(row[0])
        
    
    

with open("../data/Non-oncologicalDrugs_final.csv", "w" , encoding='utf-8') as output:
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        for row in newList:
            writer.writerow(row)