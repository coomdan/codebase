import sys, os.path

def does_file_exist(pp):
  if os.path.isfile(pp):
    print("Exists!")
    return True

def do_we_have_enough_args():
  if len(sys.argv) < 2:
    print("No args given, using default")
    path = "/tmp/"
    pattern = "test"
  else:
    pattern = sys.argv[1]
  return(path + pattern)

def read_file(pp):
  with open(pp) as file:
    test = file.readlines()
    return test

def push_to_array(lines, linearray):
  for line in lines:
    linearray.append(line.strip())
linearray = []
pp = do_we_have_enough_args()
if does_file_exist(pp):
  lines = read_file(pp)
  push_to_array(lines, linearray)
  
      
print(linearray)
