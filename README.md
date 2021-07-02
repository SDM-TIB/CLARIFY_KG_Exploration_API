# CLARIFY-KG-Exploration-API

The CLARIFY KG stores pharmacokinetic interactions at the absorption and excretion levels, and pharmacokinetic interactions at the drug metabolism level:

Drug Absorption: Process in which a pharmaceutical substance enters into the blood circulation in the body. 
Omeprazole can increase the absorption rate of  Raltegravir

Drug Metabolism: Mechanism in which a pharmaceutical substance is transformed into other substances called metabolites in the body. 
Omeprazole  can increase metabolism of  Etoposide
Drug Excretion: Process in which a pharmaceutical substance is removed from the body. 

Codeine  can decrease the excretion of  Cisplatin

Drug Serum Concentration: The amount of a drug or other compound in the circulation, both bound to proteins and unbound, the latter of which generally corresponds to the therapeutically active fraction.

Codeine  can increase serum concentration of  Cisplatin
Furthermore, the CLARIFY KG comprises pharmacodynamic interactions among drugs.  
The interaction between Trazodone and Acetylsalicylic acid can increase gastrointestinal bleeding 


# 1) Get Interactions of only Oncological and NonOncological drugs

## Input 

list of drugs CUIs

```
{
   "Drugs":[
    "C0028978",
    "C0015846",
    "C3657270"
   ]
}
```

## Output
Drug-Drug-Interactions with only ncological and NonOncological drugs for the input drugs

```
  "C0015846": {
            "DDI": {
                "Symmetric": [
                    {
                        "Drug1": "Trazodone",
                        "Drug2": "Fentanyl",
                        "effect": "Serotonin syndrome",
                        "impact": "Increase",
                        "description": "The risk or severity of serotonin syndrome can be increased when Trazodone is combined with Fentanyl."
                    },
                    {
                        "Drug1": "Tramadol",
                        "Drug2": "Fentanyl",
                        "effect": "Serotonin syndrome",
                        "impact": "Increase",
                        "description": "The risk or severity of serotonin syndrome can be increased when Tramadol is combined with Fentanyl."
                    },
		    
		    ..........
		      "NonSymmetric": [
                    {
                        "effectorDrug": "Ertapenem",
                        "affectdDrug": "Fentanyl",
                        "effect": "Serum level",
                        "impact": "Decrease",
                        "description": "Ertapenem may decrease the excretion rate of Fentanyl which could result in a higher serum level."
                    },
                    {
                        "effectorDrug": "Metformin",
                        "affectdDrug": "Fentanyl",
                        "effect": "Serum level",
                        "impact": "Decrease",
                        "description": "Metformin may decrease the excretion rate of Fentanyl which could result in a higher serum level."
                    },
	}
   }
```

## POST request example

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
   "Drugs":[
    "C0028978",
    "C0015846",
    "C3657270"
   ]
}' \
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDI&limit=10&page=0&all_drugs=0
```

# 2) DDIGroupDrugs API

## Input
List of CUIs for Oncological and NonOncological drugs

```
	{
	     "Input":{"OncologicalDrugs":["C0015133","C0079083","C0377401","C0377401","C0008838","C0078257"],"Non_OncologicalDrugs":["C0009214","C0028978","C0064636","C0207683","C1871526"]}

	}
```
## Output
 List of DDI interactions and list of drugs effects
 
 ```
 {
    "DDIs": [
        "Codeine  can increase serum concentration of  Cisplatin",
        "Carboplatin  can increase serum concentration of  Codeine",
        "Carboplatin  can increase serum concentration of  Lamotrigine",
        "Omeprazole  can increase serum concentration of  Raltegravir",
        "Omeprazole  can increase serum concentration of  Raltegravir",
        "Omeprazole  can increase serum concentration of  Raltegravir",
    ],
    "DrugEffects": {
        "C0008838": [
            "The effectiveness of  Cisplatin can be decreased because Codeine  can decrease serum concentration of  Cisplatin",
            "The effectiveness of  Cisplatin can be decreased because Carboplatin  can decrease serum concentration of  Codeine"
        ],
        "C0009214": [
            "The effectiveness of  Codeine can be decreased because Carboplatin  can decrease serum concentration of  Codeine"
        ],
        "C0064636": [
            "The effectiveness of  Lamotrigine can be decreased because Carboplatin  can decrease serum concentration of  Lamotrigine"
        ],
        "C1871526": [
            "The effectiveness of  Raltegravir can be decreased because Lamotrigine  can increase metabolism of  Raltegravir",
            "The effectiveness of  Raltegravir can be decreased because Carboplatin  can decrease serum concentration of  Lamotrigine"
        ],
        "C0207683": [
            "The toxicity of  Nafamostat can be increased because Cisplatin  can increase serum concentration of  Nafamostat",
            "The toxicity of  Nafamostat can be increased because Lamotrigine  can increase serum concentration of  Nafamostat",
            "The toxicity of  Nafamostat can be increased because Codeine  can increase serum concentration of  Cisplatin",
            "The toxicity of  Nafamostat can be increased because Codeine  can decrease the excretion of  Cisplatin",
            "The toxicity of  Nafamostat can be increased because Carboplatin  can increase serum concentration of  Codeine",
            "The toxicity of  Nafamostat can be increased because Omeprazole  can decrease metabolism of  Codeine",
            "The toxicity of  Nafamostat can be increased because Vinorelbine  can decrease metabolism of  Codeine",
            "The toxicity of  Nafamostat can be increased because Carboplatin  can decrease the excretion of  Codeine"
        ]
    }
}
 ```

## Post request example

```
curl --location --request POST 'https://labs.tib.eu/sdm/clarify-exp/ddi' \
--header 'Content-Type: application/json' \
--data-raw '	{
	     "Input":{"OncologicalDrugs":["C0015133","C0079083","C0377401","C0377401","C0008838","C0078257"],"Non_OncologicalDrugs":["C0009214","C0028978","C0064636","C0207683","C1871526"]}

	}'
```

# 3) Get Interactions of all drug types


## Input 

list of drugs CUIs

```
{
   "Drugs":[
    "C0028978",
    "C0015846",
    "C3657270"
   ]
}
```

## Output
Drug-Drug-Interactions regardless of the type of the drugs for the input drugs

```
{
    "response": {
        "C0028978": {
            "DDI": {
                "Symmetric": [
                    {
                        "Drug1": "Omeprazole",
                        "Drug2": "Citalopram",
                        "effect": "Qtc prolongation",
                        "impact": "Increase",
                        "description": "The risk or severity of QTc prolongation can be increased when Omeprazole is combined with Citalopram."
                    },
                    {
                        "Drug1": "Omeprazole",
                        "Drug2": "Ropinirole",
                        "effect": "Adverse effects",
                        "impact": "Increase",
                        "description": "The risk or severity of adverse effects can be increased when Omeprazole is combined with Ropinirole."
                    }
                ],
                "NonSymmetric": [
                    {
                        "effectorDrug": "Captopril",
                        "affectdDrug": "Omeprazole",
                        "effect": "Absorption",
                        "impact": "Decrease",
                        "description": "Captopril can cause a decrease in the absorption of Omeprazole resulting in a reduced serum concentration and potentially a decrease in efficacy."
                    },
 {
                        "effectorDrug": "Ketoconazole",
                        "affectdDrug": "Omeprazole",
                        "effect": "Absorption",
                        "impact": "Reduced",
                        "description": "Ketoconazole can cause a decrease in the absorption of Omeprazole resulting in a reduced serum concentration and potentially a decrease in efficacy."
                    },
```

## POST request example

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
   "Drugs":[
    "C0028978",
    "C0015846",
    "C3657270"
   ]
}' \
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDIS&all_drugs=1
```

# 4) Get all the interaction among the provided Drugs

## Input 

list of drugs CUIs

```
{
   "Drugs":[
    "C0028978",
    "C0015846",
    "C3657270"
   ]
}
```

## Output
Drug-Drug-Interactions for all the pairs of input drugs

```
"('C0015846', 'C0028978')": {
            "Labels": "Fentanyl AND Omeprazole",
            "DDIS": [
                {
                    "effectorDrug": "Omeprazole",
                    "affectdDrug": "Fentanyl",
                    "effect": "Metabolism",
                    "impact": "Decrease",
                    "description": "The metabolism of Fentanyl can be decreased when combined with Omeprazole."
                }
            ]
        },
```

## POST request example
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
   "Drugs":[
    "C0028978",
    "C0015846",
    "C3657270"
   ]
}' \
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDIS&limit=10&page=0
```

# 5) Get the predicted interactions of only Oncological and NonOncological drugs 

## Input 

list of drugs CUIs

```
{
   "Drugs":[
    "C1135135",
    "C1122962",
    "C0008838",
    "C0052796"
   ]
}
```

## Output
Predicted Drug-Drug-Interactions with only ncological and NonOncological drugs for the input drugs

```
        "C0028978": {
            "Label": "Omeprazole",
            "DDIP": [
                {
                    "effectorDrug": "Chlorpromazine",
                    "affectdDrug": "Omeprazole",
                    "confidence": "0.178",
                    "provenance": "LapRLS Algorithm Prediction"
                },
                {
                    "effectorDrug": "Dexketoprofen",
                    "affectdDrug": "Omeprazole",
                    "confidence": "0.1802",
                    "provenance": "LapRLS Algorithm Prediction"
                }
            ]
        },
```

## POST request example

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
   "Drugs":[
    "C1135135",
    "C1122962",
    "C0008838",
    "C0052796"
   ]
}' \
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDIP&all_drugs=0
```


# 6) Get the predicted interactions of all drugs types

## Input 

list of drugs CUIs

```
{
   "Drugs":[
    "C0028978",
    "C0030049",
    "C0040805"
   ]
}
```

## Output
Predicted Drug-Drug-Interactions regardless of the type of the drugs for the input drugs

```
{
    "response": {
        "C0028978": {
            "Label": "Omeprazole",
            "DDIP": [
                {
                    "effectorDrug": "Chlorpromazine",
                    "affectdDrug": "Omeprazole",
                    "confidence": "0.178",
                    "provenance": "LapRLS Algorithm Prediction"
                },
                {
                    "effectorDrug": "Dexketoprofen",
                    "affectdDrug": "Omeprazole",
                    "confidence": "0.1802",
                    "provenance": "LapRLS Algorithm Prediction"
                }
            ]
        },
        "C0030049": {
            "Label": "Oxycodone",
            "DDIP": [
                {
                    "effectorDrug": "16-bromoepiandrosterone",
                    "affectdDrug": "Oxycodone",
                    "confidence": "0.6667",
                    "provenance": "semEP Algorithm Prediction"
                },
                {
                    "effectorDrug": "4-methoxyamphetamine",
                    "affectdDrug": "Oxycodone",
                    "confidence": "0.1759",
                    "provenance": "LapRLS Algorithm Prediction"
                }
            ]
        },
```

## POST request example

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
   "Drugs":[
    "C0028978",
    "C0030049",
    "C0040805"
   ]
}' \
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDIP&limit=10&page=0&all_drugs=1
```

# 7) Get all the predicted interaction among the provided Drugs

## Input 

list of drugs CUIs

```
{
   "Drugs":[
    "C1135135",
    "C1122962",
    "C0008838",
    "C0052796"
   ]
}
```

## Output
Predicted Drug-Drug-Interactions for all the pairs of input drugs

```
{
    "response": {
        "('C1122962', 'C1135135')": {
            "Labels": "Erlotinib AND Gefitinib",
            "DDIPS": [
                {
                    "effectorDrug": "Gefitinib",
                    "affectdDrug": "Erlotinib",
                    "confidence": "0.5",
                    "provenance": "semEP Algorithm Prediction"
                }
            ]
        },
	 "('C0008838', 'C0052796')": {
            "Labels": "Cisplatin AND Azithromycin",
            "DDIPS": [
                {
                    "effectorDrug": "Azithromycin",
                    "affectdDrug": "Cisplatin",
                    "confidence": "0.8161",
                    "provenance": "Bipartite Local Method Prediction"
                }
            ]
        },
	
```

## POST request example

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
   "Drugs":[
    "C1135135",
    "C1122962",
    "C0008838",
    "C0052796"
   ]
}' \
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDIPS&limit=10&page=0
```

# 8) Get absorption of a drug

Drug Absorption: Process in which a pharmaceutical substance enters into the blood circulation in the body. 

## Input 

list of drugs CUIs

```
{
   "Drugs":[
    "C0028978",
    "C0015846",
    "C3657270"
   ]
}
```

## Output
The coresponding absorption for each input drug

```
        "C0028978": {
            "absorption": [
                {
                    "drug": "Omeprazole",
                    "absorption": "Omeprazole delayed-release capsules contain an enteric-coated granule formulation of omeprazole (because omeprazole is acid-labile), so that absorption of omeprazole begins only after the granules exit the stomach [FDA label]. \n\nAbsorption of omeprazole occurs rapidly, with peak plasma concentrations of omeprazole achieved within 0.5-3.5 hours [FDA label]. \n\nAbsolute bioavailability (compared with intravenous administration) is approximately 30-40% at doses of 20-40 mg, largely due to pre-systemic metabolism. The bioavailability of omeprazole increases slightly upon repeated administration of omeprazole delayed-release capsules [FDA label]."
                }
            ]
        },
```

## POST request example

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
   "Drugs":[
    "C0028978",
    "C0015846",
    "C3657270"
   ]
}' \
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=absorption
```
# 9) Get mechanism of action of a drug

Drug Metabolism: Mechanism in which a pharmaceutical substance is transformed into other substances called metabolites in the body. 

## Input 

list of drugs CUIs

```
{
   "Drugs":[
    "C0028978",
    "C0015846",
    "C3657270"
   ]
}
```

## Output
The coresponding mechanism of actions for each input drug

```
{
    "response": {
        "C0028978": {
            "MOA": [
                {
                    "drug": "Omeprazole",
                    "MechanismOfAction": "Hydrochloric acid (HCl) secretion into the gastric lumen is a process regulated mainly by the H(+)/K(+)-ATPase of the proton pump [A175180], expressed in high quantities by the parietal cells of the stomach. ATPase is an enzyme on the parietal cell membrane that facilitates hydrogen and potassium exchange through the cell, which normally results in the extrusion of potassium and formation of HCl (gastric acid) [A174295].\n\nOmeprazole is a member of a class of antisecretory compounds, the substituted _benzimidazoles_, that stop gastric acid secretion by selective inhibition of the _H+/K+ ATPase_ enzyme system. Proton-pump inhibitors such as omeprazole bind covalently to cysteine residues via disulfide bridges on the alpha subunit of the _H+/K+ ATPase_ pump, inhibiting gastric acid secretion for up to 36 hours [A175192].  This antisecretory effect is dose-related and leads to the inhibition of both basal and stimulated acid secretion, regardless of the stimulus [FDA label].  \n\n**Mechanism of H. pylori eradication**\n\nPeptic ulcer disease (PUD) is frequently associated with _Helicobacter pylori_ bacterial infection (NSAIDs) [A175195]. The treatment of H. pylori infection may include the addition of omeprazole or other proton pump inhibitors as part of the treatment regimen [FDA label], [A175198]. \n_H. pylori_ replicates most effectively at a neutral pH [A175213]. Acid inhibition in H. pylori eradication therapy, including proton-pump inhibitors such as omeprazole, raises gastric pH, discouraging the growth of H.pylori [A175198]. It is generally believed that proton pump inhibitors inhibit the _urease_ enzyme, which increases the pathogenesis of H. pylori in gastric-acid related conditions [A175216]."
                }
            ]
        },
        "C0015846": {
            "MOA": [
                {
                    "drug": "Fentanyl",
                    "MechanismOfAction": "Fentanyl binds to opioid receptors, especially the mu opioid receptor, which are coupled to G-proteins.[A179533] Activation of opioid receptors causes GTP to be exchanged for GDP on the G-proteins which in turn down regulates adenylate cyclase, reducing concentrations of cAMP.[A179533] Reduced cAMP decreases cAMP dependant influx of calcium ions into the cell.[A179533] The exchange of GTP for GDP results in hyperpolarization of the cell and inhibition of nerve activity.[A179533]"
                }
            ]
        },
```

## POST request example


```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
   "Drugs":[
    "C0028978",
    "C0015846",
    "C3657270"
   ]
}' \
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=MOA
```

