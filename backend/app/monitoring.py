import psutil

def get_system_metrics() -> dict:
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\")
    cpu_percent = psutil.cpu_percent(interval=1)

    return {
        "cpu_percent": cpu_percent,
        "memory": {
            "total": memory.total,
            "used": memory.used,
            "available": memory.available,
            "percent": memory.percent,
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent,
        },
        "uptime_seconds": int(
            psutil.time.time() - psutil.boot_time()
        ),
    }