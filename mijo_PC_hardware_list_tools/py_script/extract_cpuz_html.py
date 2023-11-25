
import os
import re

import csv

print('START~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

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

def txt_to_string(txt_file):
    # with open(txt_file , 'r' , encoding='utf-8' ) as file:
    
    # with open(txt_file , 'r' , encoding='cp1252' ) as file:
    
    # for cpuz htm
    with open(txt_file , 'r' , encoding='latin-1' ) as file:
        aaa = file.read()
            
        return aaa


# 使用遞迴函式來檢查資料夾結構
# def find_Diskinfo_files(folder_path):
def find_cpuz_files(folder_path):
    # 建立一個空的列表來存儲找到的檔案路徑
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # print(file)
            if file == "cpuz.htm":
                file_paths.append(os.path.join(root, file))
    return file_paths


# def extract_disk_info_txt(file):
def extract_cpuz_txt_monitors(file,monitor_number):
    aaa = file_s_full_path(file)
    # txt_lines = txt_to_lines(aaa)
    # print(aaa)
    txt = txt_to_string(aaa)
    
    # print(txt)
    
    # nnn = file_s_folder_name(aaa)
    
    # data = extract_disk_info(txt_lines,nnn)
    data = extract_monitor_details(txt,monitor_number)
    
    return data
    
    

def extract_monitor_details(text, monitor_number):
    # Regex pattern to find the details of a specific monitor
    pattern = f"Monitor {monitor_number}.*?Max Resolution.*?</font></small></td></tr>"
    monitor_info = re.search(pattern, text, re.DOTALL)

    if monitor_info:
        monitor_info = monitor_info.group(0)
        details = re.findall(r"<small>&nbsp;&nbsp;&nbsp;&nbsp;\t(.*?)</small></td><td valign=\"center\"><small><font color=\"#0000A0\">(.*?)</font>", monitor_info)
        return {detail[0]: detail[1] for detail in details}
    else:
        return {}

# Extracting details for Monitor 0, Monitor 1, and Monitor 2
# monitor_0_info = extract_monitor_details(file_contents, 0)
# monitor_1_info = extract_monitor_details(file_contents, 1)
# monitor_2_info = extract_monitor_details(file_contents, 2)


# 正式 code


disk_info_files = find_cpuz_files(folder_path)

# print(disk_info_files)

all_fucking_data = []

for di in disk_info_files:
    nnn = file_s_folder_name(di)
    di_full_path = file_s_full_path(di)
    # print(aaa)
    # print(di_full_path)
    
    for i in range(0,6):
        try:
            data = extract_cpuz_txt_monitors(di_full_path,i)
            
            if data != {}:
                # print(data)
        
                # for o in data:
                
                data['PC_name']=nnn
                
                all_fucking_data.append(data)
        except:
            # print('fuck')
            pass
    
# print(all_fucking_data)
    
    

# for i in all_fucking_data:
    # print(i)



# 設定 CSV 文件的標頭（列名稱）
fields = ['PC_name','Model','ID', 'Serial','Manufacturing Date','Size','Max Resolution']

# 指定要寫入的 CSV 文件名稱
filename = 'Monitor_data.csv'

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
