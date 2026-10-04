"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Windows Technician & Diagnostics Agent          ║
╚══════════════════════════════════════════════════════════════╝
Diagnoses Windows errors, driver issues, audio, display, network,
storage, background processes, system performance, and port availability.
"""

import subprocess
import platform
import os
from typing import Dict, Any
from agents.base_agent import BaseAgent

class TechnicianAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TechnicianAgent",
            description="Diagnoses system performance, network, hardware, and Windows configuration."
        )

    def diagnose_system(self) -> Dict[str, Any]:
        """Perform comprehensive system diagnostics."""
        self.log_step("Diagnostic", "Scanning system performance and hardware...")
        uname = platform.uname()

        ps_script = (
            "$cpu = (Get-CimInstance Win32_Processor).LoadPercentage; "
            "$os = Get-CimInstance Win32_OperatingSystem; "
            "$freeRam = [math]::Round($os.FreePhysicalMemory / 1MB, 2); "
            "$totalRam = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2); "
            "$disks = Get-CimInstance Win32_LogicalDisk | ForEach-Object { \"$($_.DeviceID) Free: $([math]::Round($_.FreeSpace / 1GB, 1))GB of $([math]::Round($_.Size / 1GB, 1))GB\" }; "
            "$topProcs = Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 5 -Property Name, @{Name='MemMB';Expression={[math]::Round($_.WorkingSet64 / 1MB, 1)}}; "
            "Write-Output \"CPU_LOAD:$cpu|FREE_RAM:$freeRam|TOTAL_RAM:$totalRam|DISKS:$($disks -join '; ')|TOP_PROCS:$($topProcs | ConvertTo-Json -Compress)\""
        )

        try:
            res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True, timeout=15)
            output = res.stdout.strip()
        except Exception as e:
            output = f"Diagnostic failed: {e}"

        return {
            "os": f"{uname.system} {uname.release}",
            "machine": uname.machine,
            "node": uname.node,
            "raw_diagnostics": output
        }

    def test_network(self) -> Dict[str, Any]:
        """Perform network ping and DNS diagnostic."""
        self.log_step("Network", "Testing internet and DNS connectivity...")
        try:
            res = subprocess.run(["ping", "-n", "2", "8.8.8.8"], capture_output=True, text=True, timeout=10)
            ping_ok = res.returncode == 0
            dns_res = subprocess.run(["nslookup", "google.com"], capture_output=True, text=True, timeout=10)
            dns_ok = dns_res.returncode == 0
            return {
                "internet_connected": ping_ok,
                "dns_working": dns_ok,
                "ping_details": res.stdout.strip()
            }
        except Exception as e:
            return {"error": str(e), "internet_connected": False}

    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        lower = goal.lower()
        if "network" in lower or "internet" in lower or "ping" in lower or "wifi" in lower:
            return self.test_network()
        return self.diagnose_system()

technician_agent = TechnicianAgent()
