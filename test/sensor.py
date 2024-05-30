import wmi
import psutil

# 初始化 WMI 对象
w = wmi.WMI(namespace="root\OpenHardwareMonitor")

# 获取温度传感器
temperature_sensors = w.Sensor()

# 遍历温度传感器
for sensor in temperature_sensors:
    if sensor.SensorType == u'Temperature':
        print(f"{sensor.Name}: {sensor.Value} °C")

# 获取其他系统信息（例如 CPU 使用率）
cpu_usage = psutil.cpu_percent(interval=1)
print(f"CPU 使用率：{cpu_usage}%")
