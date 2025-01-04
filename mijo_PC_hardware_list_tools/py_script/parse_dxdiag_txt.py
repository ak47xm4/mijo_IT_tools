from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path


@dataclass
class SystemInfo:
    machine_name: str
    operating_system: str
    language: str
    processor: str
    memory: str
    time_of_this_report: str


@dataclass
class DisplayDevice:
    card_name: str
    manufacturer: str
    chip_type: str
    display_memory: str
    dedicated_memory: str
    current_mode: str
    hdr_support: str
    monitor_name: str
    monitor_model: str


@dataclass
class SoundDevice:
    description: str
    default_sound_playback: str
    default_voice_playback: str
    hardware_id: str
    manufacturer_id: str
    product_id: str
    type: str
    driver_name: str
    driver_version: str
    driver_attributes: str
    whql_logo: str
    date_and_size: str
    other_files: str
    driver_provider: str
    hw_accel_level: str
    min_max_sample_rate: str
    static_strm_hw_mix_bufs: str


@dataclass
class VideoCaptureDevice:
    friendly_name: str
    category: str
    symbolic_link: str
    location: str
    rotation: str
    manufacturer: str
    hardware_id: str
    driver_desc: str
    driver_provider: str
    driver_version: str
    driver_date_english: str


@dataclass
class DirectInputDevices:
    device_name: str


class DxDiagParser:

    def __init__(self, txt_path: Path):
        # 尝试多种编码
        encodings = ['utf-8', 'big5', 'gbk', 'cp950', 'cp936']

        for encoding in encodings:
            try:
                self.content = txt_path.read_text(encoding=encoding)
                print(f"成功使用 {encoding} 编码读取文件")
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"读取文件时发生错误: {e}")
                raise
        else:
            raise UnicodeDecodeError("无法使用已知编码读取文件")

        self.sections = self._split_sections()

    def _split_sections(self) -> Dict[str, str]:
        """将文本分割成不同的段落"""
        sections = {}
        current_section = ""
        current_content = []

        for line in self.content.split('\n'):
            # 检测新的段落标题
            if line.startswith('---'):
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_content = []
                # 获取下一行作为段落标题
                continue
            elif line.strip() and all(c == '-' for c in line.strip()):
                continue
            elif line.strip():
                if not current_content and not line.startswith(' '):
                    current_section = line.strip()
                else:
                    current_content.append(line)

        # 添加最后一个段落
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content)

        return sections

    def parse_system_info(self) -> Optional[SystemInfo]:
        """解析系统信息部分"""
        section = self.sections.get('System Information', '')
        if not section:
            return None

        # 创建一个字典来存储找到的值
        info = {}

        # 创建字段名映射关系 - 确保与类定义中的字段名完全匹配(小写+下划线)
        field_mapping = {
            'machine_name': 'Machine Name',
            'operating_system': 'Operating System',
            'language': 'Language',
            'processor': 'Processor',
            'memory': 'Memory',
            'time_of_this_report': 'Time of this report'
        }

        # 遍历SystemInfo类的所有字段
        for field_name in SystemInfo.__annotations__:
            # 使用映射获取对应的搜索关键字
            search_key = field_mapping.get(field_name)
            if not search_key:
                # print(f"警告: 字段 {field_name} 没有对应的映射关键字")
                continue

            # 在section中查找对应的行
            for line in section.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    if search_key in key:
                        info[field_name] = value.strip()
                        # print(f"找到 {search_key} 的值: {value.strip()}")
                        break

            # 如果没找到对应的值,设为空字符串
            if field_name not in info:
                # print(f"未找到 {search_key} 的值")
                info[field_name] = ''

        try:
            return SystemInfo(**info)
        except Exception as e:
            # print(f"创建SystemInfo对象时发生错误: {e}")
            # print(f"当前收集的信息: {info}")
            return SystemInfo(**info)  # 即使有错误也尝试创建对象

    def parse_display_devices(self) -> List[DisplayDevice]:
        """解析显示设备信息"""
        section = self.sections.get('Display Devices', '')
        if not section:
            return []

        devices = []
        current_device = {}

        for line in section.split('\n'):
            line = line.strip()
            if line.startswith('Card name:'):
                if current_device:
                    try:
                        devices.append(DisplayDevice(**current_device))
                    except TypeError as e:
                        print(f"无法创建显示设备对象: {e}")
                        print(f"当前设备数据: {current_device}")
                current_device = {}

            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                if key in DisplayDevice.__annotations__:
                    current_device[key] = value

        if current_device:
            try:
                devices.append(DisplayDevice(**current_device))
            except TypeError as e:
                print(f"无法创建最后一个显示设备对象: {e}")
                print(f"设备数据: {current_device}")

        return devices

    def parse_sound_devices(self) -> List[SoundDevice]:
        """解析声音设备信息"""
        section = self.sections.get('Sound Devices', '')
        if not section:
            return []

        devices = []
        current_device = {}

        for line in section.split('\n'):
            line = line.strip()
            if line.startswith('Description:'):
                if current_device:
                    try:
                        devices.append(SoundDevice(**current_device))
                    except TypeError as e:
                        print(f"无法创建声音设备对象: {e}")
                current_device = {}

            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                if key in SoundDevice.__annotations__:
                    current_device[key] = value

        if current_device:
            try:
                devices.append(SoundDevice(**current_device))
            except TypeError as e:
                print(f"无法创建最后一个声音设备对象: {e}")

        return devices

    def parse_video_capture_devices(self) -> List[VideoCaptureDevice]:
        """解析视频捕获设备信息"""
        section = self.sections.get('Video Capture Devices', '')
        if not section:
            return []

        devices = []
        current_device = {}

        for line in section.split('\n'):
            line = line.strip()
            if line.startswith('FriendlyName:'):
                if current_device:
                    try:
                        devices.append(VideoCaptureDevice(**current_device))
                    except TypeError as e:
                        print(f"无法创建视频捕获设备对象: {e}")
                current_device = {}

            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                if key in VideoCaptureDevice.__annotations__:
                    current_device[key] = value

        if current_device:
            try:
                devices.append(VideoCaptureDevice(**current_device))
            except TypeError as e:
                print(f"无法创建最后一个视频捕获设备对象: {e}")

        return devices

    def parse_direct_input_devices(self) -> List[DirectInputDevices]:
        """解析DirectInput设备信息"""
        section = self.sections.get('DirectInput Devices', '')
        if not section:
            return []

        devices = []
        current_device = {}

        for line in section.split('\n'):
            line = line.strip()
            if line.startswith('Device Name:'):  # 找到设备名称行
                if current_device:  # 如果已有设备信息，保存它
                    try:
                        devices.append(
                            DirectInputDevices(device_name=current_device.get(
                                'device_name', '')))
                    except TypeError as e:
                        print(f"无法创建DirectInput设备对象: {e}")
                current_device = {'device_name': line.split(':', 1)[1].strip()}

        # 添加最后一个设备
        if current_device:
            try:
                devices.append(
                    DirectInputDevices(
                        device_name=current_device.get('device_name', '')))
            except TypeError as e:
                print(f"无法创建最后一个DirectInput设备对象: {e}")

        return devices

    def generate_report(self, output_format: str = "json") -> Dict:
        """生成完整报告"""
        try:
            return {
                "system_info": self.parse_system_info(),
                "display_devices": self.parse_display_devices(),
                "direct_input_devices": self.parse_direct_input_devices(),
                # 以下是不要解析的
                # "sound_devices": self.parse_sound_devices(),
                # "video_capture_devices": self.parse_video_capture_devices()
                # 以上是不要解析的
            }
        except Exception as e:
            print(f"生成报告时发生错误: {e}")
            return {}


def main():
    try:
        parser = DxDiagParser(Path("test_data/dxdiag.txt"))
        report = parser.generate_report()

        if not report:
            print("未能生成报告")
            return

        # 保存为JSON
        output_path = Path("output/dxdiag_report.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=lambda x: x.__dict__)

        print(f"报告已保存到: {output_path}")

    except Exception as e:
        print(f"程序执行出错: {e}")


if __name__ == "__main__":
    main()
