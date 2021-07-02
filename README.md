# CLARIFY-KG-Exploration-API



# 1) Get Interactions of only Oncological and NonOncological drugs

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


```
curl --location --request POST 'https://labs.tib.eu/sdm/clarify-exp/ddi' \
--header 'Content-Type: application/json' \
--data-raw '	{
	     "Input":{"OncologicalDrugs":["C0015133","C0079083","C0377401","C0377401","C0008838","C0078257"],"Non_OncologicalDrugs":["C0009214","C0028978","C0064636","C0207683","C1871526"]}

	}'
```

# 3) Get Interactions of all drug types


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
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDI&all_drugs=1
```

# 4) Get all the interaction among the provided Drugs


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
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDIP&limit=10&page=0&all_drugs=0
```


# 6) Get the predicted interactions of all drugs types
parameter all_drug=0 stricts the predicted interactions to only Oncological and NonOncological drugs interactions

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

