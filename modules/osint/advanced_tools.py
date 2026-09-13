"""
Advanced OSINT Tools
Created by Yinuo
"""

import requests
import re
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class AdvancedOSINTTools:
    """Advanced OSINT tools for legitimate research."""
    
    def __init__(self):
        """Initialize advanced OSINT tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
    
    @handle_errors("VPN detection", show_user=True)
    def detect_vpn_proxy(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        Detect if IP is VPN/Proxy using public APIs.
        
        Args:
            ip: IP address to check
            
        Returns:
            Detection results or None on error
        """
        if not self.validator.validate_ip_address(ip):
            self.console.print("[red]Invalid IP format[/red]")
            return None
        
        try:
            # Use multiple APIs for detection
            results = {'ip': ip, 'detection_results': []}
            
            # Try ipinfo.io
            try:
                response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('org', '').lower() in ['vpn', 'proxy', 'hosting']:
                        results['detection_results'].append({'source': 'ipinfo', 'vpn': True, 'org': data.get('org')})
                    else:
                        results['detection_results'].append({'source': 'ipinfo', 'vpn': False, 'org': data.get('org')})
            except:
                results['detection_results'].append({'source': 'ipinfo', 'vpn': None, 'error': 'API failed'})
            
            # Try ip-api.com
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('isp', '').lower() in ['vpn', 'proxy', 'datacenter']:
                        results['detection_results'].append({'source': 'ip-api', 'vpn': True, 'isp': data.get('isp')})
                    else:
                        results['detection_results'].append({'source': 'ip-api', 'vpn': False, 'isp': data.get('isp')})
            except:
                results['detection_results'].append({'source': 'ip-api', 'vpn': None, 'error': 'API failed'})
            
            self.display_vpn_detection(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "VPN detection")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_vpn_detection(self, data: Dict[str, Any]) -> None:
        """Display VPN detection results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Source", style="cyan")
        table.add_column("VPN/Proxy", style="green")
        table.add_column("Details", style="white")
        
        for result in data['detection_results']:
            vpn_status = "[red]YES[/red]" if result.get('vpn') else "[green]NO[/green]" if result.get('vpn') is False else "[yellow]UNKNOWN[/yellow]"
            details = result.get('org') or result.get('isp') or result.get('error', 'N/A')
            table.add_row(result['source'], vpn_status, details)
        
        self.console.print(Panel(table, title=f"[bold]VPN/Proxy Detection for {data['ip']}[/bold]"))
    
    @handle_errors("Username search (brand protection)", show_user=True)
    def username_search_branded(self, username: str, platforms: List[str] = None) -> Optional[Dict[str, Any]]:
        """
        Search username across platforms for brand protection.
        
        Args:
            username: Username to search
            platforms: List of platforms to check
            
        Returns:
            Search results or None on error
        """
        if not self.validator.validate_username(username):
            self.console.print("[red]Invalid username format[/red]")
            return None
        
        if platforms is None:
            platforms = [
                ('GitHub', f'https://github.com/{username}'),
                ('Twitter', f'https://twitter.com/{username}'),
                ('Reddit', f'https://reddit.com/user/{username}'),
                ('Instagram', f'https://instagram.com/{username}'),
                ('YouTube', f'https://youtube.com/@{username}'),
                ('TikTok', f'https://tiktok.com/@{username}'),
                ('LinkedIn', f'https://linkedin.com/in/{username}'),
                ('Facebook', f'https://facebook.com/{username}'),
            ]
        
        try:
            results = {'username': username, 'found_platforms': [], 'not_found': []}
            
            for platform, url in platforms:
                try:
                    response = requests.head(url, timeout=5, allow_redirects=True)
                    if response.status_code == 200:
                        results['found_platforms'].append({'platform': platform, 'url': url})
                        self.console.print(f"[green]✓[/green] {platform}: Found")
                    else:
                        results['not_found'].append({'platform': platform, 'status': response.status_code})
                        self.console.print(f"[red]✗[/red] {platform}: Not found")
                except:
                    results['not_found'].append({'platform': platform, 'status': 'Error'})
                    self.console.print(f"[yellow]?[/yellow] {platform}: Unable to check")
            
            self.display_username_results(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Username search")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_username_results(self, data: Dict[str, Any]) -> None:
        """Display username search results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Platform", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("URL", style="white")
        
        for found in data['found_platforms']:
            table.add_row(found['platform'], "[green]FOUND[/green]", found['url'])
        
        for not_found in data['not_found'][:5]:
            table.add_row(not_found['platform'], "[red]NOT FOUND[/red]", f"Status: {not_found['status']}")
        
        self.console.print(Panel(table, title=f"[bold]Username Search: {data['username']}[/bold]"))
        self.console.print(f"[green]Found on {len(data['found_platforms'])} platforms[/green]")
    
    @handle_errors("Email breach check", show_user=True)
    def check_email_breaches(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Check if email has been in data breaches.
        
        Args:
            email: Email address to check
            
        Returns:
            Breach information or None on error
        """
        if not self.validator.validate_email(email):
            self.console.print("[red]Invalid email format[/red]")
            return None
        
        try:
            # Have I Been Pwned API (requires API key for full functionality)
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {'User-Agent': 'TerminalMultiTool/1.0'}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                breaches = response.json()
                results = {
                    'email': email,
                    'breach_count': len(breaches),
                    'breaches': [
                        {
                            'name': b.get('Name'),
                            'date': b.get('BreachDate'),
                            'data_classes': b.get('DataClasses', [])
                        } for b in breaches[:5]
                    ]
                }
                
                self.display_breach_results(results)
                return results
            elif response.status_code == 404:
                self.console.print("[green]No breaches found for this email[/green]")
                return {'email': email, 'breach_count': 0, 'breaches': []}
            else:
                self.console.print(f"[yellow]API returned status {response.status_code}[/yellow]")
                self.console.print("[yellow]Note: Full functionality requires HIBP API key[/yellow]")
                return None
                
        except Exception as e:
            self.error_handler.handle_exception(e, "Email breach check")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_breach_results(self, data: Dict[str, Any]) -> None:
        """Display breach check results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Breach", style="cyan")
        table.add_column("Date", style="green")
        table.add_column("Data Compromised", style="white")
        
        for breach in data['breaches']:
            table.add_row(
                breach['name'],
                breach['date'],
                ', '.join(breach['data_classes'][:3])
            )
        
        self.console.print(Panel(table, title=f"[bold]Breaches Found: {data['breach_count']}[/bold]"))
    
    @handle_errors("Phone number lookup", show_user=True)
    def lookup_phone_number(self, phone: str) -> Optional[Dict[str, Any]]:
        """
        Basic phone number information (format validation only).
        
        Args:
            phone: Phone number to lookup
            
        Returns:
            Phone number info or None on error
        """
        try:
            # Remove non-numeric characters
            clean_phone = re.sub(r'[^\d+]', '', phone)
            
            # Basic format validation
            if len(clean_phone) < 10:
                self.console.print("[red]Invalid phone number format[/red]")
                return None
            
            results = {
                'original': phone,
                'cleaned': clean_phone,
                'length': len(clean_phone),
                'type': 'mobile' if len(clean_phone) == 11 else 'unknown',
                'valid_format': len(clean_phone) >= 10
            }
            
            self.display_phone_results(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Phone lookup")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_phone_results(self, data: Dict[str, Any]) -> None:
        """Display phone number results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Original", data['original'])
        table.add_row("Cleaned", data['cleaned'])
        table.add_row("Length", str(data['length']))
        table.add_row("Type", data['type'])
        table.add_row("Valid Format", str(data['valid_format']))
        
        self.console.print(Panel(table, title="[bold]Phone Number Analysis[/bold]"))
        self.console.print("[yellow]Note: Full phone lookup requires additional services[/yellow]")
    
    def main(self) -> None:
        """Main entry point for advanced OSINT tools."""
        tools = [
            {
                'name': 'VPN/Proxy Detection',
                'description': 'Detect if IP is VPN or proxy',
                'function': self.run_vpn_detection
            },
            {
                'name': 'Username Search',
                'description': 'Brand protection username search',
                'function': self.run_username_search
            },
            {
                'name': 'Email Breach Check',
                'description': 'Check email for data breaches',
                'function': self.run_breach_check
            },
            {
                'name': 'Phone Lookup',
                'description': 'Basic phone number analysis',
                'function': self.run_phone_lookup
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("Advanced OSINT", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_vpn_detection(self) -> None:
        """Run VPN detection."""
        self.console.print("\n[bold cyan]VPN/Proxy Detection[/bold cyan]")
        ip = input("Enter IP address: ").strip()
        if ip:
            self.detect_vpn_proxy(ip)
    
    def run_username_search(self) -> None:
        """Run username search."""
        self.console.print("\n[bold cyan]Username Search (Brand Protection)[/bold cyan]")
        username = input("Enter username: ").strip()
        if username:
            self.username_search_branded(username)
    
    def run_breach_check(self) -> None:
        """Run breach check."""
        self.console.print("\n[bold cyan]Email Breach Check[/bold cyan]")
        email = input("Enter email: ").strip()
        if email:
            self.check_email_breaches(email)
    
    def run_phone_lookup(self) -> None:
        """Run phone lookup."""
        self.console.print("\n[bold cyan]Phone Number Analysis[/bold cyan]")
        phone = input("Enter phone number: ").strip()
        if phone:
            self.lookup_phone_number(phone)


def main():
    """Entry point for advanced OSINT tools."""
    tools = AdvancedOSINTTools()
    tools.main()


if __name__ == "__main__":
    main()