import psutil

def bytes_to_gb(value: int) -> float:
    return round(value / (1024 ** 3), 2)

def get_system_metrics() -> dict:
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\")
    cpu_percent = psutil.cpu_percent(interval=1)

    return {
        "cpu_percent": cpu_percent,
        "memory": {
            "total_bytes": memory.total,
            "used_bytes": memory.used,
            "available_bytes": memory.available,
            "total_gb": bytes_to_gb(memory.total),
            "used_gb": bytes_to_gb(memory.used),
            "free_gb": bytes_to_gb(memory.free),
            "available_gb": bytes_to_gb(memory.available),
            "percent": memory.percent,
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "total_gb": bytes_to_gb(disk.total),
            "used_gb": bytes_to_gb(disk.used),
            "free_gb": bytes_to_gb(disk.free),
            "percent": disk.percent,
        },
        "uptime_seconds": int(
            psutil.time.time() - psutil.boot_time()
        ),
    }