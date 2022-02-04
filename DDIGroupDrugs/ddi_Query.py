import os
import re
import sys
import json
from SPARQLWrapper import SPARQLWrapper, JSON

class iddDescription:
 
    def __init__(self):
        self.ddiWHY = []
        self.dependencies = []

class iddTuple:
 
    def __init__(self,precipitantDrug,explaination):
        self.precipitantDrug = precipitantDrug
        self.explaination = explaination

class sideEffect:
 
    def __init__(self,precipitantDrug,objectDrug,effect,impact):
        self.precipitantDrug = precipitantDrug
        self.objectDrug = objectDrug
        self.effect = effect
        self.impact = impact

class effectTuple:
 
    def __init__(self,precipitantDrug,objectDrug):
        self.precipitantDrug = precipitantDrug
        self.objectDrug = objectDrug

class ddiTuple:
 
    def __init__(self,precipitantDrug,objectDrug,explaination):
        self.precipitantDrug = precipitantDrug
        self.objectDrug = objectDrug
        self.explaination = explaination

def CreateLabels(OncologicalDrugs,Non_OncologicalDrugs,SPARQLEndpoint,Prefix,Labels):
    listDrugs=CreateListDrugs(OncologicalDrugs,Prefix)
    listDrugs=listDrugs+ "," +CreateListDrugs(Non_OncologicalDrugs,Prefix)

    query= """select distinct ?Drug ?drugLabel \n 
    where {?Drug <http://clarify2020.eu/vocab/annLabel> ?drugLabel.\n 
    FILTER (?Drug in (""" + listDrugs + """ ))}\n"""

    #print(query)
    sparql = SPARQLWrapper(SPARQLEndpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data=results["results"]["bindings"]
    for row in data:
        Labels[row["Drug"]["value"].replace("http://clarify2020.eu/entity/","")]=row["drugLabel"]["value"]

    return Labels

def CreateEDB(OncologicalDrugs,Non_OncologicalDrugs,SPARQLEndpoint,EDB,Prefix):

    listDrugs=CreateListDrugs(OncologicalDrugs,Prefix)
    listDrugs=listDrugs+ "," +CreateListDrugs(Non_OncologicalDrugs,Prefix)

    query= """select distinct ?precipitantDrug ?objectDrug ?effect ?impact \n 
    where {?s a <http://clarify2020.eu/vocab/DrugDrugInteraction> .\n 
    ?s <http://clarify2020.eu/vocab/effect_cui> ?o . \n 
    ?o <http://clarify2020.eu/vocab/annLabel> ?effect. \n 
    ?s <http://clarify2020.eu/vocab/impact> ?impact .\n 
    ?s <http://clarify2020.eu/vocab/precipitant_drug_cui> ?precipitantDrug .\n 
    ?s <http://clarify2020.eu/vocab/object_drug_cui> ?objectDrug 
    FILTER (?precipitantDrug in (""" + listDrugs + """ ) && ?objectDrug in (""" + listDrugs +  """))}\n"""

    print(query)
    sparql = SPARQLWrapper(SPARQLEndpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data=results["results"]["bindings"]
    for row in data:
        if row["effect"]["value"] in ["Serum_concentration","Serum_concentration_of", "Serum_level"]:
            if row["impact"]["value"].replace("http://clarify2020.eu/entity/","") in ["Increase","Higher","Worsening"]:
               EDB["serum_increase"].append(sideEffect(row["precipitantDrug"]["value"].replace("http://clarify2020.eu/entity/",""), row["objectDrug"]["value"].replace("http://clarify2020.eu/entity/",""),"serum_concentration","increase"))
            else:
               EDB["serum_decrease"].append(sideEffect(row["precipitantDrug"]["value"].replace("http://clarify2020.eu/entity/",""), row["objectDrug"]["value"].replace("http://clarify2020.eu/entity/",""),"serum_concentration","decrease"))
        else:
            if row["effect"]["value"] =="Metabolism":
                if row["impact"]["value"].replace("http://clarify2020.eu/entity/","") in ["Increase","Higher","Worsening"]:
               	    EDB["metabolism_increase"].append(sideEffect(row["precipitantDrug"]["value"].replace("http://clarify2020.eu/entity/",""), row["objectDrug"]["value"].replace("http://clarify2020.eu/entity/",""),"metabolism","increase"))
                else:
                	EDB["metabolism_decrease"].append(sideEffect(row["precipitantDrug"]["value"].replace("http://clarify2020.eu/entity/",""), row["objectDrug"]["value"].replace("http://clarify2020.eu/entity/",""),"metabolism","decrease"))
            else:
                if row["effect"]["value"].replace("http://clarify2020.eu/entity/","") in ["Excretion_rate","Excretory_function"]:
                    if row["impact"]["value"] in ["Increase","Higher","Worsening"]:
                        EDB["excretion_increase"].append(sideEffect(row["precipitantDrug"]["value"].replace("http://clarify2020.eu/entity/",""), row["objectDrug"]["value"].replace("http://clarify2020.eu/entity/",""),"excretation","increase"))
                    else:
                        EDB["excretion_decrease"].append(sideEffect(row["precipitantDrug"]["value"].replace("http://clarify2020.eu/entity/",""), row["objectDrug"]["value"].replace("http://clarify2020.eu/entity/",""),"excretation","decrease"))
                else:
                    if row["effect"]["value"].replace("http://clarify2020.eu/entity/","") in ["Process_of_absorption"]:
                        if row["impact"]["value"] in ["Increase","Higher","Worsening"]:
                           EDB["absorption_increase"].append(sideEffect(row["precipitantDrug"]["value"].replace("http://clarify2020.eu/entity/",""),row["objectDrug"]["value"].replace("http://clarify2020.eu/entity/",""),"absoption","increase"))
                        else:
                           EDB["absorption_decrease"].append(sideEffect(row["precipitantDrug"]["value"].replace("http://clarify2020.eu/entity/",""), row["objectDrug"]["value"].replace("http://clarify2020.eu/entity/",""),"absoption","decrease"))
                    else:    
                        EDB["DDI_AD"].append(sideEffect(row["precipitantDrug"]["value"].replace("http://clarify2020.eu/entity/",""), row["objectDrug"]["value"].replace("http://clarify2020.eu/entity/",""),row["effect"]["value"],row["impact"]["value"].replace("http://clarify2020.eu/entity/","")))
    return EDB

def CreateListDrugs(Drugs,Prefix):
    ListOfDrugs=""
    comma=""

    for drug in Drugs:
        ListOfDrugs=ListOfDrugs + comma+"<"+Prefix+"/entity/"+drug+">"
        comma=","
    return ListOfDrugs

def BaseCaseIDB(EDB,IDB,ddiTypeList,typeDDI,Labels):
    effects={"serum_increase":" can increase serum concentration of ",
             "serum_decrease":" can decrease serum concentration of ",
             "metabolism_increase":" can increase metabolism of ",
             "metabolism_decrease":" can decrease metabolism of ",
             "absorption_increase":" can increase the absorption of ",
             "absorption_decrease":" can decrease the absorption of ",
             "excretion_increase":" can increase the excretion of ",
             "excretion_decrease":" can decrease the excretion of "}
    for ddiType in ddiTypeList:
        for ddi in EDB[ddiType]:
            if ddi.objectDrug not in IDB[typeDDI]:
               IDB[typeDDI][ddi.objectDrug] = iddDescription()
            #IDB[typeDDI][ddi.objectDrug].ddiWHY.append(effectTuple(ddi.precipitantDrug, Labels[ddi.precipitantDrug] + " " + effects[ddiType] + " " +  Labels[ddi.objectDrug]))
            explaination=Labels[ddi.precipitantDrug] + " " + effects[ddiType] + " " +  Labels[ddi.objectDrug]
            if explaination not in IDB[typeDDI][ddi.objectDrug].ddiWHY:
               IDB[typeDDI][ddi.objectDrug].ddiWHY.append(explaination)
            if ddi.precipitantDrug not in IDB[typeDDI][ddi.objectDrug].dependencies:   
               IDB[typeDDI][ddi.objectDrug].dependencies.append(ddi.precipitantDrug)
    return IDB


def InductiveCaseIDB(IDB,ddiType):
    fix_poitnt=False
    while not(fix_poitnt):
        fix_poitnt=True
        for drug1 in  IDB[ddiType]:
            for drug2 in IDB[ddiType]:
                #print(str(drug1) + " dependendencies Drug2 " + str(IDB[ddiType][drug2].dependencies) +  " dependendencies Drug1 " + str(IDB[ddiType][drug1].dependencies) +  " WHY " + str(IDB[ddiType][drug1].ddiWHY))
                if ((drug1 in IDB[ddiType][drug2].dependencies) and
                   (not(set(IDB[ddiType][drug1].dependencies).issubset(set(IDB[ddiType][drug2].dependencies))) or
                    not(set(IDB[ddiType][drug1].ddiWHY).issubset(set(IDB[ddiType][drug2].ddiWHY))))):
                        IDB[ddiType][drug2].dependencies += IDB[ddiType][drug1].dependencies
                        IDB[ddiType][drug2].ddiWHY  += IDB[ddiType][drug1].ddiWHY
                        fix_poitnt=False
    return IDB

def WriteDDIs(EDB,Labels):
    listDDIs=[]
    effects={"serum_increase":" can increase serum concentration of ",
           "serum_decrease":" can decrease serum concentration of ",
           "metabolism_increase":" can increase metabolism of ",
           "metabolism_decrease":" can decrease metabolism of ",
           "absorption_increase":" can increase the absorption of ",
           "absorption_decrease":" can decrease the absorption of ",
           "excretion_increase":" can increase the excretion of ",
           "excretion_decrease":" can decrease the excretion of "}
    for key in EDB:
        for ddi in EDB[key]:
            if key in effects:
                #listDDIs.append(ddiTuple(ddi.precipitantDrug,ddi.objectDrug,ddi.precipitantDrug + " " + effects[key] + " " + ddi.objectDrug))
                listDDIs.append(Labels[ddi.precipitantDrug] + " " + effects[key].replace("http://clarify2020.eu/entity/","") + " " + Labels[ddi.objectDrug])
                #print(Labels[ddi.precipitantDrug] + " " + effects[key] + " " + Labels[ddi.objectDrug])

            else:
                #listDDIs.append(ddiTuple(ddi.precipitantDrug,ddi.objectDrug,ddi.precipitantDrug + " " + str(key) + " " + ddi.objectDrug))
                listDDIs.append(Labels[ddi.precipitantDrug] + " " + ddi.effect + " " + ddi.impact.replace("http://clarify2020.eu/entity/","") + " " + Labels[ddi.objectDrug])
                #print(Labels[ddi.precipitantDrug] + " " + ddi.effect + " " + ddi.impact + " " + Labels[ddi.objectDrug])
    return listDDIs

def WriteDrugEffects(IDB,Labels):
    listEffects=dict()
    for  key in IDB:
        for ddi in IDB[key]:
            if ddi not in listEffects:
                listEffects[ddi]=[]
            for exp in IDB[key][ddi].ddiWHY:
                if key=="Toxicity_Increase":
                    listEffects[ddi].append("The toxicity of  " + Labels[str(ddi)] +  " can be increased because " +  str(exp))
                    #print("The toxicity of  " + Labels[str(ddi)] +  " is increased because " + str(exp))
                else:
                    listEffects[ddi].append("The effectiveness of  " +  Labels[str(ddi)] +  " can be decreased because " + str(exp)) 
                    #print("The effectiveness of  " + Labels[str(ddi)] +  " is decreased because " + str(exp) )
    return listEffects

def createJSON(SetOfDDIs,DrugEffects):
    results=dict()
    results["DDIs"]=SetOfDDIs
    results["DrugEffects"]=DrugEffects

    return results


def DDIs_Group_Drugs(OncologicalDrugs,Non_OncologicalDrugs,SPARQLEndpoint,Prefix):
    EDB={"serum_increase":[],
           "serum_decrease":[],
           "metabolism_increase":[],
           "metabolism_decrease":[],
           "absorption_increase":[],
           "absorption_decrease":[],
           "excretion_increase":[],
           "excretion_decrease":[],
           "DDI_AD":[]}
    Labels={}
    ddiTypeEffectiveness=["serum_decrease","metabolism_increase","absorption_decrease","excretion_increase"]
    ddiTypeToxicity=["serum_increase","metabolism_decrease","absorption_increase","excretion_decrease"]
    Labels=CreateLabels(OncologicalDrugs,Non_OncologicalDrugs,SPARQLEndpoint,Prefix,Labels)

    IDB={"Toxicity_Increase":{},"Effectiveness_Decrease":{}}

    EDB=CreateEDB(OncologicalDrugs,Non_OncologicalDrugs,SPARQLEndpoint,EDB,Prefix)

    IDB=BaseCaseIDB(EDB,IDB,ddiTypeEffectiveness,"Effectiveness_Decrease",Labels)

    IDB=BaseCaseIDB(EDB,IDB,ddiTypeToxicity,"Toxicity_Increase",Labels)

    IDB=InductiveCaseIDB(IDB,"Toxicity_Increase")

    IDB=InductiveCaseIDB(IDB,"Effectiveness_Decrease")

    

    SetOfDDIs=WriteDDIs(EDB,Labels)

    DrugEffects=WriteDrugEffects(IDB,Labels)


    return createJSON(SetOfDDIs,DrugEffects)


def computingDDI(input_file):
        input_data = input_file
        onco_drugs=input_data["Input"]["OncologicalDrugs"]
        non_onco_drugs=input_data["Input"]["Non_OncologicalDrugs"]
        return DDIs_Group_Drugs(onco_drugs,non_onco_drugs,os.environ["ENDPOINT"],"http://clarify2020.eu")

if __name__ == '__main__':
    x=1
    #print(computingDDI("/Users/vidalm/Nextcloud/Projects/CLARIFY/DDIsAPI/DDIGroupDrugs/input.json"))
    #computingDDI("/Users/vidalm/Nextcloud/Projects/CLARIFY/DDIsAPI/input.json")
