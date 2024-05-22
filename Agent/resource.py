import psutil

def requireCpuInfo():
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent()
    cpu_times = psutil.cpu_times()
    cpu_freq = psutil.cpu_freq()
    cpu_stats = psutil.cpu_stats()

    data = {
        "cpu_count": cpu_count,
        "cpu_percent": cpu_percent,
        "cpu_times": cpu_times,
        "cpu_freq": cpu_freq,
        "cpu_stats": cpu_stats,
    }

    return data

def requireMemInfo():
    virtual_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()

    data = {
        "virtual_mem": virtual_mem,
        "swap_mem": swap_mem,
    }

    return data

def requireDiskInfo():
    disk_partions = psutil.disk_partitions(all=False)
    disk_usage = psutil.disk_usage("/")
    disk_io_counters = psutil.disk_io_counters(perdisk=False, nowrap=True)

    data = {
        "disk_partions": disk_partions,
        "disk_usage": disk_usage,
        "disk_io_counters": disk_io_counters,
    }

    return data

def requireSensorInfo():
    sensors_battery = psutil.sensors_battery()
    data = {
        "sensors_battery": sensors_battery,
    }

    return data