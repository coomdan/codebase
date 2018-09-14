addressbook = {
  "1" :  { 
    "Vorname": "Daniel",
    "Nachname": "Aschenneller" }, 
  "2" : { 
    "Vorname": "Eduard",
    "Nachname": "Regehr" } 
  }
print(addressbook)


for id in addressbook:
  print("--")
  for key in addressbook[id]:
    print("---  {:10} :  {:30}".format(key, addressbook[id][key]))
