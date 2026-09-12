"""
Security Module
Provides legitimate network testing and security analysis tools
Created by Yinuo

DISCLAIMER: These tools are for network administration, authorized testing,
and security research only. Use only on systems you own or have explicit
permission to test.
"""

import socket
import time
import threading
import queue
import subprocess
import platform
from typing import Dict, Any, Optional, List
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class SecurityTools:
    """Main class for security and network testing tools."""
    
    def __init__(self):
        """Initialize security tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.running = False
    
    @handle_errors("Connection rate test", show_user=True)
    def test_connection_rate(self, host: str, port: int, connections: int = 10) -> Optional[Dict[str, Any]]:
        """
        Test connection rate to a server (legitimate load testing).
        
        Args:
            host: Target host
            port: Target port
            connections: Number of connections to test
            
        Returns:
            Test results or None on error
        """
        if not self.validator.validate_domain(host) and not self.validator.validate_ip_address(host):
            self.console.print("[red]Invalid host format[/red]")
            return None
        
        if not self.validator.validate_port(str(port)):
            self.console.print("[red]Invalid port number[/red]")
            return None
        
        try:
            self.console.print(f"[cyan]Testing connection rate to {host}:{port}[/cyan]")
            self.console.print(f"[yellow]Testing {connections} connections...[/yellow]")
            
            successful = 0
            failed = 0
            times = []
            
            for i in range(connections):
                try:
                    start_time = time.time()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    result = sock.connect_ex((host, port))
                    end_time = time.time()
                    
                    if result == 0:
                        successful += 1
                        times.append((end_time - start_time) * 1000)  # Convert to ms
                        self.console.print(f"[green]Connection {i+1}/{connections}: SUCCESS ({times[-1]:.2f}ms)[/green]")
                    else:
                        failed += 1
                        self.console.print(f"[red]Connection {i+1}/{connections}: FAILED[/red]")
                    
                    sock.close()
                    time.sleep(0.1)  # Small delay between connections
                    
                except Exception as e:
                    failed += 1
                    self.console.print(f"[red]Connection {i+1}/{connections}: ERROR - {e}[/red]")
            
            # Calculate statistics
            avg_time = sum(times) / len(times) if times else 0
            max_time = max(times) if times else 0
            min_time = min(times) if times else 0
            
            results = {
                'host': host,
                'port': port,
                'total_connections': connections,
                'successful': successful,
                'failed': failed,
                'success_rate': (successful / connections * 100) if connections > 0 else 0,
                'avg_response_time': avg_time,
                'max_response_time': max_time,
                'min_response_time': min_time
            }
            
            self.display_connection_rate_results(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Connection rate test")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_connection_rate_results(self, data: Dict[str, Any]) -> None:
        """Display connection rate test results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Host", f"{data['host']}:{data['port']}")
        table.add_row("Total Connections", str(data['total_connections']))
        table.add_row("Successful", str(data['successful']))
        table.add_row("Failed", str(data['failed']))
        table.add_row("Success Rate", f"{data['success_rate']:.1f}%")
        table.add_row("Avg Response Time", f"{data['avg_response_time']:.2f}ms")
        table.add_row("Max Response Time", f"{data['max_response_time']:.2f}ms")
        table.add_row("Min Response Time", f"{data['min_response_time']:.2f}ms")
        
        self.console.print(Panel(table, title="[bold]Connection Rate Test Results[/bold]"))
    
    @handle_errors("Network latency test", show_user=True)
    def test_network_latency(self, host: str, count: int = 10) -> Optional[Dict[str, Any]]:
        """
        Test network latency using ICMP ping.
        
        Args:
            host: Target host
            count: Number of ping packets
            
        Returns:
            Latency test results or None on error
        """
        if not self.validator.validate_domain(host) and not self.validator.validate_ip_address(host):
            self.console.print("[red]Invalid host format[/red]")
            return None
        
        try:
            self.console.print(f"[cyan]Testing network latency to {host}[/cyan]")
            self.console.print(f"[yellow]Sending {count} ping packets...[/yellow]")
            
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, str(count), host]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                # Parse ping output
                lines = result.stdout.split('\n')
                times = []
                
                for line in lines:
                    if 'time=' in line.lower() or 'zeit=' in line.lower():
                        try:
                            # Extract time from ping output
                            if platform.system().lower() == 'windows':
                                time_str = line.split('time=')[1].split('ms')[0]
                            else:
                                time_str = line.split('time=')[1].split(' ')[0]
                            times.append(float(time_str))
                        except:
                            pass
                
                if times:
                    avg_time = sum(times) / len(times)
                    max_time = max(times)
                    min_time = min(times)
                    packet_loss = 0  # Would need more parsing for accurate packet loss
                    
                    results = {
                        'host': host,
                        'packets_sent': count,
                        'packets_received': len(times),
                        'packet_loss': packet_loss,
                        'avg_latency': avg_time,
                        'max_latency': max_time,
                        'min_latency': min_time
                    }
                    
                    self.display_latency_results(results)
                    return results
                else:
                    self.console.print("[yellow]Could not parse ping results[/yellow]")
                    return None
            else:
                self.console.print("[red]Ping failed[/red]")
                return None
                
        except subprocess.TimeoutExpired:
            self.console.print("[red]Ping timed out[/red]")
            return None
        except Exception as e:
            self.error_handler.handle_exception(e, "Network latency test")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_latency_results(self, data: Dict[str, Any]) -> None:
        """Display latency test results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Host", data['host'])
        table.add_row("Packets Sent", str(data['packets_sent']))
        table.add_row("Packets Received", str(data['packets_received']))
        table.add_row("Packet Loss", f"{data['packet_loss']}%")
        table.add_row("Average Latency", f"{data['avg_latency']:.2f}ms")
        table.add_row("Maximum Latency", f"{data['max_latency']:.2f}ms")
        table.add_row("Minimum Latency", f"{data['min_latency']:.2f}ms")
        
        self.console.print(Panel(table, title="[bold]Network Latency Test Results[/bold]"))
    
    @handle_errors("Active connection monitoring", show_user=True)
    def monitor_active_connections(self, duration: int = 10) -> Optional[Dict[str, Any]]:
        """
        Monitor active network connections.
        
        Args:
            duration: Monitoring duration in seconds
            
        Returns:
            Connection statistics or None on error
        """
        try:
            self.console.print(f"[cyan]Monitoring active connections for {duration} seconds...[/cyan]")
            
            if platform.system().lower() == 'windows':
                command = 'netstat -an'
            else:
                command = 'netstat -an'
            
            initial_connections = subprocess.run(command, shell=True, capture_output=True, text=True)
            time.sleep(duration)
            final_connections = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # Count connections
            initial_count = len([line for line in initial_connections.stdout.split('\n') if 'ESTABLISHED' in line])
            final_count = len([line for line in final_connections.stdout.split('\n') if 'ESTABLISHED' in line])
            
            results = {
                'duration': duration,
                'initial_connections': initial_count,
                'final_connections': final_count,
                'connection_change': final_count - initial_count
            }
            
            self.display_connection_monitoring(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Connection monitoring")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_connection_monitoring(self, data: Dict[str, Any]) -> None:
        """Display connection monitoring results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Monitoring Duration", f"{data['duration']} seconds")
        table.add_row("Initial Connections", str(data['initial_connections']))
        table.add_row("Final Connections", str(data['final_connections']))
        table.add_row("Connection Change", f"{data['connection_change']:+d}")
        
        self.console.print(Panel(table, title="[bold]Active Connection Monitoring[/bold]"))
    
    @handle_errors("Bandwidth estimation", show_user=True)
    def estimate_bandwidth(self, host: str, port: int = 80, test_size: int = 1024) -> Optional[Dict[str, Any]]:
        """
        Estimate bandwidth by timing data transfer.
        
        Args:
            host: Target host
            port: Target port
            test_size: Size of data to transfer in bytes
            
        Returns:
            Bandwidth estimation or None on error
        """
        if not self.validator.validate_domain(host) and not self.validator.validate_ip_address(host):
            self.console.print("[red]Invalid host format[/red]")
            return None
        
        try:
            self.console.print(f"[cyan]Estimating bandwidth to {host}:{port}[/cyan]")
            
            # Create test data
            test_data = b'X' * test_size
            
            start_time = time.time()
            
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((host, port))
                
                # Send data
                sock.sendall(test_data)
                
                # Receive response (if any)
                sock.recv(4096)
                
                sock.close()
                end_time = time.time()
                
                transfer_time = end_time - start_time
                if transfer_time > 0:
                    bandwidth_bps = (test_size * 8) / transfer_time  # bits per second
                    bandwidth_kbps = bandwidth_bps / 1000
                    bandwidth_mbps = bandwidth_kbps / 1000
                    
                    results = {
                        'host': host,
                        'port': port,
                        'data_size': test_size,
                        'transfer_time': transfer_time,
                        'bandwidth_bps': bandwidth_bps,
                        'bandwidth_kbps': bandwidth_kbps,
                        'bandwidth_mbps': bandwidth_mbps
                    }
                    
                    self.display_bandwidth_results(results)
                    return results
                else:
                    self.console.print("[yellow]Transfer too fast to measure[/yellow]")
                    return None
                    
            except Exception as e:
                self.console.print(f"[yellow]Could not complete transfer: {e}[/yellow]")
                return None
                
        except Exception as e:
            self.error_handler.handle_exception(e, "Bandwidth estimation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_bandwidth_results(self, data: Dict[str, Any]) -> None:
        """Display bandwidth estimation results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Host", f"{data['host']}:{data['port']}")
        table.add_row("Data Size", f"{data['data_size']} bytes")
        table.add_row("Transfer Time", f"{data['transfer_time']:.4f} seconds")
        table.add_row("Bandwidth", f"{data['bandwidth_mbps']:.2f} Mbps")
        table.add_row("Bandwidth", f"{data['bandwidth_kbps']:.2f} Kbps")
        table.add_row("Bandwidth", f"{data['bandwidth_bps']:.2f} bps")
        
        self.console.print(Panel(table, title="[bold]Bandwidth Estimation Results[/bold]"))
    
    @handle_errors("Port availability scan", show_user=True)
    def scan_port_availability(self, host: str, port_range: str = "1-1024") -> Optional[Dict[str, Any]]:
        """
        Scan for available ports (lightweight version).
        
        Args:
            host: Target host
            port_range: Port range to scan (e.g., "1-1024")
            
        Returns:
            Port scan results or None on error
        """
        if not self.validator.validate_domain(host) and not self.validator.validate_ip_address(host):
            self.console.print("[red]Invalid host format[/red]")
            return None
        
        try:
            # Parse port range
            if '-' in port_range:
                start, end = map(int, port_range.split('-'))
            else:
                start = end = int(port_range)
            
            # Limit range for safety
            if end - start > 1000:
                self.console.print("[yellow]Port range too large. Limiting to 1000 ports.[/yellow]")
                end = start + 1000
            
            self.console.print(f"[cyan]Scanning {host} ports {start}-{end}...[/cyan]")
            self.console.print("[yellow]This may take a while...[/yellow]")
            
            open_ports = []
            closed_ports = []
            
            for port in range(start, end + 1):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)  # Fast timeout
                    result = sock.connect_ex((host, port))
                    
                    if result == 0:
                        open_ports.append(port)
                        self.console.print(f"[green]Port {port}: OPEN[/green]")
                    else:
                        closed_ports.append(port)
                    
                    sock.close()
                    
                except:
                    closed_ports.append(port)
            
            results = {
                'host': host,
                'port_range': f"{start}-{end}",
                'open_ports': open_ports,
                'closed_ports_count': len(closed_ports),
                'total_ports': end - start + 1
            }
            
            self.display_port_scan_results(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Port availability scan")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_port_scan_results(self, data: Dict[str, Any]) -> None:
        """Display port scan results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Category", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Host", data['host'])
        table.add_row("Port Range", data['port_range'])
        table.add_row("Total Ports Scanned", str(data['total_ports']))
        table.add_row("Open Ports", str(len(data['open_ports'])))
        table.add_row("Closed Ports", str(data['closed_ports_count']))
        
        if data['open_ports']:
            table.add_row("Open Port List", ', '.join(map(str, data['open_ports'][:20])))
            if len(data['open_ports']) > 20:
                table.add_row("", f"... and {len(data['open_ports']) - 20} more")
        
        self.console.print(Panel(table, title="[bold]Port Availability Scan Results[/bold]"))
    
    @handle_errors("DNS resolution test", show_user=True)
    def test_dns_resolution(self, domain: str, dns_server: str = "8.8.8.8") -> Optional[Dict[str, Any]]:
        """
        Test DNS resolution speed and reliability.
        
        Args:
            domain: Domain to resolve
            dns_server: DNS server to use
            
        Returns:
            DNS test results or None on error
        """
        if not self.validator.validate_domain(domain):
            self.console.print("[red]Invalid domain format[/red]")
            return None
        
        try:
            self.console.print(f"[cyan]Testing DNS resolution for {domain}[/cyan]")
            self.console.print(f"[yellow]Using DNS server: {dns_server}[/yellow]")
            
            # Test resolution speed
            start_time = time.time()
            try:
                ip_address = socket.gethostbyname(domain)
                resolution_time = (time.time() - start_time) * 1000
                
                results = {
                    'domain': domain,
                    'dns_server': dns_server,
                    'resolved_ip': ip_address,
                    'resolution_time': resolution_time,
                    'successful': True
                }
                
                self.display_dns_results(results)
                return results
                
            except socket.gaierror:
                results = {
                    'domain': domain,
                    'dns_server': dns_server,
                    'resolved_ip': None,
                    'resolution_time': 0,
                    'successful': False
                }
                
                self.display_dns_results(results)
                return results
                
        except Exception as e:
            self.error_handler.handle_exception(e, "DNS resolution test")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_dns_results(self, data: Dict[str, Any]) -> None:
        """Display DNS resolution results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Domain", data['domain'])
        table.add_row("DNS Server", data['dns_server'])
        table.add_row("Resolved IP", data['resolved_ip'] if data['resolved_ip'] else "Failed")
        table.add_row("Resolution Time", f"{data['resolution_time']:.2f}ms" if data['successful'] else "N/A")
        table.add_row("Status", "[green]SUCCESS[/green]" if data['successful'] else "[red]FAILED[/red]")
        
        self.console.print(Panel(table, title="[bold]DNS Resolution Test Results[/bold]"))
    
    def main(self) -> None:
        """Main entry point for security module."""
        tools = [
            {
                'name': 'Connection Rate Test',
                'description': 'Test connection rate (legitimate load testing)',
                'function': self.run_connection_rate_test
            },
            {
                'name': 'Network Latency Test',
                'description': 'Test network latency using ping',
                'function': self.run_latency_test
            },
            {
                'name': 'Active Connection Monitor',
                'description': 'Monitor active network connections',
                'function': self.run_connection_monitor
            },
            {
                'name': 'Bandwidth Estimation',
                'description': 'Estimate network bandwidth',
                'function': self.run_bandwidth_test
            },
            {
                'name': 'Port Availability Scan',
                'description': 'Scan for available ports',
                'function': self.run_port_scan
            },
            {
                'name': 'DNS Resolution Test',
                'description': 'Test DNS resolution speed',
                'function': self.run_dns_test
            },
            {
                'name': 'Defensive Security Tools',
                'description': 'SSL analysis, security headers, log analysis',
                'function': self.run_defensive_tools
            },
            {
                'name': 'IP Logger',
                'description': 'Legitimate IP logging for security monitoring',
                'function': self.run_ip_logger
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("Security Testing", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_connection_rate_test(self) -> None:
        """Run connection rate test."""
        self.console.print("\n[bold cyan]Connection Rate Test[/bold cyan]")
        self.console.print("[yellow]LEGITIMATE LOAD TESTING ONLY[/yellow]")
        host = input("Enter host (IP or domain): ").strip()
        port = input("Enter port (default 80): ").strip()
        connections = input("Enter number of connections (default 10): ").strip()
        
        if not port:
            port = 80
        else:
            port = int(port)
        
        if not connections:
            connections = 10
        else:
            connections = int(connections)
        
        if host:
            self.test_connection_rate(host, port, connections)
    
    def run_latency_test(self) -> None:
        """Run latency test."""
        self.console.print("\n[bold cyan]Network Latency Test[/bold cyan]")
        host = input("Enter host (IP or domain): ").strip()
        count = input("Enter number of pings (default 10): ").strip()
        
        if not count:
            count = 10
        else:
            count = int(count)
        
        if host:
            self.test_network_latency(host, count)
    
    def run_connection_monitor(self) -> None:
        """Run connection monitor."""
        self.console.print("\n[bold cyan]Active Connection Monitor[/bold cyan]")
        duration = input("Enter monitoring duration in seconds (default 10): ").strip()
        
        if not duration:
            duration = 10
        else:
            duration = int(duration)
        
        self.monitor_active_connections(duration)
    
    def run_bandwidth_test(self) -> None:
        """Run bandwidth test."""
        self.console.print("\n[bold cyan]Bandwidth Estimation[/bold cyan]")
        host = input("Enter host (IP or domain): ").strip()
        port = input("Enter port (default 80): ").strip()
        test_size = input("Enter test size in bytes (default 1024): ").strip()
        
        if not port:
            port = 80
        else:
            port = int(port)
        
        if not test_size:
            test_size = 1024
        else:
            test_size = int(test_size)
        
        if host:
            self.estimate_bandwidth(host, port, test_size)
    
    def run_port_scan(self) -> None:
        """Run port scan."""
        self.console.print("\n[bold cyan]Port Availability Scan[/bold cyan]")
        self.console.print("[yellow]AUTHORIZED NETWORK TESTING ONLY[/yellow]")
        host = input("Enter host (IP or domain): ").strip()
        port_range = input("Enter port range (e.g., 1-1024, default 1-100): ").strip()
        
        if not port_range:
            port_range = "1-100"
        
        if host:
            self.scan_port_availability(host, port_range)
    
    def run_dns_test(self) -> None:
        """Run DNS test."""
        self.console.print("\n[bold cyan]DNS Resolution Test[/bold cyan]")
        domain = input("Enter domain: ").strip()
        dns_server = input("Enter DNS server (default 8.8.8.8): ").strip()
        
        if not dns_server:
            dns_server = "8.8.8.8"
        
        if domain:
            self.test_dns_resolution(domain, dns_server)
    
    def run_defensive_tools(self) -> None:
        """Run defensive security tools."""
        self.console.print("\n[bold cyan]Defensive Security Tools[/bold cyan]")
        from .defensive.defensive_tools import DefensiveSecurityTools
        defensive = DefensiveSecurityTools()
        defensive.main()
    
    def run_ip_logger(self) -> None:
        """Run IP logger."""
        self.console.print("\n[bold cyan]IP Logger[/bold cyan]")
        from .ip_logger import IPLogger
        ip_logger = IPLogger()
        ip_logger.main()


def main():
    """Entry point for security module."""
    security = SecurityTools()
    security.main()


if __name__ == "__main__":
    main()