# CLARIFY-KG-Exploration-API



# 1) Get Interactions of a Drug

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
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDI&limit=10&page=0
```

# 2) Get Interactions of a Drug (only Oncological and NonOncological drugs interactions) 
parameter all_drug=0 stricts the interactions to only Oncological and NonOncological drugs interactions

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
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDI&all_drugs=0
```

# 3) Get all the interaction among the provided Drugs


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

# 4) Get the predicted interactions of a Drug


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
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDIP&limit=10&page=0
```


# 5) Get the predicted interactions of a Drug (only Oncological and NonOncological drugs interactions) 

parameter all_drug=0 stricts the predicted interactions to only Oncological and NonOncological drugs interactions

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

# 6) Get all the predicted interaction among the provided Drugs


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
