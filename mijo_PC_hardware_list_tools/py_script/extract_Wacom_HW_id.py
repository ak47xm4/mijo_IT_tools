
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
    with open(txt_file , 'r' , encoding='utf-16' ) as file:
        lines = file.readlines()
        
        return lines

def txt_to_string(txt_file):
    # with open(txt_file , 'r' , encoding='utf-8' ) as file:
    '''
    try:
        with open(txt_file , 'r' , encoding='cp1252' ) as file:
            aaa = file.read()
            
            return aaa
    except:
        with open(txt_file , 'r' , encoding='utf-8' ) as file:
            aaa = file.read()
        
            return aaa
    '''
    
    # with open(txt_file , 'r' , encoding='cp1252' ) as file:
    
    # for cpuz htm
    # with open(txt_file , 'r' , encoding='latin-1' ) as file:
    with open(txt_file , 'r' , encoding='utf-16' ) as file:
        aaa = file.read()
            
        return aaa


# 使用遞迴函式來檢查資料夾結構
# def find_Diskinfo_files(folder_path):
def find_USB_HW_id_files(folder_path):
    # 建立一個空的列表來存儲找到的檔案路徑
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # print(file)
            if file == "USB_HW_id.txt":
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

# from WH draft_exr2mov
def csv_2_dict(csv_file):
    csv_file = csv_file.replace('\\','/')
    
    lll = []
    
    with open( csv_file , encoding='utf-8') as f:
        
        lll = list(csv.reader(f,delimiter=','))
        
        # print(lll)
        
    return lll
    
# from WH draft_exr2mov
def get_csv_2_dict_shot_id(list_of_dict,shot_code):
    # print(shot_code)
    
    for i in list_of_dict:
        # print('list_of_dict: ',i[3])
        # print(i[2])
        if i[2].zfill(4) == shot_code:
            shot_id = i[3]
            # print('shot_id: ',shot_id)
            return str(shot_id)
            break
            
    pass
    # 處理 沒又找到的例外
    pass


# 正式 code

disk_info_files = find_USB_HW_id_files(folder_path)

# print(disk_info_files)

all_fucking_data = []


# csv lookup
# you can sort yourself
# but, I put it in HW_id
wacom_csv = csv_2_dict(r'wacom_HW_id_20231115_A.csv')


# di is diskinfo. you can rename
for di in disk_info_files:
    nnn = file_s_folder_name(di)
    di_full_path = file_s_full_path(di)
    # print(aaa)
    # print(di_full_path)
    
    # data = extract_cpuz_txt_monitors(di_full_path,i)
    data = {}
    
    lines = txt_to_lines(di_full_path) 
    
    vid_line = ''
    
    for line in lines:
        if "VID_056A" in line:
            vid_line = line
            break
        
    # Regular expression to find the PID code
    pid_match = re.search(r'PID_([0-9A-F]+)', line)

    # Extracting the PID code
    pid_code = pid_match.group(1) if pid_match else None
    
    data['PC_name']=nnn
    data['wacom_HW_id']=pid_code
    
    try:
        wacom_model_name = get_csv_2_dict_shot_id(wacom_csv,pid_code)
    except:
        wacom_model_name = 'undefined'
    data['wacom_model']=wacom_model_name
    
    all_fucking_data.append(data)

    
# print(all_fucking_data)
    
    

# for i in all_fucking_data:
    # print(i)



# 設定 CSV 文件的標頭（列名稱）
fields = ['PC_name','wacom_HW_id','wacom_model']

# 指定要寫入的 CSV 文件名稱
filename = 'aaa.csv'

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
