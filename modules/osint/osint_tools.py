"""
OSINT & Research Tools Module
Provides public-data lookups and open-source intelligence tools
"""

import requests
import json
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class OSINTTools:
    """Main class for OSINT and research tools."""
    
    def __init__(self):
        """Initialize OSINT tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        # API endpoints (public/free APIs)
        self.apis = {
            'ipinfo': 'https://ipinfo.io/{}/json',
            'virustotal': 'https://www.virustotal.com/vtapi/v2/ip-address/report',
            'shodan': 'https://api.shodan.io/shodan/host/{}',
            'haveibeenpwned': 'https://haveibeenpwned.com/api/v3/breachedaccount/{}',
            'github': 'https://api.github.com/users/{}',
            'emailrep': 'https://emailrep.io/query/{}'
        }
    
    @handle_errors("Email reputation lookup", show_user=True)
    def check_email_reputation(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Check email reputation using EmailRep.io API.
        
        Args:
            email: Email address to check
            
        Returns:
            Reputation data or None on error
        """
        if not self.validator.validate_email(email):
            self.console.print("[red]Invalid email format[/red]")
            return None
        
        try:
            url = self.apis['emailrep'].format(email)
            headers = {'User-Agent': 'TerminalMultiTool/1.0'}
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.display_email_reputation(data)
                return data
            else:
                self.console.print(f"[yellow]API returned status {response.status_code}[/yellow]")
                return None
                
        except requests.RequestException as e:
            self.error_handler.handle_network_error(e, url)
            self.console.print("[red]Network error occurred[/red]")
            return None
    
    def display_email_reputation(self, data: Dict[str, Any]) -> None:
        """Display email reputation results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Email", data.get('email', 'N/A'))
        table.add_row("Reputation", str(data.get('reputation', 'N/A')))
        table.add_row("Suspicious", str(data.get('suspicious', False)))
        table.add_row("References", str(data.get('references', 0)))
        table.add_row("Details", str(data.get('details', []))[:100])
        
        self.console.print(Panel(table, title="[bold]Email Reputation[/bold]"))
    
    @handle_errors("GitHub user lookup", show_user=True)
    def lookup_github_user(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Lookup GitHub user information.
        
        Args:
            username: GitHub username
            
        Returns:
            User data or None on error
        """
        if not self.validator.validate_username(username):
            self.console.print("[red]Invalid username format[/red]")
            return None
        
        try:
            url = self.apis['github'].format(username)
            headers = {'User-Agent': 'TerminalMultiTool/1.0'}
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.display_github_user(data)
                return data
            elif response.status_code == 404:
                self.console.print("[yellow]User not found[/yellow]")
                return None
            else:
                self.console.print(f"[yellow]API returned status {response.status_code}[/yellow]")
                return None
                
        except requests.RequestException as e:
            self.error_handler.handle_network_error(e, url)
            self.console.print("[red]Network error occurred[/red]")
            return None
    
    def display_github_user(self, data: Dict[str, Any]) -> None:
        """Display GitHub user information."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Username", data.get('login', 'N/A'))
        table.add_row("Name", data.get('name', 'N/A'))
        table.add_row("Bio", str(data.get('bio', 'N/A'))[:50])
        table.add_row("Public Repos", str(data.get('public_repos', 0)))
        table.add_row("Followers", str(data.get('followers', 0)))
        table.add_row("Following", str(data.get('following', 0)))
        table.add_row("Location", data.get('location', 'N/A'))
        table.add_row("Company", data.get('company', 'N/A'))
        
        self.console.print(Panel(table, title="[bold]GitHub User Info[/bold]"))
    
    @handle_errors("Domain research", show_user=True)
    def research_domain(self, domain: str) -> Optional[Dict[str, Any]]:
        """
        Perform basic domain research.
        
        Args:
            domain: Domain name to research
            
        Returns:
            Domain information or None on error
        """
        if not self.validator.validate_domain(domain):
            self.console.print("[red]Invalid domain format[/red]")
            return None
        
        try:
            # Basic DNS lookup using DNS Python
            import dns.resolver
            
            results = {'domain': domain}
            
            # Try to get A records
            try:
                a_records = dns.resolver.resolve(domain, 'A')
                results['a_records'] = [str(r) for r in a_records]
            except:
                results['a_records'] = []
            
            # Try to get MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                results['mx_records'] = [str(r) for r in mx_records]
            except:
                results['mx_records'] = []
            
            # Try to get TXT records
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                results['txt_records'] = [str(r) for r in txt_records]
            except:
                results['txt_records'] = []
            
            self.display_domain_info(results)
            return results
            
        except ImportError:
            self.console.print("[yellow]DNS Python not installed. Install with: pip install dnspython[/yellow]")
            return None
        except Exception as e:
            self.error_handler.handle_exception(e, "Domain research")
            self.console.print(f"[red]Error researching domain: {e}[/red]")
            return None
    
    def display_domain_info(self, data: Dict[str, Any]) -> None:
        """Display domain research results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Record Type", style="cyan")
        table.add_column("Records", style="green")
        
        table.add_row("Domain", data.get('domain', 'N/A'))
        table.add_row("A Records", ', '.join(data.get('a_records', [])[:3]))
        table.add_row("MX Records", ', '.join(data.get('mx_records', [])[:3]))
        table.add_row("TXT Records", ', '.join(data.get('txt_records', [])[:2]))
        
        self.console.print(Panel(table, title="[bold]Domain Information[/bold]"))
    
    @handle_errors("Username search", show_user=True)
    def search_username(self, username: str) -> Optional[List[str]]:
        """
        Search for username across multiple platforms.
        
        Args:
            username: Username to search for
            
        Returns:
            List of found platforms or None on error
        """
        if not self.validator.validate_username(username):
            self.console.print("[red]Invalid username format[/red]")
            return None
        
        # Common platforms to check
        platforms = [
            ('GitHub', f'https://github.com/{username}'),
            ('Twitter', f'https://twitter.com/{username}'),
            ('Reddit', f'https://reddit.com/user/{username}'),
            ('Instagram', f'https://instagram.com/{username}'),
            ('YouTube', f'https://youtube.com/@{username}'),
        ]
        
        found = []
        
        for platform, url in platforms:
            try:
                response = requests.head(url, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    found.append(platform)
                    self.console.print(f"[green]✓[/green] {platform}: {url}")
                else:
                    self.console.print(f"[red]✗[/red] {platform}: Not found")
            except:
                self.console.print(f"[yellow]?[/yellow] {platform}: Unable to check")
        
        if found:
            self.console.print(f"\n[green]Found username on {len(found)} platform(s)[/green]")
        else:
            self.console.print("[yellow]Username not found on checked platforms[/yellow]")
        
        return found
    
    def main(self) -> None:
        """Main entry point for OSINT tools module."""
        tools = [
            {
                'name': 'Email Reputation Check',
                'description': 'Check email reputation using EmailRep.io',
                'function': self.run_email_reputation
            },
            {
                'name': 'GitHub User Lookup',
                'description': 'Lookup GitHub user information',
                'function': self.run_github_lookup
            },
            {
                'name': 'Domain Research',
                'description': 'Basic domain DNS research',
                'function': self.run_domain_research
            },
            {
                'name': 'Username Search',
                'description': 'Search username across platforms',
                'function': self.run_username_search
            },
            {
                'name': 'Advanced OSINT Tools',
                'description': 'VPN detection, breach checks, more',
                'function': self.run_advanced_tools
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("OSINT & Research", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_email_reputation(self) -> None:
        """Run email reputation check."""
        self.console.print("\n[bold cyan]Email Reputation Check[/bold cyan]")
        email = input("Enter email address: ").strip()
        if email:
            self.check_email_reputation(email)
    
    def run_github_lookup(self) -> None:
        """Run GitHub user lookup."""
        self.console.print("\n[bold cyan]GitHub User Lookup[/bold cyan]")
        username = input("Enter GitHub username: ").strip()
        if username:
            self.lookup_github_user(username)
    
    def run_domain_research(self) -> None:
        """Run domain research."""
        self.console.print("\n[bold cyan]Domain Research[/bold cyan]")
        domain = input("Enter domain (e.g., example.com): ").strip()
        if domain:
            self.research_domain(domain)
    
    def run_username_search(self) -> None:
        """Run username search."""
        self.console.print("\n[bold cyan]Username Search[/bold cyan]")
        username = input("Enter username: ").strip()
        if username:
            self.search_username(username)
    
    def run_advanced_tools(self) -> None:
        """Run advanced OSINT tools."""
        self.console.print("\n[bold cyan]Advanced OSINT Tools[/bold cyan]")
        from .advanced_tools import AdvancedOSINTTools
        advanced = AdvancedOSINTTools()
        advanced.main()


def main():
    """Entry point for OSINT module."""
    osint = OSINTTools()
    osint.main()


if __name__ == "__main__":
    main()