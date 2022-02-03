import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from pyDatalog import pyDatalog
from pyDatalog.pyDatalog import assert_fact, load, ask

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph
import json
from math import comb


def build_query_clarify(input_cui, type_ddi):
    input_cui_uri = ','.join(['<http://clarify2020.eu/entity/' + cui + '>' for cui in input_cui])
    query = """
    select distinct ?EffectorDrugLabel ?AffectedDrugLabel ?Effect ?Impact ?precipitantDrug ?objectDrug
        where {""" + type_ddi + """        
        ?s <http://clarify2020.eu/vocab/effect_cui> ?o . 
        ?o <http://clarify2020.eu/vocab/annLabel> ?Effect . 
        ?s <http://clarify2020.eu/vocab/impact> ?Impact .
        ?s <http://clarify2020.eu/vocab/precipitant_drug_cui> ?precipitantDrug .
        ?s <http://clarify2020.eu/vocab/object_drug_cui> ?objectDrug .
        ?precipitantDrug <http://clarify2020.eu/vocab/annLabel> ?EffectorDrugLabel.
        ?objectDrug <http://clarify2020.eu/vocab/annLabel> ?AffectedDrugLabel.

    FILTER (?precipitantDrug in (""" + input_cui_uri + """ ) && ?objectDrug in (""" + input_cui_uri + """))
    }"""
    return query


def store_pharmacokinetic_ddi(effect):
    if effect in ['Excretion_rate', 'Excretory_function']:
        effect = 'excretion'
    elif effect in ['Process_of_absorption']:
        effect = 'absorption'
    elif effect in ['Serum_concentration', 'Serum_concentration_of', 'Serum_level']:
        effect = 'serum_concentration'
    elif effect in ['Metabolism']:
        effect = 'metabolism'
    # else:
    #    return 'pharmacodynamic'
    return effect


def rename_impact(impact):
    if impact in ['Increase', 'Higher', 'Worsening']:
        return 'increase'
    return 'decrease'


def query_result_clarify(query, endpoint):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dd = {'EffectorDrugLabel': [], 'AffectedDrugLabel': [], 'Effect': [], 'Impact': [], 'precipitantDrug': [],
          'objectDrug': []}
    for r in results['results']['bindings']:
        effect = r['Effect']['value']
        effect = store_pharmacokinetic_ddi(effect)
        if effect == 'pharmacodynamic':
            continue
        dd['Effect'].append(effect.lower())
        impact = r['Impact']['value'].replace('http://clarify2020.eu/entity/', '')
        impact = rename_impact(impact)
        dd['Impact'].append(impact)
        dd['EffectorDrugLabel'].append(r['EffectorDrugLabel']['value'].lower())
        dd['AffectedDrugLabel'].append(r['AffectedDrugLabel']['value'].lower())
        dd['precipitantDrug'].append(r['precipitantDrug']['value'].replace('http://clarify2020.eu/entity/', ''))
        dd['objectDrug'].append(r['objectDrug']['value'].replace('http://clarify2020.eu/entity/', ''))

    set_DDIs = pd.DataFrame(dd)

    return set_DDIs


def query_result_symmetric_clarify(query, endpoint):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dd = {'EffectorDrugLabel': [], 'AffectedDrugLabel': [], 'Effect': [], 'Impact': [], 'precipitantDrug': [],
          'objectDrug': []}
    for r in results['results']['bindings']:
        effect = r['Effect']['value']
        effect = store_pharmacokinetic_ddi(effect)
        if effect == 'pharmacodynamic':
            continue
        dd['Effect'].append(effect.lower())
        impact = r['Impact']['value'].replace('http://clarify2020.eu/entity/', '')
        impact = rename_impact(impact)
        dd['Impact'].append(impact)
        dd['EffectorDrugLabel'].append(r['AffectedDrugLabel']['value'].lower())
        dd['AffectedDrugLabel'].append(r['EffectorDrugLabel']['value'].lower())
        dd['precipitantDrug'].append(r['objectDrug']['value'].replace('http://clarify2020.eu/entity/', ''))
        dd['objectDrug'].append(r['precipitantDrug']['value'].replace('http://clarify2020.eu/entity/', ''))

    set_DDIs = pd.DataFrame(dd)
    # lowerify_cols = [col for col in set_DDIs if col not in ['precipitantDrug', 'objectDrug']]
    # set_DDIs[lowerify_cols] = set_DDIs[lowerify_cols].apply(lambda x: x.astype(str).str.lower(), axis=1)
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


def extract_ddi(onco_drugs, non_onco_drugs, endpoint):
    input_cui = onco_drugs + non_onco_drugs

    # ===== Endpoint 'clarify2020' =====
    asymmetric_ddi = """    ?s a <http://clarify2020.eu/vocab/DrugDrugInteraction> . 
                     """
    symmetric_ddi = """     ?sim a <http://clarify2020.eu/vocab/SymmetricDrugDrugInteraction> . 
                            ?sim <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?s.
                    """
    query = build_query_clarify(input_cui, asymmetric_ddi)
    set_DDIs = query_result_clarify(query, endpoint)
    query = build_query_clarify(input_cui, symmetric_ddi)
    corpus_symmetric = query_result_symmetric_clarify(query, endpoint)

    set_DDIs = combine_col(set_DDIs, ['Effect', 'Impact'])
    corpus_symmetric = combine_col(corpus_symmetric, ['Effect', 'Impact'])
    adverse_event = corpus_symmetric.Effect_Impact.unique()
    union = pd.concat([set_DDIs, corpus_symmetric])

    set_dsd_label = get_drug_label_by_category(onco_drugs, union)
    comorbidity_drug = get_drug_label_by_category(non_onco_drugs, union)
    set_DDIs = set_DDIs[['EffectorDrugLabel', 'AffectedDrugLabel', 'Effect_Impact']]
    return adverse_event, union, set_dsd_label, comorbidity_drug, set_DDIs


def load_data(file):
    onco_drugs = file["Input"]["OncologicalDrugs"]
    non_onco_drugs = file["Input"]["Non_OncologicalDrugs"]
    # onco_drugs = file["oncological_drug"]
    # non_onco_drugs = file["non_oncological_drug"]
    return extract_ddi(onco_drugs, non_onco_drugs, "https://labs.tib.eu/sdm/clarify-kg-5-1/sparql")


pyDatalog.create_terms('rdf_star_triple, inferred_rdf_star_triple, wedge, A, B, C, T, T2, wedge_pharmacokinetic')


def build_datalog_model(union):
    pyDatalog.clear()
    for d in union.values:
        # Extensional Database
        assert_fact('rdf_star_triple', d[0], d[1], d[2])
    # Intentional Database
    inferred_rdf_star_triple(A, B, T) <= rdf_star_triple(A, B, T)  # & (T._in(ddiTypeToxicity))
    inferred_rdf_star_triple(A, C, T2) <= inferred_rdf_star_triple(A, B, T) & rdf_star_triple(B, C, T2) & (
        T._in(ddiTypeToxicity)) & (T2._in(ddiTypeToxicity)) & (A != C)

    inferred_rdf_star_triple(A, B, T) <= rdf_star_triple(A, B, T)  # & (T._in(ddiTypeEffectiveness))
    inferred_rdf_star_triple(A, C, T2) <= inferred_rdf_star_triple(A, B, T) & rdf_star_triple(B, C, T2) & (
        T._in(ddiTypeEffectiveness)) & (T2._in(ddiTypeEffectiveness)) & (A != C)

    wedge(A, B, C, T, T2) <= inferred_rdf_star_triple(A, B, T) & inferred_rdf_star_triple(B, C, T2) & (A != C)

    wedge_pharmacokinetic(A, B, C, T, T2) <= inferred_rdf_star_triple(A, B, T) & inferred_rdf_star_triple(B, C, T2) & (
        T._in(pharmacokinetic_ddi)) & (T2._in(pharmacokinetic_ddi)) & (A != C)


def computing_wedge(set_drug_label, ddi_type):
    dict_frequency = dict()
    dict_frequency_k = dict()
    max_wedge = len(ddi_type) * comb(len(set_drug_label) - 1, 2)

    ddi_k = set.intersection(set(ddi_type), set(pharmacokinetic_ddi))
    max_wedge_k = len(ddi_k) * comb(len(set_drug_label) - 1, 2)
    #print(n_ddi, len(set_drug_label), max_wedge)
    for d in set_drug_label:
        w = wedge(A, d, C, T, T2)
        dict_frequency[d] = len(w) / max_wedge

        w_k = wedge_pharmacokinetic(A, d, C, T, T2)
        dict_frequency_k[d] = len(w_k) / max_wedge_k
    return dict_frequency, dict_frequency_k


ddiTypeToxicity = ["serum_concentration_increase", "metabolism_decrease", "absorption_increase", "excretion_decrease"]
ddiTypeEffectiveness = ["serum_concentration_decrease", "metabolism_increase", "absorption_decrease",
                        "excretion_increase"]
pharmacokinetic_ddi = ddiTypeToxicity + ddiTypeEffectiveness


def discovering_knowledge(adverse_event, union, set_dsd_label, comorbidity_drug):
    dict_wedge = dict()
    plot_ddi = union[['EffectorDrugLabel', 'AffectedDrugLabel', 'Effect_Impact']]
    plot_ddi.drop_duplicates(keep='first', inplace=True)
    build_datalog_model(plot_ddi)
    ddi_type = plot_ddi.Effect_Impact.unique()
    dict_frequency, dict_frequency_k = computing_wedge(comorbidity_drug.union(set_dsd_label), ddi_type)
    dict_frequency = dict(sorted(dict_frequency.items(), key=lambda item: item[1], reverse=True))
    dict_wedge['toxicity_rate'] = dict_frequency
    dict_wedge['most_toxic_drug'] = max(dict_frequency, key=dict_frequency.get)

    dict_frequency_k = dict(sorted(dict_frequency_k.items(), key=lambda item: item[1], reverse=True))
    dict_wedge['pharmacokinetic_toxicity_rate'] = dict_frequency_k
    dict_wedge['most_toxic_drug_pharmacokinetic'] = max(dict_frequency_k, key=dict_frequency_k.get)
    return dict_wedge
