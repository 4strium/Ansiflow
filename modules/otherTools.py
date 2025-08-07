import zipfile, os, json

def zip_folder(folder_path, zip_path):
  with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(folder_path):
      for file in files:
        file_path = os.path.join(root, file)
        arcname = os.path.relpath(file_path, folder_path)
        zipf.write(file_path, arcname)

def keep_visuals(str_lst_data):
  index = 0
  cut_index = len(str_lst_data)
  for line in str_lst_data :
    if "__VISUAL1__" in line :
      cut_index = index
    index += 1
  
  return str_lst_data[cut_index:]

def checkOS():
  if os.name == 'posix' :
    return "UNIX"
  elif os.name == 'nt' :
    return "Windows"
  else :
    return "Java"
  
def translation(key,language):
  with open("language/language_content.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)
  
  return json_data[key][language]