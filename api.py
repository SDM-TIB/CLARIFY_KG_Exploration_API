#!/usr/bin/env python3
#
# Description: POST service for exploration of
# data of Lung Cancer in the iASiS KG.
#

import sys
from flask import Flask, abort, request, make_response , render_template
import json
from SPARQLWrapper import SPARQLWrapper, JSON, POST
import logging
import os
import itertools
import csv
from DDIGroupDrugs import ddi_Query
from flask_cors import CORS
from wedge import auxiliar_wedge


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



#os.environ["ENDPOINT"]='https://labs.tib.eu/sdm/clarify-kg-5-1/sparql'
KG = os.environ["ENDPOINT"]
#KG= 'http://node2.research.tib.eu:11295/sparql'
EMPTY_JSON = "{}"

app = Flask(__name__)
CORS(app)



filename='data/Non-oncologicalDrugs_final.csv'
with open(filename, 'r', encoding='utf-8') as file:
    reader = csv.reader(file,delimiter=',')
    rows=list(reader)
    
LC_consideredDrugs=[]
for row in rows:
    LC_consideredDrugs.append('http://clarify2020.eu/entity/'+row[1])
    
    
filename='data/LC_OncologicalDrugs.csv'
with open(filename, 'r', encoding='utf-8') as file:
    reader = csv.reader(file,delimiter=',')
    rows=list(reader)
    
rows.pop(0)
    

for row in rows:
    LC_consideredDrugs.append('http://clarify2020.eu/entity/'+row[1])



BC_consideredDrugs=[]

filename='data/BC_OncologicalDrugs.csv'
with open(filename, 'r', encoding='utf-8') as file:
    reader = csv.reader(file,delimiter=',')
    rows=list(reader)
    
rows.pop(0)
    

for row in rows:
    BC_consideredDrugs.append('http://clarify2020.eu/entity/'+row[1])
############################
#
# Query constants
#
############################




QUERY_DRUG_TO_DRUGS_INTERACTIONS ="""
SELECT * {{
{{SELECT  ?effectorDrugCUI ?affectdDrugCUI  ?effectorDrugLabel ?affectdDrugLabel ?adverse ?impact 'Symmetric' AS ?type ?description   WHERE {{  
                                           ?interaction_symm a <http://clarify2020.eu/vocab/SymmetricDrugDrugInteraction>. 
                                           ?interaction a <http://clarify2020.eu/vocab/DrugDrugInteraction>.
                                           ?interaction_symm ?p ?interaction.
                                           ?interaction <http://clarify2020.eu/vocab/precipitant_drug_cui> ?effectorDrugCUI.
                                           ?interaction <http://clarify2020.eu/vocab/object_drug_cui> ?affectdDrugCUI.
                                           ?effectorDrugCUI <http://clarify2020.eu/vocab/annLabel> ?effectorDrugLabel.
                                           ?affectdDrugCUI <http://clarify2020.eu/vocab/annLabel> ?affectdDrugLabel.
                                            ?interaction <http://clarify2020.eu/vocab/effect_cui> ?adverse_cui.   
                                            ?adverse_cui <http://clarify2020.eu/vocab/annLabel> ?adverse.
                                            ?interaction <http://clarify2020.eu/vocab/impact> ?impact.  
                                            ?interaction <http://clarify2020.eu/vocab/ddi_description> ?description.
                                            {0}
UNION
{{
SELECT  ?effectorDrugCUI ?affectdDrugCUI ?effectorDrugLabel ?affectdDrugLabel ?adverse ?impact 'Symmetric' AS ?type ?description   WHERE {{  
                                           ?interaction_symm a <http://clarify2020.eu/vocab/SymmetricDrugDrugInteraction>. 
                                           ?interaction a <http://clarify2020.eu/vocab/DrugDrugInteraction>.
                                           ?interaction_symm ?p ?interaction.
                                           ?interaction <http://clarify2020.eu/vocab/precipitant_drug_cui> ?effectorDrugCUI.
                                           ?interaction <http://clarify2020.eu/vocab/object_drug_cui> ?affectdDrugCUI.
                                           ?effectorDrugCUI <http://clarify2020.eu/vocab/annLabel> ?effectorDrugLabel.
                                           ?affectdDrugCUI <http://clarify2020.eu/vocab/annLabel> ?affectdDrugLabel.
                                            ?interaction <http://clarify2020.eu/vocab/effect_cui> ?adverse_cui.   
                                            ?adverse_cui <http://clarify2020.eu/vocab/annLabel> ?adverse.  
                                            ?interaction <http://clarify2020.eu/vocab/impact> ?impact.    
                                            ?interaction <http://clarify2020.eu/vocab/ddi_description> ?description.
                                            {1}
UNION
{{ 
    SELECT  ?effectorDrugCUI ?affectdDrugCUI ?effectorDrugLabel ?affectdDrugLabel ?adverse ?impact 'NonSymmetric' AS ?type ?description   WHERE {{  
                                           ?interaction_notsymm a <http://clarify2020.eu/vocab/NonSymmetricDrugDrugInteraction>. 
                                           ?interaction a <http://clarify2020.eu/vocab/DrugDrugInteraction>.
                                           ?interaction_notsymm ?p ?interaction.
                                           ?interaction <http://clarify2020.eu/vocab/precipitant_drug_cui> ?effectorDrugCUI.
                                           ?interaction <http://clarify2020.eu/vocab/object_drug_cui> ?affectdDrugCUI.
                                           ?effectorDrugCUI <http://clarify2020.eu/vocab/annLabel> ?effectorDrugLabel.
                                           ?affectdDrugCUI <http://clarify2020.eu/vocab/annLabel> ?affectdDrugLabel.
                                           ?interaction <http://clarify2020.eu/vocab/effect_cui> ?adverse_cui.   
                                            ?adverse_cui <http://clarify2020.eu/vocab/annLabel> ?adverse.
                                            ?interaction <http://clarify2020.eu/vocab/impact> ?impact.     
                                            ?interaction <http://clarify2020.eu/vocab/ddi_description> ?description.
                                            {2}      
UNION
{{ 
    SELECT  ?effectorDrugCUI ?affectdDrugCUI ?effectorDrugLabel ?affectdDrugLabel ?adverse ?impact 'NonSymmetric' AS ?type ?description   WHERE {{  
                                           ?interaction_notsymm a <http://clarify2020.eu/vocab/NonSymmetricDrugDrugInteraction>. 
                                           ?interaction a <http://clarify2020.eu/vocab/DrugDrugInteraction>.
                                           ?interaction_notsymm ?p ?interaction.
                                           ?interaction <http://clarify2020.eu/vocab/precipitant_drug_cui> ?effectorDrugCUI.
                                           ?interaction <http://clarify2020.eu/vocab/object_drug_cui> ?affectdDrugCUI.
                                           ?effectorDrugCUI <http://clarify2020.eu/vocab/annLabel> ?effectorDrugLabel.
                                           ?affectdDrugCUI <http://clarify2020.eu/vocab/annLabel> ?affectdDrugLabel.
                                           ?interaction <http://clarify2020.eu/vocab/effect_cui> ?adverse_cui.   
                                            ?adverse_cui <http://clarify2020.eu/vocab/annLabel> ?adverse.  
                                            ?interaction <http://clarify2020.eu/vocab/impact> ?impact.     
                                            ?interaction <http://clarify2020.eu/vocab/ddi_description> ?description.
                                            {3}                                              
"""


QUERY_DRUG_TO_DRUGS_INTERACTIONS_PREDICTED ="""
SELECT  * WHERE {  
                                           ?interaction a <http://clarify2020.eu/vocab/DrugDrugPrediction>.
                                           ?interaction <http://clarify2020.eu/vocab/interactor1> ?effectorDrug.
                                           ?interaction <http://clarify2020.eu/vocab/interactor2> ?affectdDrug.
                                            ?affectdDrug owl:sameAs ?affectdDrugwithLabel.
                                            ?effectorDrug owl:sameAs ?effectorDrugwithlabel.
                                            ?affectdDrugwithLabel <http://clarify2020.eu/vocab/hasCUIAnnotation> ?affectdDrugCUI.
                                            ?effectorDrugwithlabel <http://clarify2020.eu/vocab/hasCUIAnnotation> ?effectorDrugCUI.
                                           ?effectorDrug <http://clarify2020.eu/vocab/drugLabel> ?effectorDrugLabel.
                                           ?affectdDrug <http://clarify2020.eu/vocab/drugLabel> ?affectdDrugLabel.
                                          ?interaction <http://clarify2020.eu/vocab/confidence> ?confidence.
                                           ?interaction <http://clarify2020.eu/vocab/predictionMethod> ?provenance.                             
"""

QUERY_DRUGS_TO_DRUGS_INTERACTIONS ="""
SELECT DISTINCT * {{
{{SELECT  ?effectorDrugLabel ?affectdDrugLabel ?adverse ?impact ?description  WHERE {{
                                           ?interaction a <http://clarify2020.eu/vocab/DrugDrugInteraction>.
                                           ?interaction <http://clarify2020.eu/vocab/precipitant_drug_cui> <http://clarify2020.eu/entity/{0}>.
                                           ?interaction <http://clarify2020.eu/vocab/object_drug_cui> <http://clarify2020.eu/entity/{1}>.
                                           <http://clarify2020.eu/entity/{0}> <http://clarify2020.eu/vocab/annLabel> ?effectorDrugLabel.
                                           <http://clarify2020.eu/entity/{1}> <http://clarify2020.eu/vocab/annLabel> ?affectdDrugLabel.
                                            ?interaction <http://clarify2020.eu/vocab/effect_cui> ?adverse_cui.   
                                            ?adverse_cui <http://clarify2020.eu/vocab/annLabel> ?adverse.  
                                            ?interaction <http://clarify2020.eu/vocab/impact> ?impact.
                                            ?interaction <http://clarify2020.eu/vocab/ddi_description> ?description.
   
}}}} UNION 
{{SELECT  ?effectorDrugLabel ?affectdDrugLabel ?adverse ?impact ?description WHERE {{  
                                           ?interaction a <http://clarify2020.eu/vocab/DrugDrugInteraction>.
                                           ?interaction <http://clarify2020.eu/vocab/precipitant_drug_cui> <http://clarify2020.eu/entity/{1}>.
                                           ?interaction <http://clarify2020.eu/vocab/object_drug_cui> <http://clarify2020.eu/entity/{0}>.
                                           <http://clarify2020.eu/entity/{1}> <http://clarify2020.eu/vocab/annLabel> ?effectorDrugLabel.
                                           <http://clarify2020.eu/entity/{0}> <http://clarify2020.eu/vocab/annLabel> ?affectdDrugLabel.
                                            ?interaction <http://clarify2020.eu/vocab/effect_cui> ?adverse_cui.   
                                            ?adverse_cui <http://clarify2020.eu/vocab/annLabel> ?adverse.  
                                            ?interaction <http://clarify2020.eu/vocab/impact> ?impact.
                                            ?interaction <http://clarify2020.eu/vocab/ddi_description> ?description.
}}}}}}                                     
"""


QUERY_DRUGS_TO_DRUGS_INTERACTIONS_PREDICTED ="""
SELECT * {{
{{SELECT DISTINCT ?effectorDrugLabel ?affectdDrugLabel ?confidence ?provenance  WHERE {{
                                           ?interaction a <http://clarify2020.eu/vocab/DrugDrugPrediction>.
                                           ?interaction <http://clarify2020.eu/vocab/interactor1> ?effectorDrug.
                                           ?interaction <http://clarify2020.eu/vocab/interactor2> ?affectdDrug.
                                           ?affectdDrug owl:sameAs ?affectdDrugwithLabel.
                                           ?effectorDrug owl:sameAs ?effectorDrugwithLabel.
                                           ?affectdDrugwithLabel <http://clarify2020.eu/vocab/hasCUIAnnotation> <http://clarify2020.eu/entity/{0}>.
                                           ?effectorDrugwithLabel <http://clarify2020.eu/vocab/hasCUIAnnotation> <http://clarify2020.eu/entity/{1}>.
                                           ?effectorDrug <http://clarify2020.eu/vocab/drugLabel> ?effectorDrugLabel.
                                           ?affectdDrug <http://clarify2020.eu/vocab/drugLabel> ?affectdDrugLabel.
                                          ?interaction <http://clarify2020.eu/vocab/confidence> ?confidence.
                                           ?interaction <http://clarify2020.eu/vocab/predictionMethod> ?provenance.         
}}}} UNION 
{{SELECT DISTINCT ?effectorDrugLabel ?affectdDrugLabel ?confidence ?provenance  WHERE {{  
                                           ?interaction a <http://clarify2020.eu/vocab/DrugDrugPrediction>.
                                           ?interaction <http://clarify2020.eu/vocab/interactor1> ?effectorDrug.
                                           ?interaction <http://clarify2020.eu/vocab/interactor2> ?affectdDrug.
                                           ?affectdDrug owl:sameAs ?affectdDrugwithLabel.
                                           ?effectorDrug owl:sameAs ?effectorDrugwithLabel.
                                           ?affectdDrugwithLabel <http://clarify2020.eu/vocab/hasCUIAnnotation> <http://clarify2020.eu/entity/{1}>.
                                           ?effectorDrugwithLabel <http://clarify2020.eu/vocab/hasCUIAnnotation> <http://clarify2020.eu/entity/{0}>.
                                           ?effectorDrug <http://clarify2020.eu/vocab/drugLabel> ?effectorDrugLabel.
                                           ?affectdDrug <http://clarify2020.eu/vocab/drugLabel> ?affectdDrugLabel.
                                          ?interaction <http://clarify2020.eu/vocab/confidence> ?confidence.
                                           ?interaction <http://clarify2020.eu/vocab/predictionMethod> ?provenance.     
}}}}}}                                     
"""

QUERY_DRUG_TO_MOA="""
select distinct  ?drug ?drugLabel ?moa WHERE 
{{
?drug owl:sameAs ?drugwithLabel.
?drugwithLabel <http://clarify2020.eu/vocab/hasCUIAnnotation> <http://clarify2020.eu/entity/{0}>.
?drug <http://clarify2020.eu/vocab/drugsMechanismOfAction> ?moa .
?drug <http://clarify2020.eu/vocab/drugLabel> ?drugLabel.
}}
"""

QUERY_DRUG_TO_absorption="""
select distinct  ?drug ?drugLabel ?absorption WHERE 
{{
?drug owl:sameAs ?drugwithLabel.
?drugwithLabel <http://clarify2020.eu/vocab/hasCUIAnnotation> <http://clarify2020.eu/entity/{0}>.
?drug <http://clarify2020.eu/vocab/drugAbsorption> ?absorption .
?drug <http://clarify2020.eu/vocab/drugLabel> ?drugLabel.
}}
"""


############################
#
# Query generation
#
############################


def execute_query(query,limit=0,page=0):
    if limit!=0:
       query+="LIMIT "+str(limit)
    query+=" OFFSET "+str(page) 
    sparql_ins = SPARQLWrapper(KG)
    sparql_ins.setMethod(POST)
    sparql_ins.setQuery(query)
    sparql_ins.setReturnFormat(JSON)
    return sparql_ins.query().convert()['results']['bindings']



############################
#
# Processing results
#
############################

def drug2_interactions_query(drug,limit,page,all_drugs,cancer):
    if cancer=="LC":
        consideredDrugs=LC_consideredDrugs
    elif cancer=="BC":
        consideredDrugs=BC_consideredDrugs
    
    
    query_1=""

    
        
    query_1+="FILTER(?affectdDrugCUI in ("
    query_1+="<http://clarify2020.eu/entity/"+drug+">))"
    
    if all_drugs==0:
        query_1+="FILTER(?effectorDrugCUI in ("
        for drug in consideredDrugs:
            query_1+="<"+drug+">,"
        query_1=query_1[:-1]
        query_1+="))"

    
    query_1+="}}"
    
    
    
    
   
    query_2=""


        
    query_2+="FILTER(?effectorDrugCUI in ("
    query_2+="<http://clarify2020.eu/entity/"+drug+">))"
    
    if all_drugs==0:
        query_2+="FILTER(?affectdDrugCUI in ("
        for drug in consideredDrugs:
            query_2+="<"+drug+">,"
        query_2=query_2[:-1]
        query_2+="))"
 
    query_2+="}}"
    

    query_3=""
 
        
    query_3+="FILTER(?affectdDrugCUI in ("
    query_3+="<http://clarify2020.eu/entity/"+drug+">))"
    
    if all_drugs==0:
        query_3+="FILTER(?effectorDrugCUI in ("
        for drug in consideredDrugs:
            query_3+="<"+drug+">,"
        query_3=query_3[:-1]
        query_3+="))"


    query_3+="}}"
    
    
  
    
    
    
    query_4=""
  
        
    query_4+="FILTER(?effectorDrugCUI in ("
    query_4+="<http://clarify2020.eu/entity/"+drug+">))"
    
    if all_drugs==0:
        query_4+="FILTER(?affectdDrugCUI in ("
        for drug in consideredDrugs:
            query_4+="<"+drug+">,"
        query_4=query_4[:-1]
        query_4+="))"


    query_4+="}}}"
    
 
    

       
    query=QUERY_DRUG_TO_DRUGS_INTERACTIONS.format(query_1,query_2,query_3,query_4)
    
    qresults = execute_query(query,limit,page)
    return qresults


def drug2_interactions_predicted_query(drug,limit,page,all_drugs):
    query=QUERY_DRUG_TO_DRUGS_INTERACTIONS_PREDICTED
    query+="FILTER(?affectdDrugCUI in ("
    query+="<http://clarify2020.eu/entity/"+drug+">"
    
    '''if all_drugs==0:
        query+=","
        for drug in consideredDrugs:
            query+="<"+drug+">,"
        query=query[:-1]'''
        
    
    query+="))}"
        
    qresults = execute_query(query,limit,page)
    return qresults


def drugs2_interactions_query(drug_pairs,limit,page):
    query=QUERY_DRUGS_TO_DRUGS_INTERACTIONS.format(drug_pairs[0],drug_pairs[1])        
    qresults = execute_query(query,limit,page)
    return qresults


def drugs2_interactions_predicted_query(drug_pairs,limit,page):
    query=QUERY_DRUGS_TO_DRUGS_INTERACTIONS_PREDICTED.format(drug_pairs[0],drug_pairs[1])        
    qresults = execute_query(query,limit,page)
    return qresults


def drug2_moa_query(drug,limit,page):
    query=QUERY_DRUG_TO_MOA.format(drug)        
    qresults = execute_query(query,limit,page)
    return qresults

def drug2_absorption_query(drug,limit,page):
    query=QUERY_DRUG_TO_absorption.format(drug)        
    qresults = execute_query(query,limit,page)
    return qresults

def proccesing_response(input_dicc, target,limit,page,all_drugs,cancer):
    cuis=dict()
    results=dict()

    drugInteractions=dict()
    drugMOA=dict()
    drugAbsorption=dict()
    for elem in input_dicc:
        lcuis = input_dicc[elem]
        if len(lcuis)==0:
            continue
        for item in lcuis:
            cuis[item]=elem

        if len(cuis)==0:
            continue

   
       ############################Interactions#####################################         
           
        if elem=='Drugs':
            if target=="DDI":
                for drug in lcuis:
                    query_reslut=drug2_interactions_query(drug,limit,page,all_drugs,cancer)
                    drugInteractions[drug]=dict()
                    if len(query_reslut)>0:
                        #drugInteractions[drug]["Label"]=query_reslut[0]["affectdDrugLabel"]["value"]
                        drugInteractions[drug]["DDI"]=dict()
                        drugInteractions[drug]["DDI"]["Pharmacodynamic"]=[]
                        drugInteractions[drug]["DDI"]["Pharmacokinetic"]=[]
                        DDI_description=dict()
                        for result in query_reslut:
                            #if all_drugs==0:
                                #if not (result["effectorDrugCUI"]["value"]  in consideredDrugs and result["affectdDrugCUI"]["value"] in consideredDrugs) :
                                    #continue
                            if result["description"]["value"] in DDI_description:
                                continue
                            else:
                                DDI_description[result["description"]["value"]]=''
                            interaction=dict()
                            if result["type"]["value"]=='Symmetric':
                                interaction["Drug1"]=result["effectorDrugLabel"]["value"]
                                interaction["Drug2"]=result["affectdDrugLabel"]["value"]
                                interaction["effect"]=result["adverse"]["value"].replace('http://clarify2020.eu/entity/','').replace('_',' ')
                                interaction["impact"]=result["impact"]["value"].replace('http://clarify2020.eu/entity/','').replace('_',' ')
                                interaction["description"]=result["description"]["value"]
                                drugInteractions[drug]["DDI"]["Pharmacodynamic"].append(interaction)
                            else:     
                                interaction["effectorDrug"]=result["effectorDrugLabel"]["value"]
                                interaction["affectdDrug"]=result["affectdDrugLabel"]["value"]
                                interaction["effect"]=result["adverse"]["value"].replace('http://clarify2020.eu/entity/','').replace('_',' ')
                                interaction["impact"]=result["impact"]["value"].replace('http://clarify2020.eu/entity/','').replace('_',' ')
                                interaction["description"]=result["description"]["value"]
                                drugInteractions[drug]["DDI"]["Pharmacokinetic"].append(interaction)
                results['response']=drugInteractions
            elif target=="DDIS":
                drugs_pairs=[(x,y) for x,y in list(itertools.product(lcuis, lcuis)) if x!=y and x<y]
                for drug_pair in drugs_pairs :
                    query_reslut=drugs2_interactions_query(drug_pair,limit,page)
                    drugInteractions[str(drug_pair)]=dict()
                    if len(query_reslut)>0:
                        drugInteractions[str(drug_pair)]["Labels"]=query_reslut[0]["affectdDrugLabel"]["value"]+" AND "+query_reslut[0]["effectorDrugLabel"]["value"]
                        drugInteractions[str(drug_pair)]["DDIS"]=[]
                        
                        for result in query_reslut:                        
                            DDI_description=dict()
                            if result["description"]["value"] in DDI_description:
                                    continue
                            else:
                                    DDI_description[result["description"]["value"]]=''
                            for result in query_reslut:
                                interaction=dict()
                                interaction["effectorDrug"]=result["effectorDrugLabel"]["value"]
                                interaction["affectdDrug"]=result["affectdDrugLabel"]["value"]
                                interaction["effect"]=result["adverse"]["value"].replace('http://clarify2020.eu/entity/','').replace('_',' ')
                                interaction["impact"]=result["impact"]["value"].replace('http://clarify2020.eu/entity/','').replace('_',' ')
                                interaction["description"]=result["description"]["value"]
                                if interaction not in drugInteractions[str(drug_pair)]["DDIS"]:
                                    drugInteractions[str(drug_pair)]["DDIS"].append(interaction)
                results['response']=drugInteractions
            elif target=="DDIP":
                if cancer=="LC":
                    consideredDrugs=LC_consideredDrugs
                elif cancer=="BC":
                    consideredDrugs=BC_consideredDrugs
                #drugs_pairs=[(x,y) for x,y in list(itertools.product(lcuis, lcuis)) if x!=y]
                for drug in lcuis:
                    query_reslut=drug2_interactions_predicted_query(drug,limit,page,all_drugs)
                    drugInteractions[drug]=dict()
                    if len(query_reslut)>0:
                        drugInteractions[drug]["Label"]=query_reslut[0]["affectdDrugLabel"]["value"]
                        drugInteractions[drug]["DDIP"]=[]
                        for result in query_reslut:
                            if all_drugs==0:
                                if not (result["effectorDrugCUI"]["value"]  in consideredDrugs and result["affectdDrugCUI"]["value"] in consideredDrugs) :
                                    continue
                            interaction=dict()
                            interaction["effectorDrug"]=result["effectorDrugLabel"]["value"]
                            interaction["affectdDrug"]=result["affectdDrugLabel"]["value"]
                            interaction["confidence"]=result["confidence"]["value"]
                            interaction["provenance"]=result["provenance"]["value"]
                            drugInteractions[drug]["DDIP"].append(interaction)
                results['response']=drugInteractions
            elif target=="DDIPS":
                drugs_pairs=[(x,y) for x,y in list(itertools.product(lcuis, lcuis)) if x!=y and x<y]
                for drug_pair in drugs_pairs :
                    query_reslut=drugs2_interactions_predicted_query(drug_pair,limit,page)
                    drugInteractions[str(drug_pair)]=dict()
                    if len(query_reslut)>0:
                        drugInteractions[str(drug_pair)]["Labels"]=query_reslut[0]["affectdDrugLabel"]["value"]+" AND "+query_reslut[0]["effectorDrugLabel"]["value"]
                        drugInteractions[str(drug_pair)]["DDIPS"]=[]
                        for result in query_reslut:
                            interaction=dict()
                            interaction["effectorDrug"]=result["effectorDrugLabel"]["value"]
                            interaction["affectdDrug"]=result["affectdDrugLabel"]["value"]
                            interaction["confidence"]=result["confidence"]["value"]
                            interaction["provenance"]=result["provenance"]["value"]
                            drugInteractions[str(drug_pair)]["DDIPS"].append(interaction)
                results['response']=drugInteractions
            elif target=="MOA":
                for drug in lcuis:
                    query_reslut=drug2_moa_query(drug,limit,page)
                    drugMOA[drug]=dict()
                    if len(query_reslut)>0:
                        drugMOA[drug]["MOA"]=[]
                        for result in query_reslut:
                            interaction=dict()
                            interaction["drug"]=result["drugLabel"]["value"]
                            interaction["MechanismOfAction"]=result["moa"]["value"]
                            drugMOA[drug]["MOA"].append(interaction)
                results['response']=drugMOA
            elif target=="absorption":
                for drug in lcuis:
                    query_reslut=drug2_absorption_query(drug,limit,page)
                    drugAbsorption[drug]=dict()
                    if len(query_reslut)>0:
                        drugAbsorption[drug]["absorption"]=[]
                        for result in query_reslut:
                            interaction=dict()
                            interaction["drug"]=result["drugLabel"]["value"]
                            interaction["absorption"]=result["absorption"]["value"]
                            drugAbsorption[drug]["absorption"].append(interaction)
                results['response']=drugAbsorption

        
    
    return results
           


@app.route('/ddi', methods=['POST'])
def main_api():
    if (not request.json):
        abort(400)
    input_list = request.json
    if len(input_list) == 0:
        r = "{results: 'Error in the input format'}"
    else:
        response = ddi_Query.computingDDI(input_list)
        r = json.dumps(response, indent=4)            
    response = make_response(r, 200)
    response.mimetype = "application/json"
    return response




@app.route('/kg-exp', methods=['POST'])
def run_exploration_api():
    if (not request.json):
        abort(400)
    if 'limit' in request.args:
        limit = int(request.args['limit'])
    else:
        limit = 0
    if 'page' in request.args:
        page = int(request.args['page'])
    else:
        page = 0
    if 'target' in request.args:
        target = request.args['target']
    else:
        abort(400)
    if 'all_drugs' in request.args:
        all_drugs = int(request.args['all_drugs'])
    else:
        all_drugs=1
    if 'cancer' in request.args:
        cancer = request.args['cancer']
    else:
        cancer=1

    input_list = request.json
    if len(input_list) == 0:
        logger.info("Error in the input format")
        r = "{results: 'Error in the input format'}"
    else:
        response = proccesing_response(input_list,target,limit,page,all_drugs,cancer)       
        r = json.dumps(response, indent=4)  
    logger.info("Sending the results: ")
    response = make_response(r, 200)
    response.mimetype = "application/json"
    return response


def get_oncological_drugs_query(cancer):
    if cancer=="LC":
        query="""select distinct ?drugLabel ?cui where 
{?drug a <http://clarify2020.eu/vocab/LungCancerOncologicalDrug>.
?drug <http://clarify2020.eu/vocab/drugLabel> ?drugLabel.
?drug <http://clarify2020.eu/vocab/hasCUIAnnotation> ?ann.
?ann <http://clarify2020.eu/vocab/annID> ?cui.
} 
    """
    elif cancer=="BC":
        query="""select distinct ?drugLabel ?cui where 
{?drug a <http://clarify2020.eu/vocab/BreastCancerOncologicalDrug>.
?drug <http://clarify2020.eu/vocab/drugLabel> ?drugLabel.
?drug <http://clarify2020.eu/vocab/hasCUIAnnotation> ?ann.
?ann <http://clarify2020.eu/vocab/annID> ?cui.
} 
"""
    qresults = execute_query(query,0,0)
    finalresult=[]
    for result in qresults:
        item={}
        item["label"]=result["drugLabel"]["value"].replace("_"," ")
        item["cui"]=result["cui"]["value"]
        finalresult.append(item)
        
    return finalresult

def get_nononcological_drugs_query():
    query="""select distinct ?drugLabel ?cui where 
{?drug a <http://clarify2020.eu/vocab/LungCancerNonOncologicalDrug>.
?drug <http://clarify2020.eu/vocab/drugLabel> ?drugLabel.
?drug <http://clarify2020.eu/vocab/hasCUIAnnotation> ?ann.
?ann <http://clarify2020.eu/vocab/annID> ?cui.
} 
    """
    qresults = execute_query(query)
    finalresult=[]
    for result in qresults:
        item={}
        item["label"]=result["drugLabel"]["value"].replace("_"," ")
        item["cui"]=result["cui"]["value"]
        finalresult.append(item)
        
    return finalresult


def proccesing_response_nononcological():
    response=dict()
    response['NoNOncological_Drugs']=[]
    nononcological_drugs=get_nononcological_drugs_query()
    response['NoNOncological_Drugs']=nononcological_drugs

    return response

@app.route('/get_oncological_drugs', methods=['GET'])
def get_oncological_drugs():
    if 'cancer' in request.args:
        cancer = request.args['cancer']
    else:
        abort(400)
    response=dict()
    response['Oncological_Drugs'] = get_oncological_drugs_query(cancer)
    r = json.dumps(response, indent=4)            
    logger.info("Sending the results: ")
    response = make_response(r, 200)
    response.mimetype = "application/json"
    return response


@app.route('/get_DDI_rate', methods=['POST'])
def ddi_wedge():
    if (not request.json):
        abort(400)
    input_list = request.json
    if len(input_list) == 0:
        r = "{results: 'Error in the input format'}"
    else:
        union, set_dsd_label = auxiliar_wedge.load_data(input_list)
        response = auxiliar_wedge.discovering_knowledge(union, set_dsd_label)
        r = json.dumps(response, indent=4)
    response = make_response(r, 200)
    response.mimetype = "application/json"
    return response


@app.route('/get_nononcological_drugs', methods=['GET'])
def get_nononcological_drugs():
    response = proccesing_response_nononcological()
    r = json.dumps(response, indent=4)            
    logger.info("Sending the results: ")
    response = make_response(r, 200)
    response.mimetype = "application/json"
    return response


@app.route('/')
def render_static_home():
    return render_template('index.html')  

def main(*args):
    if len(args) == 1:
        myhost = args[0]
    else:
        myhost = "0.0.0.0"
    app.run(debug=False, host=myhost)
    
if __name__ == '__main__':
     main(*sys.argv[1:])
