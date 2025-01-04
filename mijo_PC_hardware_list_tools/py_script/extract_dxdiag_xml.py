from dataclasses import dataclass
from typing import List, Dict
import xml.etree.ElementTree as ET
from pathlib import Path
import json


@dataclass
class SystemInfo:
    os_version: str
    processor: str
    memory: str
    directx_version: str


@dataclass
class DisplayDevice:
    card_name: str
    manufacturer: str
    chip_type: str
    display_memory: str


class DxDiagParser:

    def __init__(self, xml_path: Path):
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()

    def parse_system_info(self) -> SystemInfo:
        """解析系统信息"""
        sys_info = self.root.find("SystemInformation")
        if sys_info is None:
            return None

        return SystemInfo(os_version=sys_info.findtext("OperatingSystem", ""),
                          processor=sys_info.findtext("Processor", ""),
                          memory=sys_info.findtext("Memory", ""),
                          directx_version=sys_info.findtext(
                              "DirectXVersion", ""))

    def parse_display_devices(self) -> List[DisplayDevice]:
        """解析显示设备信息"""
        devices = []
        display_devices = self.root.find("DisplayDevices")

        if display_devices is not None:
            for device in display_devices.findall("DisplayDevice"):
                devices.append(
                    DisplayDevice(
                        card_name=device.findtext("CardName", ""),
                        manufacturer=device.findtext("Manufacturer", ""),
                        chip_type=device.findtext("ChipType", ""),
                        display_memory=device.findtext("DisplayMemory", "")))

        return devices

    def generate_report(self, output_format: str = "json") -> None:
        """生成报告"""
        data = {
            "system_info": self.parse_system_info(),
            "display_devices": self.parse_display_devices()
        }

        if output_format == "json":
            return json.dumps(data, default=lambda x: x.__dict__, indent=2)
        # 可以添加其他格式的支持


def main():
    parser = DxDiagParser(Path("test_data/dxdiag.xml"))
    report = parser.generate_report()

    # 保存报告
    output_path = Path("output/dxdiag_report.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding='utf-8')


if __name__ == "__main__":
    main()
