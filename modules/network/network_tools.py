"""
Network Module
Provides IP geolocation, WHOIS info, and port checking tools
"""

import requests
import socket
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class NetworkTools:
    """Main class for network tools."""
    
    def __init__(self):
        """Initialize network tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        # API endpoints
        self.apis = {
            'ipinfo': 'https://ipinfo.io/{}/json',
            'ipapi': 'http://ip-api.com/json/{}',
            'whois': 'https://whois.pconline.com.cn/ipJson.jsp?ip={}&json=true'
        }
    
    @handle_errors("IP geolocation", show_user=True)
    def get_ip_geolocation(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        Get geolocation information for an IP address.
        
        Args:
            ip: IP address to lookup
            
        Returns:
            Geolocation data or None on error
        """
        if not self.validator.validate_ip_address(ip):
            self.console.print("[red]Invalid IP address format[/red]")
            return None
        
        try:
            # Try ipinfo.io first
            url = self.apis['ipinfo'].format(ip)
            headers = {'User-Agent': 'TerminalMultiTool/1.0'}
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.display_ip_geolocation(data)
                return data
            else:
                # Fallback to ip-api
                url = self.apis['ipapi'].format(ip)
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    self.display_ip_geolocation(data)
                    return data
                else:
                    self.console.print(f"[yellow]API returned status {response.status_code}[/yellow]")
                    return None
                    
        except requests.RequestException as e:
            self.error_handler.handle_network_error(e, url)
            self.console.print("[red]Network error occurred[/red]")
            return None
    
    def display_ip_geolocation(self, data: Dict[str, Any]) -> None:
        """Display IP geolocation results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("IP", data.get('ip', data.get('query', 'N/A')))
        table.add_row("City", data.get('city', 'N/A'))
        table.add_row("Region", data.get('region', data.get('regionName', 'N/A')))
        table.add_row("Country", data.get('country', 'N/A'))
        table.add_row("Location", data.get('loc', 'N/A'))
        table.add_row("ISP", data.get('org', data.get('isp', 'N/A')))
        table.add_row("Timezone", data.get('timezone', 'N/A'))
        table.add_row("Postal", data.get('postal', 'N/A'))
        
        self.console.print(Panel(table, title="[bold]IP Geolocation[/bold]"))
    
    @handle_errors("WHOIS lookup", show_user=True)
    def whois_lookup(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        Perform WHOIS lookup for an IP address.
        
        Args:
            ip: IP address to lookup
            
        Returns:
            WHOIS data or None on error
        """
        if not self.validator.validate_ip_address(ip):
            self.console.print("[red]Invalid IP address format[/red]")
            return None
        
        try:
            # Try using python-whois if available
            try:
                import whois
                data = whois.whois(ip)
                
                if data:
                    self.display_whois_info(data)
                    return data
                else:
                    self.console.print("[yellow]No WHOIS data found[/yellow]")
                    return None
                    
            except ImportError:
                self.console.print("[yellow]python-whois not installed. Install with: pip install python-whois[/yellow]")
                
                # Fallback to API
                url = self.apis['whois'].format(ip)
                headers = {'User-Agent': 'TerminalMultiTool/1.0'}
                
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    self.display_whois_info(data)
                    return data
                else:
                    self.console.print(f"[yellow]API returned status {response.status_code}[/yellow]")
                    return None
                    
        except Exception as e:
            self.error_handler.handle_exception(e, "WHOIS lookup")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_whois_info(self, data: Dict[str, Any]) -> None:
        """Display WHOIS information."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        # Handle different data formats
        if isinstance(data, dict):
            for key, value in data.items():
                if value and value != 'N/A':
                    display_value = str(value)[:50] if len(str(value)) > 50 else str(value)
                    table.add_row(str(key).title(), display_value)
        else:
            # Handle whois library object
            if hasattr(data, 'domain_name'):
                table.add_row("Domain", str(data.domain_name))
            if hasattr(data, 'registrar'):
                table.add_row("Registrar", str(data.registrar))
            if hasattr(data, 'creation_date'):
                table.add_row("Created", str(data.creation_date))
            if hasattr(data, 'expiration_date'):
                table.add_row("Expires", str(data.expiration_date))
        
        self.console.print(Panel(table, title="[bold]WHOIS Information[/bold]"))
    
    @handle_errors("Reverse DNS lookup", show_user=True)
    def reverse_dns_lookup(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        Perform reverse DNS lookup for an IP address.
        
        Args:
            ip: IP address to lookup
            
        Returns:
            DNS information or None on error
        """
        if not self.validator.validate_ip_address(ip):
            self.console.print("[red]Invalid IP address format[/red]")
            return None
        
        try:
            hostname = socket.gethostbyaddr(ip)
            
            result = {
                'ip': ip,
                'hostname': hostname[0],
                'aliases': hostname[1],
                'ip_addresses': hostname[2]
            }
            
            self.display_reverse_dns(result)
            return result
            
        except socket.herror:
            self.console.print("[yellow]No reverse DNS record found[/yellow]")
            return None
        except Exception as e:
            self.error_handler.handle_exception(e, "Reverse DNS lookup")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_reverse_dns(self, data: Dict[str, Any]) -> None:
        """Display reverse DNS results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("IP", data.get('ip', 'N/A'))
        table.add_row("Hostname", data.get('hostname', 'N/A'))
        table.add_row("Aliases", ', '.join(data.get('aliases', []))[:50])
        table.add_row("IP Addresses", ', '.join(data.get('ip_addresses', []))[:50])
        
        self.console.print(Panel(table, title="[bold]Reverse DNS Lookup[/bold]"))
    
    @handle_errors("HTTP(S) port check", show_user=True)
    def check_http_port(self, host: str, port: int = 80, use_https: bool = False) -> Optional[Dict[str, Any]]:
        """
        Check if HTTP/HTTPS port is open and get server response.
        
        Args:
            host: Host to check
            port: Port number (default 80 for HTTP, 443 for HTTPS)
            use_https: Use HTTPS instead of HTTP
            
        Returns:
            Port check results or None on error
        """
        if not self.validator.validate_domain(host) and not self.validator.validate_ip_address(host):
            self.console.print("[red]Invalid host format[/red]")
            return None
        
        if not self.validator.validate_port(str(port)):
            self.console.print("[red]Invalid port number[/red]")
            return None
        
        try:
            protocol = 'https' if use_https else 'http'
            url = f"{protocol}://{host}:{port}"
            
            self.console.print(f"[cyan]Checking {protocol}://{host}:{port}...[/cyan]")
            
            response = requests.get(url, timeout=30, allow_redirects=True)
            
            result = {
                'host': host,
                'port': port,
                'protocol': protocol,
                'status_code': response.status_code,
                'server': response.headers.get('Server', 'N/A'),
                'content_type': response.headers.get('Content-Type', 'N/A'),
                'content_length': response.headers.get('Content-Length', 'N/A')
            }
            
            self.display_http_port_check(result)
            return result
            
        except requests.RequestException as e:
            self.error_handler.handle_network_error(e, url)
            self.console.print(f"[red]Port check failed: {e}[/red]")
            return None
        except Exception as e:
            self.error_handler.handle_exception(e, "HTTP port check")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_http_port_check(self, data: Dict[str, Any]) -> None:
        """Display HTTP port check results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Host", data.get('host', 'N/A'))
        table.add_row("Port", str(data.get('port', 'N/A')))
        table.add_row("Protocol", data.get('protocol', 'N/A'))
        table.add_row("Status Code", str(data.get('status_code', 'N/A')))
        table.add_row("Server", data.get('server', 'N/A'))
        table.add_row("Content Type", data.get('content_type', 'N/A'))
        table.add_row("Content Length", data.get('content_length', 'N/A'))
        
        self.console.print(Panel(table, title="[bold]HTTP Port Check[/bold]"))
    
    @handle_errors("Blacklist check", show_user=True)
    def check_blacklist(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        Check if IP is on common blacklists.
        
        Args:
            ip: IP address to check
            
        Returns:
            Blacklist status or None on error
        """
        if not self.validator.validate_ip_address(ip):
            self.console.print("[red]Invalid IP address format[/red]")
            return None
        
        self.console.print("[cyan]Blacklist check requires additional API access[/cyan]")
        self.console.print("[yellow]This is a placeholder for full implementation[/yellow]")
        
        # Placeholder response
        return {
            'ip': ip,
            'blacklisted': False,
            'lists_checked': ['placeholder list'],
            'listings': []
        }
    
    def main(self) -> None:
        """Main entry point for network module."""
        tools = [
            {
                'name': 'IP Geolocation',
                'description': 'Get geolocation data for IP address',
                'function': self.run_ip_geolocation
            },
            {
                'name': 'WHOIS Lookup',
                'description': 'Perform WHOIS lookup for IP',
                'function': self.run_whois_lookup
            },
            {
                'name': 'Reverse DNS Lookup',
                'description': 'Perform reverse DNS lookup',
                'function': self.run_reverse_dns
            },
            {
                'name': 'HTTP Port Check',
                'description': 'Check HTTP/HTTPS port availability',
                'function': self.run_http_port_check
            },
            {
                'name': 'Blacklist Check',
                'description': 'Check IP against blacklists',
                'function': self.run_blacklist_check
            },
            {
                'name': 'Advanced Network Tools',
                'description': 'Trace route, speed test, ARP scan',
                'function': self.run_advanced_tools
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("IP & Network", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_ip_geolocation(self) -> None:
        """Run IP geolocation."""
        self.console.print("\n[bold cyan]IP Geolocation[/bold cyan]")
        ip = input("Enter IP address: ").strip()
        if ip:
            self.get_ip_geolocation(ip)
    
    def run_whois_lookup(self) -> None:
        """Run WHOIS lookup."""
        self.console.print("\n[bold cyan]WHOIS Lookup[/bold cyan]")
        ip = input("Enter IP address: ").strip()
        if ip:
            self.whois_lookup(ip)
    
    def run_reverse_dns(self) -> None:
        """Run reverse DNS lookup."""
        self.console.print("\n[bold cyan]Reverse DNS Lookup[/bold cyan]")
        ip = input("Enter IP address: ").strip()
        if ip:
            self.reverse_dns_lookup(ip)
    
    def run_http_port_check(self) -> None:
        """Run HTTP port check."""
        self.console.print("\n[bold cyan]HTTP Port Check[/bold cyan]")
        host = input("Enter host (IP or domain): ").strip()
        port = input("Enter port (default 80): ").strip()
        use_https = input("Use HTTPS? (y/n, default n): ").strip().lower() == 'y'
        
        if not port:
            port = 443 if use_https else 80
        
        if host:
            self.check_http_port(host, int(port), use_https)
    
    def run_blacklist_check(self) -> None:
        """Run blacklist check."""
        self.console.print("\n[bold cyan]Blacklist Check[/bold cyan]")
        ip = input("Enter IP address: ").strip()
        if ip:
            self.check_blacklist(ip)
    
    def run_advanced_tools(self) -> None:
        """Run advanced network tools."""
        self.console.print("\n[bold cyan]Advanced Network Tools[/bold cyan]")
        from .advanced_tools import AdvancedNetworkTools
        advanced = AdvancedNetworkTools()
        advanced.main()


def main():
    """Entry point for network module."""
    network = NetworkTools()
    network.main()


if __name__ == "__main__":
    main()