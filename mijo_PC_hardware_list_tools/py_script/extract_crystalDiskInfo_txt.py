
import os
import re

import csv


# 指定放置檔案的單層資料夾路徑
folder_path = 'folder_path'  # 將此路徑替換為你的資料夾路徑


def file_s_folder_name(file):
    file_path = os.path.join(folder_path, file)
    
    # 檢查檔案是否存在
    if os.path.isfile(file_path):
        # print(file_path)
        
        sss = file_path.split('\\')
        
        return sss[-2]
        
def file_s_full_path(file):
    file_path = os.path.join(folder_path, file)
    
    # 檢查檔案是否存在
    if os.path.isfile(file_path):
        # print(file_path)
        return file_path
        
def txt_to_lines(txt_file):
    with open(txt_file , 'r' , encoding='utf-8' ) as file:
        lines = file.readlines()
        
        return lines



# 使用遞迴函式來檢查資料夾結構
def find_Diskinfo_files(folder_path):
    # 建立一個空的列表來存儲找到的檔案路徑
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # print(file)
            if file == "DiskInfo.txt":
                file_paths.append(os.path.join(root, file))
    return file_paths


def extract_disk_info_txt(file):
    aaa = file_s_full_path(file)
    txt_lines = txt_to_lines(aaa)
    
    nnn = file_s_folder_name(aaa)
    
    data = extract_disk_info(txt_lines,nnn)
    
    return data
    

# Function to extract relevant information (Model, Disk Size, Health Status) from the text data
def extract_disk_info(lines, computer_name):
    
    scan_Date = ""
    for line in lines:
        if "Date" in line:
            scan_Date = line.split(":")[1].strip()
            scan_Date +=':'
            scan_Date += line.split(":")[2].strip()
    
    
    disk_data = []
    current_disk = {}
    
    for line in lines:
        current_disk['scan_Date'] = scan_Date
        current_disk['PC_name'] = computer_name
        
        if "Model" in line:
            current_disk['Model'] = line.split(":")[1].strip()
        elif "Serial Number" in line:
            current_disk['SN'] = line.split(":")[1].strip()
        elif "Disk Size" in line:
            current_disk['Disk Size'] = line.split(":")[1].strip()
        elif "Interface" in line:
            current_disk['Interface'] = line.split(":")[1].strip()
        elif "Transfer Mode" in line:
            current_disk['TM'] = line.split(":")[1].strip()
        elif "Health Status" in line:
            # Extracting the percentage value from the Health Status line
            health_status_match = re.search(r'\d+\s%', line)
            if health_status_match:
                aaa = ''
                aaa = health_status_match.group()
                aaa = str(aaa)
                aaa = aaa.replace('%','')
                aaa = aaa.replace(' ','')
                # aaa = int(aaa)
                # print(aaa)
                aaa_3padzero = aaa.zfill(3)
                # print(aaa_3padzero)
                
                current_disk['Health Status'] = aaa_3padzero
            else:
                current_disk['Health Status'] = 'Unknown'
        elif "Drive Letter" in line:
            sss = line.split(":")
            aaa = ''
            for i in range(1,len(sss)):
                aaa += sss[i].strip()
                # aaa +=': '
            
            current_disk['Drive Letter'] = aaa

            
            # Append the current disk data to the list and reset the current disk dictionary
            disk_data.append(current_disk)
            current_disk = {}
            
    return disk_data


# 正式 code


disk_info_files = find_Diskinfo_files(folder_path)

# print(disk_info_files)

all_fucking_data = []

for di in disk_info_files:
    nnn = file_s_folder_name(di)
    di_full_path = file_s_full_path(di)
    # print(aaa)
    # print(di_full_path)
    
    data = extract_disk_info_txt(di_full_path)
    
    # print(data)
    
    for i in data:
        all_fucking_data.append(i)
    
    
# print(all_fucking_data)
    
    

# 設定 CSV 文件的標頭（列名稱）
fields = ['PC_name','scan_Date','Model', 'Disk Size' , 'Drive Letter' , 'Interface' ,'TM', 'SN' , 'Health Status']

# 指定要寫入的 CSV 文件名稱
filename = 'SSD_data.csv'

# 開啟 CSV 文件並寫入資料
with open(filename, 'w', newline='') as csvfile:
    # 創建 CSV 寫入器
    csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
    
    # 寫入標頭
    csvwriter.writeheader()
    
    # 寫入資料
    for row in all_fucking_data:
        csvwriter.writerow(row)

# print(f'已將字典轉換為 CSV 文件：{filename}')



print('OK~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
