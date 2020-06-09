#MEHMET KIVANÇ ERBUDAK - 170709062 - Computer Engineering
import os
import time
import requests
from multiprocessing import Pool
import hashlib
import uuid

web_links = ["http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg", "https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg", "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]

def create_parent_child(): 
    n = os.fork() 
    # n greater than 0  means parent process 
    if n > 0: 
        os.waitpid(pid, 0) #Avoid Orphans
        print("Parent process and id is : ", os.getpid()) 
    # n equals to 0 means child process 
    else: 
        print("Child process and id is : ", os.getpid())

def download_file(web_links, file_name=None):
	r = requests.get(web_links, allow_redirects=True)
	file = file_name if file_name else str(uuid.uuid4())
	open(file, 'wb').write(r.content)

def download_file2():
    print("{} files downloading...\n".format(len(web_links)))
    for i in range(len(web_links)):
		download_file(web_links[i], "file{}".format(i))
		print("file{0} downloaded from\n{1}\n".format(i, web_links[i]))

def unique(liste): 
    ulist = [] 
    for x in liste: 
        if x == None:
            liste.remove(None)
        elif x not in ulist: 
            ulist.append(x)
    return ulist

def md5(file_name):
    do_md5 = hashlib.md5()
    with open(file_name, "rb") as file1:
        for chunk in iter(lambda: file1.read(4096), b""):
            do_md5.update(chunk)
    return do_md5.hexdigest()

def check_duplicate(element, list_md5):
	dupcount = 0
	indexes = []
	for i in range(len(list_md5)):
		if list_md5[i] == element:
			dupcount += 1
			indexes.append(i)
	if dupcount > 1:
		return indexes

def check_duplicate2():
	files_n = os.listdir() 
	files_n.remove("ceng_2034_final_answer.py")
	list_md5 = []
	print("Checking checksum md5 values...\n")
	start_duplicate_time = time.time()
	with Pool(5) as p:
		list_md5 = p.map(md5,files_n)
	print("Checking duplicate values...\n")
	with Pool(5) as p:
		list_duplicate = p.starmap(check_duplicate,([list_md5[0],
		list_md5],[list_md5[1], list_md5], 
		[list_md5[2], list_md5], [list_md5[3],
		list_md5], [list_md5[4], list_md5]))
	list_duplicates = list(list_duplicate)
	print("Last fixes...\n")
	unique_duplicates = unique(list_duplicates)
	for j in range(len(unique_duplicates)):
		print("{0} and {1} duplicate files.".format(files_n[unique_duplicates[j][0]],
		files_n[unique_duplicates[j][1]]))
		end_duplicate_time = time.time()
		subtract_duplicate_time = end_duplicate_time - start_duplicate_time
		print("\nTotal execution time to check duplicate = {}".format(subtract_duplicate_time))
        
def clear_orphans(): 
  process= subprocess.Popen( ('ls', '-l', '/tmp'), stdout=subprocess.PIPE)
  for line in process.stdout:
        pass
    
  subprocess.call( ('ps', '-l') )
  process.wait()
  print("\n")
  print( "Clearing...\n")
  print("------------------------------------------------------------")
  subprocess.call( ('ps', '-l') )



os.system("clear")
print("\n Hi user, welcome to script. | created by Mehmet Kıvanç ERBUDAK - 170709062 \n")
print("General Information")
print("------------------------------------------------------------")
print("Operating System Type: ", os.name, "\n")
print("Your destination: ", os.getcwd(), "\n")
print("CPU (Core) Count: ", str(os.cpu_count()), "\n")
print("------------------------------------------------------------")
print("\n Please enter the command number to execute the script: \n"
      " 1 : Create a New Parent and Child Process and Print Process ID (PID). \n"
      " 2 : Create a New Parent and Child Process, Download the Files With Child Process. \n"
      " 3 : Clean Out the Orphans. \n"
      " 4 : Control Duplicate Files Within the Downloaded Files. \n"
      " 0 : Exit the script.\n")
print("------------------------------------------------------------\n")

while(True):
  command = input("Please enter the command number: ")
  if(command==None or command=="" or command==" "):
    print("Unvalid command number was sended.")
  elif(command=="1"):
    create_parent_child()
  elif(command=="2"):
    n2 = os.fork() 
    if n2 > 0: 
        os.waitpid(pid, 0) #Avoid Orphans
        print("")
    else: 
        download_file2()
  elif(command=="3"):
    clear_orphans()
  elif(command=="4"):
    check_duplicate2()
  elif(command=="0"):
    print("Exiting from the script.")
    
    # Chechking all sources in the end
    src_folder = "../../"


    def generate_md5(fname, chunk_size=1024):
        hash = hashlib.md5()
        with open(fname, "rb") as f:
            chunk = f.read(chunk_size)
            while chunk:
                hash.update(chunk)
                chunk = f.read(chunk_size)

        return hash.hexdigest()


    if __name__ == "__main__":
    md5_dict = defaultdict(list)
    file_types_inscope = ["jpg", "png"]
    for path, dirs, files in os.walk(src_folder):
        print("Analyzing {}".format(path))
        for each_file in files:
            if each_file.split(".")[-1].lower() in file_types_inscope:
                file_path = os.path.join(os.path.abspath(path), each_file)
                md5_dict[generate_md5(file_path)].append(file_path)

    duplicate_files = (
        val for key, val in md5_dict.items() if len(val) > 1)

    # Write the list of duplicate files to csv file
    with open("duplicates.csv", "w") as log:
        csv_writer = csv.writer(log, quoting=csv.QUOTE_MINIMAL, delimiter=",",
                                lineterminator="\n")
        header = ["File Names"]
        csv_writer.writerow(header)

        for file_name in duplicate_files:
            csv_writer.writerow(file_name)

    print("Checked all folders.")
    
    sys.exit()