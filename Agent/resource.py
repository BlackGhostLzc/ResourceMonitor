import psutil

def requireCpuInfo():
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(percpu=True, interval=1)
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


def get_top_cpu_processes(n=5, interval=1):
    # 获取所有进程的列表
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # 初次调用cpu_percent以初始化
    for proc in processes:
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # 等待一段时间再获取CPU使用率
    # time.sleep(interval)

    # 获取CPU使用率
    processes_with_cpu = []
    for proc in processes:
        try:
            cpu_percent = proc.cpu_percent(interval=None)
            processes_with_cpu.append((proc, cpu_percent))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # 按CPU使用率排序并选择前n个进程
    top_processes = sorted(processes_with_cpu, key=lambda p: p[1], reverse=True)[:n]

    data = []
    for proc, cpu_percent in top_processes:
        data.append(proc.pid)
        data.append(proc.name())
        data.append(cpu_percent)

    return data



def requireProcInfo():
    top_processes = get_top_cpu_processes(5)
    process_ids = psutil.pids()
    # 进程总数
    procNum = len(process_ids)

    data = {
        "procinfo": top_processes,
        "procnum": procNum
    }

    return data