# See if it works on raspberry pi

import psutil
import subprocess

class SystemMonitor:
    def __init__(self):
        self.temp_files = [
            '/sys/class/thermal/thermal_zone0/temp',
            '/sys/class/thermal/thermal_zone1/temp',
            '/sys/class/thermal/thermal_zone2/temp'
        ]
    
    def get_cpu_usage(self):
        """Return the CPU usage percentage."""
        return psutil.cpu_percent(interval=1)
    
    def get_ram_usage(self):
        """Return the RAM usage in percentage and GB."""
        ram = psutil.virtual_memory()
        return ram.percent, ram.used / (1024 ** 3), ram.total / (1024 ** 3)
    
    def get_storage_details(self):
        """Return the storage details for all partitions."""
        partitions = psutil.disk_partitions()
        storage_info = []
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            storage_info.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': usage.total / (1024 ** 3),
                'used': usage.used / (1024 ** 3),
                'free': usage.free / (1024 ** 3),
                'percent': usage.percent
            })
        return storage_info
    
    def get_cpu_temperature(self):
        """Return the CPU temperature from different possible files."""
        for temp_file in self.temp_files:
            try:
                with open(temp_file, 'r') as f:
                    temp = int(f.read().strip()) / 1000.0
                return temp
            except Exception as e:
                print(f"Failed to read CPU temperature from {temp_file}: {e}")
        return None
    
    def get_wifi_status(self):
        """Check the status of the Wi-Fi connection."""
        try:
            result = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,SSID', 'dev', 'wifi'], capture_output=True, text=True)
            if result.returncode == 0:
                active_ssids = [line.split(':')[1] for line in result.stdout.splitlines() if line.startswith('yes')]
                return active_ssids if active_ssids else "No Wi-Fi connected"
            else:
                return "Error fetching Wi-Fi status"
        except Exception as e:
            return f"Failed to get Wi-Fi status: {e}"

    def get_bluetooth_status(self):
        """Check the status of Bluetooth."""
        try:
            result = subprocess.run(['bluetoothctl', 'show'], capture_output=True, text=True)
            if result.returncode == 0:
                status_lines = result.stdout.splitlines()
                for line in status_lines:
                    if line.startswith('Powered:'):
                        return line.split(':')[1].strip() == 'yes'
                return "Bluetooth status not found"
            else:
                return "Error fetching Bluetooth status"
        except Exception as e:
            return f"Failed to get Bluetooth status: {e}"

    def report(self):
        """Print the system report."""
        print("System Report:")
        print("---------------")
        
        print(f"CPU Usage: {self.get_cpu_usage()}%")
        
        ram_percent, ram_used, ram_total = self.get_ram_usage()
        print(f"RAM Usage: {ram_percent}% ({ram_used:.2f} GB used of {ram_total:.2f} GB total)")
        
        storage_details = self.get_storage_details()
        for storage in storage_details:
            print(f"Storage Device: {storage['device']}")
            print(f"  Mountpoint: {storage['mountpoint']}")
            print(f"  Filesystem: {storage['fstype']}")
            print(f"  Total: {storage['total']:.2f} GB")
            print(f"  Used: {storage['used']:.2f} GB")
            print(f"  Free: {storage['free']:.2f} GB")
            print(f"  Percent Used: {storage['percent']}%")
            print()
        
        cpu_temp = self.get_cpu_temperature()
        if cpu_temp is not None:
            print(f"CPU Temperature: {cpu_temp:.2f} °C")
        else:
            print("CPU Temperature: Not available")

        print(f"Wi-Fi Status: {self.get_wifi_status()}")
        print(f"Bluetooth Status: {'On' if self.get_bluetooth_status() else 'Off'}")

# Example usage
if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.report()
