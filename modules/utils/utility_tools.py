"""
Utilities Module
Provides productivity and network-related helpers
"""

import time
import socket
import subprocess
import platform
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class UtilityTools:
    """Main class for utility tools."""
    
    def __init__(self):
        """Initialize utility tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
    
    @handle_errors("Ping test", show_user=True)
    def ping_host(self, host: str, count: int = 4) -> Optional[Dict[str, Any]]:
        """
        Ping a host to check connectivity.
        
        Args:
            host: Host to ping
            count: Number of ping packets
            
        Returns:
            Ping results or None on error
        """
        if not self.validator.validate_domain(host) and not self.validator.validate_ip_address(host):
            self.console.print("[red]Invalid host format[/red]")
            return None
        
        try:
            self.console.print(f"[cyan]Pinging {host}...[/cyan]")
            
            # Use system ping command
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, str(count), host]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.console.print("[green]Ping successful![/green]")
                self.console.print(result.stdout)
                return {'success': True, 'output': result.stdout}
            else:
                self.console.print("[yellow]Ping failed or timed out[/yellow]")
                return {'success': False, 'output': result.stderr}
                
        except subprocess.TimeoutExpired:
            self.console.print("[red]Ping timed out[/red]")
            return None
        except Exception as e:
            self.error_handler.handle_exception(e, "Ping test")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("DNS lookup", show_user=True)
    def dns_lookup(self, domain: str) -> Optional[Dict[str, Any]]:
        """
        Perform DNS lookup for a domain.
        
        Args:
            domain: Domain to lookup
            
        Returns:
            DNS information or None on error
        """
        if not self.validator.validate_domain(domain):
            self.console.print("[red]Invalid domain format[/red]")
            return None
        
        try:
            self.console.print(f"[cyan]Performing DNS lookup for {domain}...[/cyan]")
            
            # Get IP address
            ip_address = socket.gethostbyname(domain)
            
            results = {
                'domain': domain,
                'ip_address': ip_address,
                'hostname': socket.gethostname()
            }
            
            self.display_dns_results(results)
            return results
            
        except socket.gaierror:
            self.console.print("[red]DNS lookup failed - domain not found[/red]")
            return None
        except Exception as e:
            self.error_handler.handle_exception(e, "DNS lookup")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_dns_results(self, data: Dict[str, Any]) -> None:
        """Display DNS lookup results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Domain", data.get('domain', 'N/A'))
        table.add_row("IP Address", data.get('ip_address', 'N/A'))
        table.add_row("Hostname", data.get('hostname', 'N/A'))
        
        self.console.print(Panel(table, title="[bold]DNS Lookup Results[/bold]"))
    
    @handle_errors("Port scan", show_user=True)
    def scan_ports(self, host: str, ports: str = "21,22,80,443,8080") -> Optional[Dict[str, Any]]:
        """
        Scan common ports on a host.
        
        Args:
            host: Host to scan
            ports: Comma-separated list of ports to scan
            
        Returns:
            Port scan results or None on error
        """
        if not self.validator.validate_domain(host) and not self.validator.validate_ip_address(host):
            self.console.print("[red]Invalid host format[/red]")
            return None
        
        try:
            port_list = [int(p.strip()) for p in ports.split(',')]
            results = {'host': host, 'open_ports': [], 'closed_ports': []}
            
            self.console.print(f"[cyan]Scanning {host} on ports: {ports}[/cyan]")
            
            for port in port_list:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result = sock.connect_ex((host, port))
                    
                    if result == 0:
                        results['open_ports'].append(port)
                        self.console.print(f"[green]Port {port}: OPEN[/green]")
                    else:
                        results['closed_ports'].append(port)
                        self.console.print(f"[red]Port {port}: CLOSED[/red]")
                    
                    sock.close()
                except:
                    results['closed_ports'].append(port)
                    self.console.print(f"[yellow]Port {port}: ERROR[/yellow]")
            
            self.display_port_results(results)
            return results
            
        except ValueError:
            self.console.print("[red]Invalid port format[/red]")
            return None
        except Exception as e:
            self.error_handler.handle_exception(e, "Port scan")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_port_results(self, data: Dict[str, Any]) -> None:
        """Display port scan results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Category", style="cyan")
        table.add_column("Ports", style="green")
        
        table.add_row("Host", data.get('host', 'N/A'))
        table.add_row("Open Ports", ', '.join(map(str, data.get('open_ports', []))))
        table.add_row("Closed Ports", ', '.join(map(str, data.get('closed_ports', []))))
        
        self.console.print(Panel(table, title="[bold]Port Scan Results[/bold]"))
    
    @handle_errors("System info", show_user=True)
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information.
        
        Returns:
            System information dictionary
        """
        try:
            info = {
                'system': platform.system(),
                'node': platform.node(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'python_version': platform.python_version()
            }
            
            self.display_system_info(info)
            return info
            
        except Exception as e:
            self.error_handler.handle_exception(e, "System info")
            self.console.print(f"[red]Error: {e}[/red]")
            return {}
    
    def display_system_info(self, data: Dict[str, Any]) -> None:
        """Display system information."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in data.items():
            table.add_row(key.replace('_', ' ').title(), str(value))
        
        self.console.print(Panel(table, title="[bold]System Information[/bold]"))
    
    @handle_errors("HTTP headers check", show_user=True)
    def check_http_headers(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Check HTTP headers for a URL.
        
        Args:
            url: URL to check
            
        Returns:
            HTTP headers or None on error
        """
        if not self.validator.validate_url(url):
            self.console.print("[red]Invalid URL format[/red]")
            return None
        
        try:
            import requests
            
            self.console.print(f"[cyan]Checking HTTP headers for {url}...[/cyan]")
            
            response = requests.head(url, timeout=30)
            
            headers = dict(response.headers)
            self.display_http_headers(headers)
            
            return headers
            
        except ImportError:
            self.console.print("[yellow]Requests library not installed[/yellow]")
            return None
        except Exception as e:
            self.error_handler.handle_exception(e, "HTTP headers check")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_http_headers(self, headers: Dict[str, str]) -> None:
        """Display HTTP headers."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Header", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in headers.items():
            table.add_row(key, str(value)[:50])
        
        self.console.print(Panel(table, title="[bold]HTTP Headers[/bold]"))
    
    def main(self) -> None:
        """Main entry point for utilities module."""
        tools = [
            {
                'name': 'Ping Host',
                'description': 'Test network connectivity to a host',
                'function': self.run_ping
            },
            {
                'name': 'DNS Lookup',
                'description': 'Resolve domain to IP address',
                'function': self.run_dns_lookup
            },
            {
                'name': 'Port Scanner',
                'description': 'Scan common ports on a host',
                'function': self.run_port_scan
            },
            {
                'name': 'System Information',
                'description': 'Display system information',
                'function': self.run_system_info
            },
            {
                'name': 'HTTP Headers Check',
                'description': 'Check HTTP headers for a URL',
                'function': self.run_http_headers
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("Utilities", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_ping(self) -> None:
        """Run ping test."""
        self.console.print("\n[bold cyan]Ping Host[/bold cyan]")
        host = input("Enter host (IP or domain): ").strip()
        if host:
            self.ping_host(host)
    
    def run_dns_lookup(self) -> None:
        """Run DNS lookup."""
        self.console.print("\n[bold cyan]DNS Lookup[/bold cyan]")
        domain = input("Enter domain: ").strip()
        if domain:
            self.dns_lookup(domain)
    
    def run_port_scan(self) -> None:
        """Run port scan."""
        self.console.print("\n[bold cyan]Port Scanner[/bold cyan]")
        host = input("Enter host (IP or domain): ").strip()
        ports = input("Enter ports (comma-separated, default: 21,22,80,443,8080): ").strip()
        if not ports:
            ports = "21,22,80,443,8080"
        if host:
            self.scan_ports(host, ports)
    
    def run_system_info(self) -> None:
        """Run system info."""
        self.console.print("\n[bold cyan]System Information[/bold cyan]")
        self.get_system_info()
    
    def run_http_headers(self) -> None:
        """Run HTTP headers check."""
        self.console.print("\n[bold cyan]HTTP Headers Check[/bold cyan]")
        url = input("Enter URL (e.g., https://example.com): ").strip()
        if url:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            self.check_http_headers(url)


def main():
    """Entry point for utilities module."""
    utilities = UtilityTools()
    utilities.main()


if __name__ == "__main__":
    main()