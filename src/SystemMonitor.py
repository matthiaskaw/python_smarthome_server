import logging
from typing import Dict, Optional
import psutil


class SystemMonitor:
    """
    Collects system metrics using psutil (cross-platform for CPU/RAM)
    and simple file read for temperature (Linux/Raspberry Pi only).
    """

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info("SystemMonitor initialized")
        # Initialize CPU percent (first call always returns 0)
        psutil.cpu_percent()

    async def get_system_metrics(self) -> Dict[str, Optional[float]]:
        """Returns CPU, RAM usage and temperature (if available)"""
        try:
            # Get CPU usage (second call returns actual value)
            cpu_usage = psutil.cpu_percent(interval=0)
            ram_usage = psutil.virtual_memory().percent
            cpu_temp = self._get_cpu_temperature()

            return {
                "cpu_usage": round(cpu_usage, 1),
                "ram_usage": round(ram_usage, 1),
                "cpu_temp": round(cpu_temp, 1) if cpu_temp else None
            }
        except Exception as e:
            self._logger.error(f"Error reading system metrics: {e}")
            return {"cpu_usage": 0, "ram_usage": 0, "cpu_temp": None}

    def _get_cpu_temperature(self) -> Optional[float]:
        """Single method: Read from standard thermal zone file (Raspberry Pi)"""
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                return float(f.read().strip()) / 1000.0
        except Exception:
            return None
