"""
Advanced Network Tools
Created by Yinuo
"""

import socket
import subprocess
import platform
import threading
import time
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class AdvancedNetworkTools:
    """Advanced network analysis tools."""
    
    def __init__(self):
        """Initialize advanced network tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
    
    @handle_errors("Trace route", show_user=True)
    def trace_route(self, host: str, max_hops: int = 30) -> Optional[Dict[str, Any]]:
        """
        Perform trace route to host.
        
        Args:
            host: Target host
            max_hops: Maximum number of hops
            
        Returns:
            Trace route results or None on error
        """
        if not self.validator.validate_domain(host) and not self.validator.validate_ip_address(host):
            self.console.print("[red]Invalid host format[/red]")
            return None
        
        try:
            self.console.print(f"[cyan]Tracing route to {host}...[/cyan]")
            
            if platform.system().lower() == 'windows':
                command = ['tracert', '-h', str(max_hops), host]
            else:
                command = ['traceroute', '-m', str(max_hops), host]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                self.console.print(result.stdout)
                return {'host': host, 'output': result.stdout}
            else:
                self.console.print("[yellow]Trace route completed with errors[/yellow]")
                self.console.print(result.stdout)
                return {'host': host, 'output': result.stdout, 'errors': True}
                
        except subprocess.TimeoutExpired:
            self.console.print("[red]Trace route timed out[/red]")
            return None
        except Exception as e:
            self.error_handler.handle_exception(e, "Trace route")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("Network interface info", show_user=True)
    def get_network_interfaces(self) -> Optional[Dict[str, Any]]:
        """
        Get network interface information.
        
        Returns:
        Network interface information or None on error
        """
        try:
            self.console.print("[cyan]Getting network interface information...[/cyan]")
            
            if platform.system().lower() == 'windows':
                command = ['ipconfig', '/all']
            else:
                command = ['ifconfig', '-a']
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.console.print(result.stdout)
                return {'output': result.stdout}
            else:
                self.console.print("[red]Failed to get network interface info[/red]")
                return None
                
        except Exception as e:
            self.error_handler.handle_exception(e, "Network interface info")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("Network speed test", show_user=True)
    def test_network_speed(self) -> Optional[Dict[str, Any]]:
        """
        Basic network speed estimation.
        
        Returns:
        Speed test results or None on error
        """
        try:
            self.console.print("[cyan]Testing network speed...[/cyan]")
            self.console.print("[yellow]Note: This is a basic estimation. For accurate results, use dedicated speed test services.[/yellow]")
            
            # Test download speed by timing a simple HTTP request
            import requests
            test_urls = [
                'http://speedtest.tele2.net/1MB.zip',
                'http://ipv4.download.thinkbroadband.com/1MB.zip'
            ]
            
            for url in test_urls:
                try:
                    start_time = time.time()
                    response = requests.get(url, timeout=30, stream=True)
                    
                    if response.status_code == 200:
                        total_size = 0
                        for chunk in response.iter_content(chunk_size=8192):
                            total_size += len(chunk)
                        
                        end_time = time.time()
                        duration = end_time - start_time
                        
                        if duration > 0:
                            speed_bps = (total_size * 8) / duration
                            speed_mbps = speed_bps / 1000000
                            
                            results = {
                                'url': url,
                                'size_bytes': total_size,
                                'duration': duration,
                                'speed_bps': speed_bps,
                                'speed_mbps': speed_mbps
                            }
                            
                            self.display_speed_results(results)
                            return results
                            break
                except:
                    continue
            
            self.console.print("[yellow]Could not complete speed test with any URL[/yellow]")
            return None
            
        except ImportError:
            self.console.print("[yellow]Requests library not installed[/yellow]")
            return None
        except Exception as e:
            self.error_handler.handle_exception(e, "Network speed test")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_speed_results(self, data: Dict[str, Any]) -> None:
        """Display speed test results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Size", f"{data['size_bytes'] / 1024 / 1024:.2f} MB")
        table.add_row("Duration", f"{data['duration']:.2f} seconds")
        table.add_row("Speed", f"{data['speed_mbps']:.2f} Mbps")
        table.add_row("Speed", f"{data['speed_bps'] / 1000:.2f} Kbps")
        
        self.console.print(Panel(table, title="[bold]Network Speed Test Results[/bold]"))
    
    @handle_errors("ARP table scan", show_user=True)
    def scan_arp_table(self) -> Optional[Dict[str, Any]]:
        """
        Scan ARP table for local network devices.
        
        Returns:
        ARP table information or None on error
        """
        try:
            self.console.print("[cyan]Scanning ARP table...[/cyan]")
            
            if platform.system().lower() == 'windows':
                command = ['arp', '-a']
            else:
                command = ['arp', '-n']
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.console.print(result.stdout)
                return {'output': result.stdout}
            else:
                self.console.print("[red]Failed to scan ARP table[/red]")
                return None
                
        except Exception as e:
            self.error_handler.handle_exception(e, "ARP table scan")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("Network connection stats", show_user=True)
    def get_connection_stats(self) -> Optional[Dict[str, Any]]:
        """
        Get network connection statistics.
        
        Returns:
        Connection statistics or None on error
        """
        try:
            self.console.print("[cyan]Getting network connection statistics...[/cyan]")
            
            if platform.system().lower() == 'windows':
                command = ['netstat', '-an']
            else:
                command = ['netstat', '-tuln']
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                
                # Count different connection states
                states = {}
                for line in lines:
                    if 'ESTABLISHED' in line:
                        states['ESTABLISHED'] = states.get('ESTABLISHED', 0) + 1
                    elif 'LISTENING' in line or 'LISTEN' in line:
                        states['LISTENING'] = states.get('LISTENING', 0) + 1
                    elif 'TIME_WAIT' in line:
                        states['TIME_WAIT'] = states.get('TIME_WAIT', 0) + 1
                
                results = {
                    'states': states,
                    'total_lines': len(lines)
                }
                
                self.display_connection_stats(results)
                return results
            else:
                self.console.print("[red]Failed to get connection stats[/red]")
                return None
                
        except Exception as e:
            self.error_handler.handle_exception(e, "Connection stats")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_connection_stats(self, data: Dict[str, Any]) -> None:
        """Display connection statistics."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("State", style="cyan")
        table.add_column("Count", style="green")
        
        for state, count in data['states'].items():
            table.add_row(state, str(count))
        
        table.add_row("Total Lines", str(data['total_lines']))
        
        self.console.print(Panel(table, title="[bold]Network Connection Statistics[/bold]"))
    
    @handle_errors("DNS cache flush", show_user=True)
    def flush_dns_cache(self) -> bool:
        """
        Flush DNS cache.
        
        Returns:
        True if successful, False otherwise
        """
        try:
            self.console.print("[cyan]Flushing DNS cache...[/cyan]")
            
            if platform.system().lower() == 'windows':
                command = ['ipconfig', '/flushdns']
            else:
                command = ['sudo', 'systemd-resolve', '--flush-caches']
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.console.print("[green]DNS cache flushed successfully[/green]")
                self.console.print(result.stdout)
                return True
            else:
                self.console.print("[red]Failed to flush DNS cache[/red]")
                self.console.print(result.stderr)
                return False
                
        except Exception as e:
            self.error_handler.handle_exception(e, "DNS cache flush")
            self.console.print(f"[red]Error: {e}[/red]")
            return False
    
    @handle_errors("Network latency map", show_user=True)
    def create_latency_map(self, hosts: List[str]) -> Optional[Dict[str, Any]]:
        """
        Create latency map for multiple hosts.
        
        Args:
            hosts: List of hosts to test
            
        Returns:
        Latency map or None on error
        """
        try:
            self.console.print("[cyan]Creating latency map...[/cyan]")
            
            results = {}
            
            for host in hosts:
                if not self.validator.validate_domain(host) and not self.validator.validate_ip_address(host):
                    self.console.print(f"[red]Invalid host: {host}[/red]")
                    continue
                
                try:
                    param = '-n' if platform.system().lower() == 'windows' else '-c'
                    command = ['ping', param, '4', host]
                    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        # Extract average time
                        lines = result.stdout.split('\n')
                        avg_time = 0
                        for line in lines:
                            if 'Average' in line or 'avg' in line.lower():
                                try:
                                    if platform.system().lower() == 'windows':
                                        avg_time = float(line.split('=')[1].split('ms')[0])
                                    else:
                                        avg_time = float(line.split('/')[4])
                                except:
                                    pass
                        
                        results[host] = {
                            'status': 'reachable',
                            'avg_latency': avg_time,
                            'output': result.stdout
                        }
                        self.console.print(f"[green]{host}: {avg_time:.2f}ms[/green]")
                    else:
                        results[host] = {'status': 'unreachable', 'avg_latency': 0}
                        self.console.print(f"[red]{host}: Unreachable[/red]")
                        
                except Exception as e:
                    results[host] = {'status': 'error', 'avg_latency': 0, 'error': str(e)}
                    self.console.print(f"[yellow]{host}: Error - {e}[/yellow]")
            
            self.display_latency_map(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Latency map")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_latency_map(self, data: Dict[str, Any]) -> None:
        """Display latency map."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Host", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Avg Latency", style="white")
        
        for host, info in data.items():
            status = "[green]OK[/green]" if info['status'] == 'reachable' else "[red]FAIL[/red]"
            latency = f"{info['avg_latency']:.2f}ms" if info['avg_latency'] > 0 else "N/A"
            table.add_row(host, status, latency)
        
        self.console.print(Panel(table, title="[bold]Network Latency Map[/bold]"))
    
    def main(self) -> None:
        """Main entry point for advanced network tools."""
        tools = [
            {
                'name': 'Trace Route',
                'description': 'Trace network path to host',
                'function': self.run_trace_route
            },
            {
                'name': 'Network Interfaces',
                'description': 'Get network interface information',
                'function': self.run_network_interfaces
            },
            {
                'name': 'Network Speed Test',
                'description': 'Basic network speed estimation',
                'function': self.run_speed_test
            },
            {
                'name': 'ARP Table Scan',
                'description': 'Scan ARP table for devices',
                'function': self.run_arp_scan
            },
            {
                'name': 'Connection Stats',
                'description': 'Get network connection statistics',
                'function': self.run_connection_stats
            },
            {
                'name': 'Flush DNS Cache',
                'description': 'Flush DNS resolver cache',
                'function': self.run_dns_flush
            },
            {
                'name': 'Latency Map',
                'description': 'Create latency map for multiple hosts',
                'function': self.run_latency_map
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("Advanced Network", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_trace_route(self) -> None:
        """Run trace route."""
        self.console.print("\n[bold cyan]Trace Route[/bold cyan]")
        host = input("Enter host: ").strip()
        if host:
            self.trace_route(host)
    
    def run_network_interfaces(self) -> None:
        """Run network interfaces."""
        self.console.print("\n[bold cyan]Network Interfaces[/bold cyan]")
        self.get_network_interfaces()
    
    def run_speed_test(self) -> None:
        """Run speed test."""
        self.console.print("\n[bold cyan]Network Speed Test[/bold cyan]")
        self.test_network_speed()
    
    def run_arp_scan(self) -> None:
        """Run ARP scan."""
        self.console.print("\n[bold cyan]ARP Table Scan[/bold cyan]")
        self.scan_arp_table()
    
    def run_connection_stats(self) -> None:
        """Run connection stats."""
        self.console.print("\n[bold cyan]Connection Statistics[/bold cyan]")
        self.get_connection_stats()
    
    def run_dns_flush(self) -> None:
        """Run DNS flush."""
        self.console.print("\n[bold cyan]Flush DNS Cache[/bold cyan]")
        self.flush_dns_cache()
    
    def run_latency_map(self) -> None:
        """Run latency map."""
        self.console.print("\n[bold cyan]Network Latency Map[/bold cyan]")
        hosts_input = input("Enter hosts (comma-separated): ").strip()
        if hosts_input:
            hosts = [h.strip() for h in hosts_input.split(',')]
            self.create_latency_map(hosts)


def main():
    """Entry point for advanced network tools."""
    tools = AdvancedNetworkTools()
    tools.main()


if __name__ == "__main__":
    main()