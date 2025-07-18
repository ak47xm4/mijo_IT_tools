#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
讀取nwinfo.json 的 檔案
mijo 會在 進行後續作業，先把 大概的 json code 範本 寫給我，我再進行 修改
要用cli執行，要有 argument
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    載入 JSON 檔案
    
    Args:
        file_path: JSON 檔案路徑
        
    Returns:
        Dict: 解析後的 JSON 資料
        
    Raises:
        FileNotFoundError: 檔案不存在
        json.JSONDecodeError: JSON 格式錯誤
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"錯誤: 找不到檔案 '{file_path}'")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"錯誤: JSON 格式錯誤 - {e}")
        sys.exit(1)


def extract_system_info(data: Dict[str, Any]) -> Dict[str, Any]:
    """提取系統資訊"""
    system_info = {}

    # 基本系統資訊
    if "System" in data:
        system = data["System"]
        system_info["os"] = system.get("OS", "Unknown")
        system_info["computer_name"] = system.get("Computer Name", "Unknown")
        system_info["username"] = system.get("Username", "Unknown")
        system_info["uptime"] = system.get("Uptime", "Unknown")

        # 記憶體資訊
        if "Physical Memory" in system:
            memory = system["Physical Memory"]
            system_info["memory_total"] = memory.get("Total", "Unknown")
            system_info["memory_free"] = memory.get("Free", "Unknown")

    return system_info


def extract_cpu_info(data: Dict[str, Any]) -> Dict[str, Any]:
    """提取 CPU 資訊"""
    cpu_info = {}

    if "CPUID" in data:
        cpuid = data["CPUID"]
        cpu_info["total_cpus"] = cpuid.get("Total CPUs", 0)
        cpu_info["processor_count"] = cpuid.get("Processor Count", 0)
        cpu_info["cpu_clock"] = cpuid.get("CPU Clock (MHz)", 0)

        # CPU0 詳細資訊
        if "CPU0" in cpuid:
            cpu0 = cpuid["CPU0"]
            cpu_info["vendor"] = cpu0.get("Vendor", "Unknown")
            cpu_info["brand"] = cpu0.get("Brand", "Unknown").strip()
            cpu_info["cores"] = cpu0.get("Cores", 0)
            cpu_info["logical_cpus"] = cpu0.get("Logical CPUs", 0)
            cpu_info["temperature"] = cpu0.get("Temperature (C)", 0)

    return cpu_info


def extract_disk_info(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """提取磁碟資訊"""
    disks = []

    if "Disks" in data:
        for disk in data["Disks"]:
            disk_info = {
                "path": disk.get("Path", ""),
                "hw_name": disk.get("HW Name", ""),
                "size": disk.get("Size", ""),
                "type": disk.get("Type", ""),
                "ssd": disk.get("SSD", False),
                "temperature": disk.get("Temperature (C)", 0),
                "health_status": disk.get("Health Status", ""),
                "serial_number": disk.get("Serial Number", ""),
                "volumes": []
            }

            # 提取磁碟區資訊
            if "Volumes" in disk:
                for volume in disk["Volumes"]:
                    volume_info = {
                        "path": volume.get("Path", ""),
                        "label": volume.get("Label", ""),
                        "filesystem": volume.get("Filesystem", ""),
                        "free_space": volume.get("Free Space", ""),
                        "total_space": volume.get("Total Space", ""),
                        "usage": volume.get("Usage", ""),
                        "drive_letters": []
                    }

                    # 提取磁碟機代號
                    if "Volume Path Names" in volume:
                        for path_name in volume["Volume Path Names"]:
                            if "Drive Letter" in path_name:
                                volume_info["drive_letters"].append(
                                    path_name["Drive Letter"])

                    disk_info["volumes"].append(volume_info)

            disks.append(disk_info)

    return disks


def extract_gpu_info(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """提取 GPU 資訊"""
    gpus = []

    if "GPU" in data:
        for gpu in data["GPU"]:
            gpu_info = {
                "device": gpu.get("Device", ""),
                "vendor": gpu.get("Vendor", ""),
                "memory_size": gpu.get("Memory Size", ""),
                "driver_version": gpu.get("Driver Version", ""),
                "location": gpu.get("Location", "")
            }
            gpus.append(gpu_info)

    return gpus


def extract_network_info(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """提取網路介面資訊"""
    networks = []

    if "Network" in data:
        for network in data["Network"]:
            network_info = {
                "description": network.get("Description", ""),
                "type": network.get("Type", ""),
                "status": network.get("Status", ""),
                "mac_address": network.get("MAC Address", ""),
                "ip_addresses": []
            }

            # 提取 IP 位址
            if "Unicasts" in network:
                for unicast in network["Unicasts"]:
                    if "IPv4" in unicast:
                        network_info["ip_addresses"].append({
                            "type":
                            "IPv4",
                            "address":
                            unicast["IPv4"],
                            "subnet":
                            unicast.get("Subnet Mask", "")
                        })
                    elif "IPv6" in unicast:
                        network_info["ip_addresses"].append({
                            "type":
                            "IPv6",
                            "address":
                            unicast["IPv6"]
                        })

            networks.append(network_info)

    return networks


def extract_usb_info(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """提取 USB 裝置資訊"""
    usb_devices = []

    if "USB" in data:
        for usb in data["USB"]:
            usb_info = {
                "hwid": usb.get("HWID", ""),
                "vendor_id": usb.get("Vendor ID", ""),
                "device_id": usb.get("Device ID", ""),
                "vendor": usb.get("Vendor", ""),
                "name": usb.get("Name", "")
            }
            usb_devices.append(usb_info)

    return usb_devices


def print_summary(data: Dict[str, Any]):
    """印出系統摘要"""
    print("=== 系統硬體摘要 ===")

    # 系統資訊
    system_info = extract_system_info(data)
    print(f"作業系統: {system_info.get('os', 'Unknown')}")
    print(f"電腦名稱: {system_info.get('computer_name', 'Unknown')}")
    print(f"使用者: {system_info.get('username', 'Unknown')}")
    print(f"運行時間: {system_info.get('uptime', 'Unknown')}")
    print(
        f"記憶體: {system_info.get('memory_free', 'Unknown')} / {system_info.get('memory_total', 'Unknown')}"
    )

    # CPU 資訊
    cpu_info = extract_cpu_info(data)
    print(f"CPU: {cpu_info.get('brand', 'Unknown')}")
    print(f"核心數: {cpu_info.get('cores', 0)}")
    print(f"邏輯處理器: {cpu_info.get('logical_cpus', 0)}")
    print(f"溫度: {cpu_info.get('temperature', 0)}°C")

    # 磁碟資訊
    disks = extract_disk_info(data)
    print(f"磁碟數量: {len(disks)}")
    for i, disk in enumerate(disks):
        print(
            f"  磁碟 {i+1}: {disk['hw_name']} ({disk['size']}) - {disk['health_status']}"
        )

    # GPU 資訊
    gpus = extract_gpu_info(data)
    print(f"GPU 數量: {len(gpus)}")
    for gpu in gpus:
        print(f"  GPU: {gpu['device']} ({gpu['memory_size']})")

    # 網路介面
    networks = extract_network_info(data)
    active_networks = [n for n in networks if n['status'] == 'Active']
    print(f"網路介面: {len(active_networks)} 個啟用")

    # USB 裝置
    usb_devices = extract_usb_info(data)
    print(f"USB 裝置: {len(usb_devices)} 個")


def main():
    """主程式"""
    parser = argparse.ArgumentParser(description='讀取 nwinfo JSON 報告檔案')
    parser.add_argument('json_file', help='JSON 檔案路徑')
    parser.add_argument('--summary', action='store_true', help='顯示系統摘要')
    parser.add_argument('--cpu', action='store_true', help='顯示 CPU 詳細資訊')
    parser.add_argument('--disks', action='store_true', help='顯示磁碟詳細資訊')
    parser.add_argument('--gpu', action='store_true', help='顯示 GPU 詳細資訊')
    parser.add_argument('--network', action='store_true', help='顯示網路詳細資訊')
    parser.add_argument('--usb', action='store_true', help='顯示 USB 詳細資訊')
    parser.add_argument('--all', action='store_true', help='顯示所有詳細資訊')

    args = parser.parse_args()

    # 檢查檔案是否存在
    if not Path(args.json_file).exists():
        print(f"錯誤: 檔案 '{args.json_file}' 不存在")
        sys.exit(1)

    # 載入 JSON 資料
    print(f"正在載入 JSON 檔案: {args.json_file}")
    data = load_json_file(args.json_file)
    print("JSON 檔案載入成功!")

    # 根據參數顯示不同資訊
    if args.summary or not any(
        [args.cpu, args.disks, args.gpu, args.network, args.usb, args.all]):
        print_summary(data)

    if args.all or args.cpu:
        print("\n=== CPU 詳細資訊 ===")
        cpu_info = extract_cpu_info(data)
        print(json.dumps(cpu_info, indent=2, ensure_ascii=False))

    if args.all or args.disks:
        print("\n=== 磁碟詳細資訊 ===")
        disks = extract_disk_info(data)
        print(json.dumps(disks, indent=2, ensure_ascii=False))

    if args.all or args.gpu:
        print("\n=== GPU 詳細資訊 ===")
        gpus = extract_gpu_info(data)
        print(json.dumps(gpus, indent=2, ensure_ascii=False))

    if args.all or args.network:
        print("\n=== 網路詳細資訊 ===")
        networks = extract_network_info(data)
        print(json.dumps(networks, indent=2, ensure_ascii=False))

    if args.all or args.usb:
        print("\n=== USB 詳細資訊 ===")
        usb_devices = extract_usb_info(data)
        print(json.dumps(usb_devices, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
