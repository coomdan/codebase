#
import glob, os.path, shutil

key_path = "key-files/"
input_dir = key_path + "unverified"
archive_dir = key_path + "archive"
pattern = "test-keyfile*.keys"

def find_files(pattern):
    files = glob.glob(input_dir + '/' + pattern)
    return files
    
def verify_keyfiles(files):
    verified_files = []
    for file in files:
        if os.path.isfile(file):
            verified_files.append(file)
    if not verified_files:
        print("No valid files found!")
    return verified_files

def rename_files(files, archive, src, dst, destination):
    print(files)
    for file in files:
        shutil.copyfile(file, archive + "/" + file.rsplit('/',1)[1])
        shutil.move(file, input_dir + "/" + file.rsplit('/',1)[1].replace(src, dst))

files = find_files(pattern)
verified_files = verify_keyfiles(files)
rename_files(verified_files, archive_dir, "test", "live", input_dir)
