import json
import pandas as pd
pd.options.mode.chained_assignment = None
from pyDatalog import pyDatalog
from pyDatalog.pyDatalog import assert_fact, load, ask
from SPARQLWrapper import SPARQLWrapper, JSON
import os

KG = os.environ["ENDPOINT"]
# KG ='https://labs.tib.eu/sdm/clarify_kg/sparql'
# KG = 'http://node2.research.tib.eu:12200/sparql'


def execute_query(query, limit=0, page=0):
    if limit != 0:
        query += "LIMIT " + str(limit)
    query += " OFFSET " + str(page)
    sparql_ins = SPARQLWrapper(KG)
    sparql_ins.setQuery(query)
    sparql_ins.setReturnFormat(JSON)
    return sparql_ins.query().convert()


def create_filter_cui(input_cui):
    return ','.join(['<http://research.tib.eu/clarify2020/entity/' + cui + '>' for cui in input_cui])


def build_query_clarify(input_cui_uri):
    query = """
    prefix clarify: <http://research.tib.eu/clarify2020/vocab/>
    select distinct ?EffectorDrugLabel ?AffectedDrugLabel ?Effect ?Impact ?precipitantDrug ?objectDrug ?type
        where {
        {{?s a clarify:DrugDrugInteraction .  BIND('Pharmacokinetics' as ?type)} 
        UNION {?sim a clarify:SymmetricDrugDrugInteraction . 
                            ?sim <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?s.BIND('Pharmadynamics' as ?type) }}
        ?s clarify:effect_cui ?o . 
        ?o clarify:annLabel ?Effect . 
        ?s clarify:impact ?Impact .
        ?s clarify:precipitant_drug_cui ?precipitantDrug .
        ?s clarify:object_drug_cui ?objectDrug .
        ?precipitantDrug clarify:annLabel ?EffectorDrugLabel.
        ?objectDrug clarify:annLabel ?AffectedDrugLabel.

    FILTER (?precipitantDrug in (""" + input_cui_uri + """ ) && ?objectDrug in (""" + input_cui_uri + """))
    }"""
    return query


def store_pharmacokinetic_ddi(effect):
    if effect in ['excretion_rate', 'excretory_function', 'excretion', 'excretion rate']:
        effect = 'excretion'
    elif effect in ['process_of_absorption', 'process of absorption', 'absorption']:
        effect = 'absorption'
    elif effect in ['serum_concentration', 'serum_concentration_of', 'serum_level', 'serum_globulin_level',
                    'metabolite', 'active_metabolites', 'serum concentration']:
        effect = 'serum_concentration'
    elif effect in ['metabolism']:
        effect = 'metabolism'
    else:
        if effect == 'adverse effects':
            effect = 'adverse_effects'
        return effect, True
    return effect, False


def rename_impact(impact):
    if impact in ['Increase', 'Higher', 'Worsening']:
        return 'increase'
    return 'decrease'


def get_Labels(input_cui_uri):
    labels = {}
    query = """select distinct ?Drug ?drugLabel \n 
    where {?Drug <http://research.tib.eu/clarify2020/vocab/annLabel> ?drugLabel.\n 
    FILTER (?Drug in (""" + input_cui_uri + """ ))}\n"""

    results = execute_query(query, limit=0, page=0)
    for row in results["results"]["bindings"]:
        labels[row["Drug"]["value"].replace("http://research.tib.eu/clarify2020/entity/", "")] = row["drugLabel"][
            "value"].lower()
    return list(labels.values())


def query_result_clarify(query, labels):
    results = execute_query(query, limit=0, page=0)
    prefix = 'http://research.tib.eu/clarify2020/entity/'
    dd = {'EffectorDrugLabel': [], 'AffectedDrugLabel': [], 'Effect': [], 'Impact': [], 'precipitantDrug': [],
          'objectDrug': []}
    for r in results['results']['bindings']:
        effect = r['Effect']['value'].lower()
        effect, pharmadynamic = store_pharmacokinetic_ddi(effect)
        dd['Effect'].append(effect.lower())
        impact = r['Impact']['value'].replace(prefix, '')
        impact = rename_impact(impact)
        dd['Impact'].append(impact)

        dd['EffectorDrugLabel'].append(r['EffectorDrugLabel']['value'].lower())
        dd['AffectedDrugLabel'].append(r['AffectedDrugLabel']['value'].lower())
        dd['precipitantDrug'].append(r['precipitantDrug']['value'].replace(prefix, ''))
        dd['objectDrug'].append(r['objectDrug']['value'].replace(prefix, ''))

        if pharmadynamic:
            dd['Effect'].append(effect.lower())
            impact = r['Impact']['value'].replace(prefix, '')
            impact = rename_impact(impact)
            dd['Impact'].append(impact)
            dd['EffectorDrugLabel'].append(r['AffectedDrugLabel']['value'].lower())
            dd['AffectedDrugLabel'].append(r['EffectorDrugLabel']['value'].lower())
            dd['precipitantDrug'].append(r['objectDrug']['value'].replace(prefix, ''))
            dd['objectDrug'].append(r['precipitantDrug']['value'].replace(prefix, ''))

    set_DDIs = pd.DataFrame(dd)
    set_DDIs = set_DDIs.loc[set_DDIs.EffectorDrugLabel.isin(labels)]
    set_DDIs = set_DDIs.loc[set_DDIs.AffectedDrugLabel.isin(labels)]
    set_DDIs.drop_duplicates(inplace=True)
    return set_DDIs


def combine_col(corpus, cols):
    # corpus = corpus.apply(lambda x: x.astype(str).str.lower())
    name = '_'.join(cols)
    corpus[name] = corpus[cols].apply(lambda x: '_'.join(x.values.astype(str)), axis=1)
    return corpus


def get_drug_label_by_category(drugs_cui, set_DDIs):
    d_label = set(set_DDIs.loc[set_DDIs.precipitantDrug.isin(drugs_cui)].EffectorDrugLabel.unique())
    d_label.update(set_DDIs.loc[set_DDIs.objectDrug.isin(drugs_cui)].AffectedDrugLabel.unique())
    return d_label


def extract_ddi(file):
    onco_drugs = file["Input"]["OncologicalDrugs"]
    non_onco_drugs = file["Input"]["Non_OncologicalDrugs"]

    input_cui = onco_drugs + non_onco_drugs
    input_cui_uri = create_filter_cui(input_cui)
    """extracting DDIs"""
    labels = get_Labels(input_cui_uri)
    query = build_query_clarify(input_cui_uri)
    # print(query)
    union = query_result_clarify(query, labels)
    union = combine_col(union, ['Effect', 'Impact'])
    union = union.reset_index()
    union = union.drop(columns=['index'])
    set_dsd_label = get_drug_label_by_category(input_cui, union)

    return union, set_dsd_label


pyDatalog.create_terms('ddi_triple, deduced_ddi_triple, A, B, C, T, T2')


def build_datalog_model(ddi):
    pyDatalog.clear()
    for d in ddi.values:
        # Extensional Database
        assert_fact('ddi_triple', d[0], d[1], d[2])
    # Intentional Database
    deduced_ddi_triple(A, B, T) <= ddi_triple(A, B, T)
    deduced_ddi_triple(A, C, T2) <= deduced_ddi_triple(A, B, T) & ddi_triple(B, C, T2) & (
        T._in(ddiTypeToxicity)) & (T2._in(ddiTypeToxicity)) & (A != C)
    deduced_ddi_triple(A, B, T) <= ddi_triple(A, B, T)
    deduced_ddi_triple(A, C, T2) <= deduced_ddi_triple(A, B, T) & ddi_triple(B, C, T2) & (
        T._in(ddiTypeEffectiveness)) & (T2._in(ddiTypeEffectiveness)) & (A != C)


def get_indirect_ddi(indirect_ddi, dsd, deduced_ddi):
    for i in range(len(deduced_ddi)):
        t = deduced_ddi[i][1].split('_')
        effect = '_'.join(t[:-1])
        impact = t[-1]
        x = {'EffectorDrugLabel': [deduced_ddi[i][0]], 'AffectedDrugLabel': dsd,
             'Effect': effect, 'Impact': impact, 'Effect_Impact': deduced_ddi[i][1]}
        indirect_ddi = pd.concat([indirect_ddi, pd.DataFrame(data=x)])
    return indirect_ddi


def get_deduced_interaction(ddi, set_dsd_label):
    set_ddi = ddi[['EffectorDrugLabel', 'AffectedDrugLabel', 'Effect_Impact', 'Effect', 'Impact']]
    build_datalog_model(set_ddi)
    indirect_ddi = pd.DataFrame(columns=['EffectorDrugLabel', 'AffectedDrugLabel', 'Effect', 'Impact', 'Effect_Impact'])
    for dsd in set_dsd_label:
        deduced_ddi = deduced_ddi_triple(C, dsd, T)
        indirect_ddi = get_indirect_ddi(indirect_ddi, dsd, deduced_ddi)

    graph_ddi = pd.concat([set_ddi, indirect_ddi])
    graph_ddi.drop_duplicates(keep='first', inplace=True)
    return graph_ddi


def get_interaction_in_text(set_DDIs, ddi_edb):
    list_ddi = []
    drugEffects = dict()
    for drug in set_DDIs.AffectedDrugLabel.unique():
        drug_cui = ddi_edb.loc[ddi_edb.AffectedDrugLabel==drug].objectDrug.to_list()[0]
        ddi_s = set_DDIs.loc[set_DDIs.AffectedDrugLabel==drug]
        list_effect = []
        for i in range(ddi_s.shape[0]):
            ddi = ddi_s.iloc[i]['Effect_Impact']
            ddi_type = ddi_s.iloc[i]['EffectorDrugLabel'] + ' can ' + ddi_s.iloc[i]['Impact'] + ' ' + ddi_s.iloc[i][
                           'Effect'] + ' of ' + ddi_s.iloc[i]['AffectedDrugLabel']
            if ddi in ddiTypeToxicity:
                tox_increase = "The toxicity of " + ddi_s.iloc[i][
                    'AffectedDrugLabel'] + " is increased because " + ddi_type
                list_effect.append(tox_increase)
            elif ddi in ddiTypeEffectiveness:
                effectiv_decrease = "The effectiveness of " + ddi_s.iloc[i][
                    'AffectedDrugLabel'] + " is decreased because " + ddi_type
                list_effect.append(effectiv_decrease)
            list_ddi.append(ddi_type)
        drugEffects[drug_cui] = list_effect
    return drugEffects, list_ddi


ddiTypeToxicity = ["serum_concentration_increase", "metabolism_decrease", "absorption_increase", "excretion_decrease"]
ddiTypeEffectiveness = ["serum_concentration_decrease", "metabolism_increase", "absorption_decrease",
                        "excretion_increase"]
pharmacokinetic_ddi = ddiTypeToxicity + ddiTypeEffectiveness


def get_DDI(input_list):
    ddi, set_dsd_label = extract_ddi(input_list)
    df_ddi = get_deduced_interaction(ddi, set_dsd_label)
    response = dict()
    drugEffects, list_ddi = get_interaction_in_text(df_ddi, ddi)
    response["DDIs"] = list_ddi
    response["DrugEffects"] = drugEffects
    return response


if __name__ == '__main__':

    input_list = {
	     "Input":{"OncologicalDrugs":["C0015133"],"Non_OncologicalDrugs":["C0028978","C0061851"]}
	}
    ddi, set_dsd_label = extract_ddi(input_list)
    df_ddi = get_deduced_interaction(ddi, set_dsd_label)
    response = dict()
    drugEffects, list_ddi = get_interaction_in_text(df_ddi, ddi)
    response["DDIs"] = list_ddi
    response["DrugEffects"] = drugEffects
    r = json.dumps(response, indent=4)
    print(r)
