"""
System Monitoring Tools Module
Provides system monitoring and analysis utilities
Created by Yinuo
"""

import platform
import subprocess
import psutil
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class SystemTools:
    """Main class for system monitoring tools."""
    
    def __init__(self):
        """Initialize system tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
    
    @handle_errors("System information", show_user=True)
    def get_system_info(self) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive system information.
        
        Returns:
            System information or None on error
        """
        try:
            info = {
                'system': platform.system(),
                'node': platform.node(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'architecture': platform.architecture()[0],
                'hostname': platform.node(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                'uptime': str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0]
            }
            
            self.display_system_info(info)
            return info
            
        except Exception as e:
            self.error_handler.handle_exception(e, "System info")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_system_info(self, data: Dict[str, Any]) -> None:
        """Display system information."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in data.items():
            table.add_row(key.replace('_', ' ').title(), str(value))
        
        self.console.print(Panel(table, title="[bold]System Information[/bold]"))
    
    @handle_errors("CPU monitoring", show_user=True)
    def monitor_cpu(self, duration: int = 5) -> Optional[Dict[str, Any]]:
        """
        Monitor CPU usage over time.
        
        Args:
            duration: Monitoring duration in seconds
            
        Returns:
            CPU statistics or None on error
        """
        try:
            self.console.print(f"[cyan]Monitoring CPU for {duration} seconds...[/cyan]")
            
            cpu_stats = []
            
            for i in range(duration):
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_freq = psutil.cpu_freq()
                cpu_count = psutil.cpu_count()
                
                cpu_stats.append({
                    'timestamp': datetime.now().isoformat(),
                    'cpu_percent': cpu_percent,
                    'cpu_freq': cpu_freq.current if cpu_freq else 0,
                    'cpu_count': cpu_count
                })
                
                self.console.print(f"[green]CPU: {cpu_percent}%[/green]")
                time.sleep(1)
            
            # Calculate averages
            avg_cpu = sum(s['cpu_percent'] for s in cpu_stats) / len(cpu_stats)
            
            results = {
                'duration': duration,
                'average_cpu': avg_cpu,
                'current_cpu': cpu_stats[-1]['cpu_percent'],
                'cpu_count': cpu_count,
                'samples': cpu_stats
            }
            
            self.display_cpu_monitoring(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "CPU monitoring")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_cpu_monitoring(self, data: Dict[str, Any]) -> None:
        """Display CPU monitoring results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Duration", f"{data['duration']} seconds")
        table.add_row("Average CPU", f"{data['average_cpu']:.1f}%")
        table.add_row("Current CPU", f"{data['current_cpu']:.1f}%")
        table.add_row("CPU Count", str(data['cpu_count']))
        
        self.console.print(Panel(table, title="[bold]CPU Monitoring Results[/bold]"))
    
    @handle_errors("Memory monitoring", show_user=True)
    def monitor_memory(self) -> Optional[Dict[str, Any]]:
        """
        Monitor memory usage.
        
        Returns:
            Memory statistics or None on error
        """
        try:
            mem = psutil.virtual_memory()
            
            results = {
                'total': mem.total,
                'available': mem.available,
                'used': mem.used,
                'percent': mem.percent,
                'total_gb': mem.total / (1024**3),
                'available_gb': mem.available / (1024**3),
                'used_gb': mem.used / (1024**3)
            }
            
            self.display_memory_monitoring(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Memory monitoring")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_memory_monitoring(self, data: Dict[str, Any]) -> None:
        """Display memory monitoring results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total", f"{data['total_gb']:.2f} GB")
        table.add_row("Available", f"{data['available_gb']:.2f} GB")
        table.add_row("Used", f"{data['used_gb']:.2f} GB")
        table.add_row("Usage", f"{data['percent']:.1f}%")
        
        self.console.print(Panel(table, title="[bold]Memory Monitoring[/bold]"))
    
    @handle_errors("Disk monitoring", show_user=True)
    def monitor_disk(self) -> Optional[Dict[str, Any]]:
        """
        Monitor disk usage.
        
        Returns:
        Disk statistics or None on error
        """
        try:
            disk = psutil.disk_usage('/')
            
            results = {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent,
                'total_gb': disk.total / (1024**3),
                'used_gb': disk.used / (1024**3),
                'free_gb': disk.free / (1024**3)
            }
            
            self.display_disk_monitoring(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Disk monitoring")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_disk_monitoring(self, data: Dict[str, Any]) -> None:
        """Display disk monitoring results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total", f"{data['total_gb']:.2f} GB")
        table.add_row("Used", f"{data['used_gb']:.2f} GB")
        table.add_row("Free", f"{data['free_gb']:.2f} GB")
        table.add_row("Usage", f"{data['percent']:.1f}%")
        
        self.console.print(Panel(table, title="[bold]Disk Monitoring[/bold]"))
    
    @handle_errors("Process list", show_user=True)
    def list_processes(self, limit: int = 10) -> Optional[List[Dict[str, Any]]]:
        """
        List running processes.
        
        Args:
            limit: Number of processes to show
            
        Returns:
            Process list or None on error
        """
        try:
            self.console.print(f"[cyan]Listing top {limit} processes...[/cyan]")
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_percent': proc.info['memory_percent']
                    })
                except:
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            self.display_processes(processes[:limit])
            return processes[:limit]
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Process list")
            self.console.print(f"[red]Error: {e}[-red]")
            return None
    
    def display_processes(self, processes: List[Dict[str, Any]]) -> None:
        """Display process list."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("PID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("CPU %", style="yellow")
        table.add_column("Memory %", style="magenta")
        
        for proc in processes:
            table.add_row(
                str(proc['pid']),
                proc['name'][:20] if proc['name'] else 'N/A',
                f"{proc['cpu_percent']:.1f}" if proc['cpu_percent'] else 'N/A',
                f"{proc['memory_percent']:.1f}" if proc['memory_percent'] else 'N/A'
            )
        
        self.console.print(Panel(table, title=f"[bold]Top {len(processes)} Processes[/bold]"))
    
    @handle_errors("Network connections", show_user=True)
    def list_connections(self) -> Optional[List[Dict[str, Any]]]:
        """
        List network connections.
        
        Returns:
        Connection list or None on error
        """
        try:
            self.console.print("[cyan]Listing network connections...[/cyan]")
            
            connections = []
            for conn in psutil.net_connections():
                try:
                    connections.append({
                        'type': conn.type,
                        'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A",
                        'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        'status': conn.status,
                        'pid': conn.pid
                    })
                except:
                    pass
            
            self.display_connections(connections[:20])
            return connections[:20]
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Network connections")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_connections(self, connections: List[Dict[str, Any]]) -> None:
        """Display network connections."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Type", style="cyan")
        table.add_column("Local", style="green")
        table.add_column("Remote", style="white")
        table.add_column("Status", style="yellow")
        table.add_column("PID", style="magenta")
        
        for conn in connections:
            table.add_row(
                str(conn['type']),
                conn['local_address'],
                conn['remote_address'],
                conn['status'],
                str(conn['pid']) if conn['pid'] else 'N/A'
            )
        
        self.console.print(Panel(table, title=f"[bold]Network Connections ({len(connections)} shown)[/bold]"))
    
    @handle_errors("Battery status", show_user=True)
    def check_battery(self) -> Optional[Dict[str, Any]]:
        """
        Check battery status (laptops only).
        
        Returns:
        Battery information or None on error
        """
        try:
            if not hasattr(psutil, 'sensors_battery'):
                self.console.print("[yellow]Battery monitoring not available on this system[/yellow]")
                return None
            
            battery = psutil.sensors_battery()
            
            if battery:
                results = {
                    'percent': battery.percent,
                    'power_plugged': battery.power_plugged,
                    'seconds_left': battery.secsleft if hasattr(battery, 'secsleft') else None
                }
                
                self.display_battery_status(results)
                return results
            else:
                self.console.print("[yellow]No battery detected[/yellow]")
                return None
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Battery check")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_battery_status(self, data: Dict[str, Any]) -> None:
        """Display battery status."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Battery Level", f"{data['percent']}%")
        table.add_row("Power Plugged", str(data['power_plugged']))
        
        if data['seconds_left']:
            time_left = data['seconds_left'] / 60
            table.add_row("Time Left", f"{time_left:.0f} minutes")
        
        self.console.print(Panel(table, title="[bold]Battery Status[/bold]"))
    
    @handle_errors("Temperature monitoring", show_user=True)
    def check_temperature(self) -> Optional[Dict[str, Any]]:
        """
        Check system temperature.
        
        Returns:
            Temperature information or None on error
        """
        try:
            if not hasattr(psutil, 'sensors_temperatures'):
                self.console.print("[yellow]Temperature monitoring not available on this system[/yellow]")
                return None
            
            temps = psutil.sensors_temperatures(fahrenheit=False)
            
            if temps:
                results = []
                for temp in temps:
                    results.append({
                        'label': temp.label,
                        'current': temp.current,
                        'high': temp.high,
                        'critical': temp.critical
                    })
                
                self.display_temperature(results)
                return results
            else:
                self.console.print("[yellow]No temperature sensors found[/yellow]")
                return None
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Temperature check")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_temperature(self, temps: List[Dict[str, Any]]) -> None:
        """Display temperature information."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Sensor", style="cyan")
        table.add_column("Current", style="green")
        table.add_column("High", style="yellow")
        table.add_column("Critical", style="red")
        
        for temp in temps:
            table.add_row(
                temp['label'],
                f"{temp['current']:.1f}°C" if temp['current'] else 'N/A',
                f"{temp['high']:.1f}°C" if temp['high'] else 'N/A',
                f"{temp['critical']:.1f}°C" if temp['critical'] else 'N/A'
            )
        
        self.console.print(Panel(table, title="[bold]Temperature Sensors[/bold]"))
    
    def main(self) -> None:
        """Main entry point for system tools."""
        tools = [
            {
                'name': 'System Info',
                'description': 'Get comprehensive system information',
                'function': self.run_system_info
            },
            {
                'name': 'CPU Monitor',
                'description': 'Monitor CPU usage over time',
                'function': self.run_cpu_monitor
            },
            {
                'name': 'Memory Monitor',
                'description': 'Monitor memory usage',
                'function': self.run_memory_monitor
            },
            {
                'name': 'Disk Monitor',
                'description': 'Monitor disk usage',
                'function': self.run_disk_monitor
            },
            {
                'name': 'Process List',
                'description': 'List running processes',
                'function': self.run_process_list
            },
            {
                'name': 'Network Connections',
                'description': 'List network connections',
                'function': self.run_connections
            },
            {
                'name': 'Battery Status',
                'description': 'Check battery status',
                'function': self.run_battery
            },
            {
                'name': 'Temperature',
                'description': 'Check system temperature',
                'function': self.run_temperature
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("System Tools", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_system_info(self) -> None:
        """Run system info."""
        self.console.print("\n[bold cyan]System Information[/bold cyan]")
        self.get_system_info()
    
    def run_cpu_monitor(self) -> None:
        """Run CPU monitor."""
        self.console.print("\n[bold cyan]CPU Monitor[/bold cyan]")
        duration = input("Enter duration in seconds (default 5): ").strip()
        if not duration:
            duration = 5
        else:
            duration = int(duration)
        self.monitor_cpu(duration)
    
    def run_memory_monitor(self) -> None:
        """Run memory monitor."""
        self.console.print("\n[bold cyan]Memory Monitor[/bold cyan]")
        self.monitor_memory()
    
    def run_disk_monitor(self) -> None:
        """Run disk monitor."""
        self.console.print("\n[bold cyan]Disk Monitor[/bold cyan]")
        self.monitor_disk()
    
    def run_process_list(self) -> None:
        """Run process list."""
        self.console.print("\n[bold cyan]Process List[/bold cyan]")
        limit = input("Enter number of processes to show (default 10): ").strip()
        if not limit:
            limit = 10
        else:
            limit = int(limit)
        self.list_processes(limit)
    
    def run_connections(self) -> None:
        """Run network connections."""
        self.console.print("\n[bold cyan]Network Connections[/bold cyan]")
        self.list_connections()
    
    def run_battery(self) -> None:
        """Run battery check."""
        self.console.print("\n[bold cyan]Battery Status[/bold cyan]")
        self.check_battery()
    
    def run_temperature(self) -> None:
        """Run temperature check."""
        self.console.print("\n[bold cyan]Temperature Check[/bold cyan]")
        self.check_temperature()


def main():
    """Entry point for system tools."""
    tools = SystemTools()
    tools.main()


if __name__ == "__main__":
    main()
