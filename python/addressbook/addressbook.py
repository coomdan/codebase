##addressbook = {
##  1 :  { 
##    "Vorname": "Daniel",
##    "Nachname": "Aschenneller" }, 
##  2 : { 
##    "Vorname": "Eduard",
##    "Nachname": "Regehr" } 
##  }
addressbook = {}
def show_entries():
  for id in addressbook:
    print("-- {}".format(id))
    for key in addressbook[id]:
      print("---  {:10} :  {:30}".format(key, addressbook[id][key]))

def add_entry(vorname, nachname):
  print(addressbook.keys())
  new_id = max(addressbook.keys()) + 1
  print("...adding new id {}".format(new_id))
  addressbook[new_id] = {}
  addressbook[new_id]["Vorname"] = vorname
  addressbook[new_id]["Nachname"] = nachname

def del_entry_by_id(id):
  if addressbook.pop(id, None):
    print("{} deleted".format(id))
  else:
    print("{} NOT deleted, does not exist".format(id))

def find_key_by_name(name):
  idlist = []
  for id in addressbook:
    for key, value in addressbook[id].items():
      if name == value:
        print("Found {} in ID {}".format(name, id))
        idlist.append(id)
  return idlist      

def write_to_file(filename, ab):
  with open(filename,'w') as file:
    file.write(str(ab))

def read_from_file(filename):
  with open(filename,'r') as file:
    ab = eval(file.read())
    return ab

addressbook = read_from_file("addressbook.asche")
print(addressbook)
mandatoryfields = ["Vorname", "Nachname", "Telefon"]



add_entry("hans","peter")
add_entry("sepp","dieter")
add_entry("sepp","dieter")
del_entry_by_id(3)
del_entry_by_id(6)
ids = find_key_by_name("dieter")
for id in ids:
  del_entry_by_id(id)
add_entry("Josef","Gruber")
show_entries()
write_to_file("addressbook.asche", addressbook)
ab = read_from_file("addressbook.asche")
print(ab)
