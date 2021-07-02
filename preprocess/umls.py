# -*- coding: utf-8 -*-

import csv

f = open("../data/CUIs_oneLabel.csv", 'r',encoding="utf-8" )
reader = csv.reader(f,delimiter=',')
cuis=list(reader)
f.close()

CUIs=dict()
CUIsLabel=dict()
for cui in cuis:
    CUIs[cui[0]]=cui[1]
    CUIsLabel[cui[1]]=cui[0]
    
    
f = open("../data/CUI_types.csv", 'r',encoding="utf-8" )
reader = csv.reader(f,delimiter=',')
cuis=list(reader)
f.close()

cuis.pop(0)

CUIsGroups=dict()
for cui in cuis:
    CUIsGroups[cui[0]]=cui[3]

    
    
def get_cui_label(id):
  if id in CUIs:
    return CUIs[id]  
  return "" 


def get_cui_group(id):
  if id in CUIsGroups:
    return CUIsGroups[id]  
  return ""
