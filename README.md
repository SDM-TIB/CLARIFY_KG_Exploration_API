# CLARIFY-KG-Exploration-API



# 1) Get Interactions of a Drug

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
   "Drugs":[
  	"C0000970",
  	"C0028978",
  	"C0009214"
   ]
}' \
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDI&limit=10&page=0
```

# 2) Get all the interaction among the provided Drugs


```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
   "Drugs":[
  	"C0000970",
  	"C0028978",
  	"C0009214"
   ]
}' \
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDIS&limit=10&page=0
```

# 3) Get the predicted interactions of a Drug


```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
   "Drugs":[
  	"C0000970",
  	"C0028978",
  	"C0009214"
   ]
}' \
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDIP&limit=10&page=0
```

# 4) Get all the predicted interaction among the provided Drugs


```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
   "Drugs":[
    "C0013618",
  	"C0010592",
  	"C0043822"
   ]
}' \
  https://labs.tib.eu/sdm/clarify-exp/kg-exp?target=DDIPS&limit=10&page=0
```
