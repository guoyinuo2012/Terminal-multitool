"""
Resources Module
Provides curated public OSINT and research bookmarks
"""

from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class ResourceLinks:
    """Main class for resource links and bookmarks."""
    
    def __init__(self):
        """Initialize resource links."""
        self.logger = setup_logger()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        # Curated resource categories
        self.resources = {
            'osint_tools': {
                'name': 'OSINT Tools',
                'description': 'Open-source intelligence gathering tools',
                'links': [
                    {'name': 'Maltego', 'url': 'https://www.maltego.com', 'description': 'Visual link analysis tool'},
                    {'name': 'Shodan', 'url': 'https://www.shodan.io', 'description': 'Internet-connected device search'},
                    {'name': 'Censys', 'url': 'https://censys.io', 'description': 'Internet-wide scanning and search'},
                    {'name': 'SpiderFoot', 'url': 'https://www.spiderfoot.net', 'description': 'OSINT automation tool'},
                    {'name': 'theHarvester', 'url': 'https://github.com/laramies/theHarvester', 'description': 'Email, subdomain, and people harvesting'},
                    {'name': 'Recon-ng', 'url': 'https://github.com/lanmaster53/recon-ng', 'description': 'Web reconnaissance framework'},
                ]
            },
            'social_media': {
                'name': 'Social Media Intelligence',
                'description': 'Social media investigation tools',
                'links': [
                    {'name': 'Sherlock', 'url': 'https://github.com/sherlock-project/sherlock', 'description': 'Username search across social networks'},
                    {'name': 'Social-Analyzer', 'url': 'https://github.com/qeeqbox/social-analyzer', 'description': 'Social media analysis framework'},
                    {'name': 'Namechk', 'url': 'https://namechk.com', 'description': 'Username availability checker'},
                    {'name': 'KnowEm', 'url': 'https://knowem.com', 'description': 'Username and brand search'},
                ]
            },
            'domain_dns': {
                'name': 'Domain & DNS Tools',
                'description': 'Domain research and DNS investigation',
                'links': [
                    {'name': 'DNS Dumpster', 'url': 'https://dnsdumpster.com', 'description': 'DNS reconnaissance and mapping'},
                    {'name': 'VirusTotal', 'url': 'https://www.virustotal.com', 'description': 'File and URL analysis'},
                    {'name': 'SecurityTrails', 'url': 'https://securitytrails.com', 'description': 'Domain and DNS intelligence'},
                    {'name': 'WhoisXML API', 'url': 'https://whoisxmlapi.com', 'description': 'WHOIS and domain data'},
                    {'name': 'DomainTools', 'url': 'https://www.domaintools.com', 'description': 'Domain research and intelligence'},
                ]
            },
            'geolocation': {
                'name': 'Geolocation & IP Tools',
                'description': 'IP geolocation and mapping tools',
                'links': [
                    {'name': 'IPInfo', 'url': 'https://ipinfo.io', 'description': 'IP geolocation and intelligence'},
                    {'name': 'GeoIPTool', 'url': 'https://www.geoiptool.com', 'description': 'IP geolocation lookup'},
                    {'name': 'MaxMind GeoIP', 'url': 'https://www.maxmind.com', 'description': 'Geolocation database and API'},
                    {'name': 'IP-API', 'url': 'http://ip-api.com', 'description': 'IP geolocation API'},
                ]
            },
            'search_engines': {
                'name': 'Specialized Search Engines',
                'description': 'Alternative search engines for research',
                'links': [
                    {'name': 'Google Dorks', 'url': 'https://www.google.com/advanced_search', 'description': 'Advanced Google search techniques'},
                    {'name': 'DuckDuckGo', 'url': 'https://duckduckgo.com', 'description': 'Privacy-focused search engine'},
                    {'name': 'Bing Advanced Search', 'url': 'https://www.bing.com/search', 'description': 'Microsoft search with advanced features'},
                    {'name': 'Yandex', 'url': 'https://yandex.com', 'description': 'Russian search engine, useful for regional searches'},
                ]
            },
            'data_breach': {
                'name': 'Data Breach & Leaks',
                'description': 'Data breach and credential leak resources',
                'links': [
                    {'name': 'Have I Been Pwned', 'url': 'https://haveibeenpwned.com', 'description': 'Check if email is in data breaches'},
                    {'name': 'Breach Directory', 'url': 'https://breachdirectory.org', 'description': 'Search exposed data breaches'},
                    {'name': 'DeHashed', 'url': 'https://dehashed.com', 'description': 'Breach database search'},
                    {'name': 'IntelX', 'url': 'https://intelx.io', 'description': 'Data leak search engine'},
                ]
            },
            'email_research': {
                'name': 'Email Research',
                'description': 'Email investigation and validation tools',
                'links': [
                    {'name': 'EmailRep', 'url': 'https://emailrep.io', 'description': 'Email reputation investigation'},
                    {'name': 'Hunter.io', 'url': 'https://hunter.io', 'description': 'Email finder and verifier'},
                    {'name': 'VoilaNorbert', 'url': 'https://www.voilanorbert.com', 'description': 'Email finder for professionals'},
                    {'name': 'MailTester', 'url': 'https://mailtester.com', 'description': 'Email address validation'},
                ]
            },
            'public_records': {
                'name': 'Public Records',
                'description': 'Public record and government databases',
                'links': [
                    {'name': 'SEC EDGAR', 'url': 'https://www.sec.gov/edgar', 'description': 'SEC company filings and reports'},
                    {'name': 'CourtListener', 'url': 'https://www.courtlistener.com', 'description': 'US court case search'},
                    {'name': 'USA.gov', 'url': 'https://www.usa.gov', 'description': 'Official US government information'},
                    {'name': 'NMLS Consumer Access', 'url': 'https://nmlsconsumeraccess.org', 'description': 'Financial professional search'},
                ]
            },
            'image_research': {
                'name': 'Image & Video Research',
                'description': 'Image forensics and reverse image search',
                'links': [
                    {'name': 'Google Images', 'url': 'https://images.google.com', 'description': 'Reverse image search'},
                    {'name': 'TinEye', 'url': 'https://tineye.com', 'description': 'Reverse image search engine'},
                    {'name': 'Yandex Images', 'url': 'https://yandex.com/images', 'description': 'Russian image search'},
                    {'name': 'InVID', 'url': 'https://www.invid-project.eu', 'description': 'Video verification tool'},
                ]
            },
            'github_research': {
                'name': 'GitHub & Code Research',
                'description': 'Source code and repository research',
                'links': [
                    {'name': 'GitHub Advanced Search', 'url': 'https://github.com/search/advanced', 'description': 'Advanced GitHub code search'},
                    {'name': 'GitLab', 'url': 'https://gitlab.com', 'description': 'Git repository hosting'},
                    {'name': 'GHTorrent', 'url': 'https://ghtorrent.org', 'description': 'GitHub research dataset'},
                    {'name': 'Sourcegraph', 'url': 'https://sourcegraph.com', 'description': 'Code search and intelligence'},
                ]
            },
            'learning_resources': {
                'name': 'Learning Resources',
                'description': 'Educational resources and tutorials',
                'links': [
                    {'name': 'OSINT Framework', 'url': 'https://osintframework.com', 'description': 'Comprehensive OSINT tool directory'},
                    {'name': 'Bellingcat', 'url': 'https://www.bellingcat.com', 'description': 'Online investigation resources'},
                    {'name': 'CyberChef', 'url': 'https://gchq.github.io/CyberChef', 'description': 'Web-based data conversion tool'},
                    {'name': 'SANS OSINT', 'url': 'https://www.sans.org', 'description': 'Security training and resources'},
                ]
            },
            'api_directories': {
                'name': 'API Directories',
                'description': 'Public API directories and documentation',
                'links': [
                    {'name': 'Public APIs', 'url': 'https://publicapis.dev', 'description': 'Directory of public APIs'},
                    {'name': 'RapidAPI', 'url': 'https://rapidapi.com', 'description': 'API marketplace and directory'},
                    {'name': 'API List', 'url': 'https://apilist.fun', 'description': 'Curated API directory'},
                    {'name': 'ProgrammableWeb', 'url': 'https://www.programmableweb.com', 'description': 'API directory and news'},
                ]
            }
        }
    
    @handle_errors("Display resources", show_user=True)
    def display_category(self, category_key: str) -> None:
        """
        Display resources for a specific category.
        
        Args:
            category_key: Key of the category to display
        """
        if category_key not in self.resources:
            self.console.print(f"[red]Category '{category_key}' not found[/red]")
            return
        
        category = self.resources[category_key]
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Tool/Service", style="cyan")
        table.add_column("URL", style="green")
        table.add_column("Description", style="white")
        
        for link in category['links']:
            table.add_row(
                link['name'],
                link['url'],
                link['description']
            )
        
        self.console.print(Panel(table, title=f"[bold]{category['name']}[/bold]", subtitle=category['description']))
    
    @handle_errors("List all categories", show_user=True)
    def list_all_categories(self) -> None:
        """Display all resource categories."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan")
        table.add_column("Category", style="green")
        table.add_column("Description", style="white")
        table.add_column("Links", style="yellow")
        
        for i, (key, category) in enumerate(self.resources.items(), 1):
            table.add_row(
                str(i),
                category['name'],
                category['description'],
                str(len(category['links']))
            )
        
        self.console.print(Panel(table, title="[bold]Resource Categories[/bold]"))
    
    @handle_errors("Search resources", show_user=True)
    def search_resources(self, query: str) -> None:
        """
        Search resources by name or description.
        
        Args:
            query: Search query
        """
        query = query.lower()
        results = []
        
        for category_key, category in self.resources.items():
            for link in category['links']:
                if (query in link['name'].lower() or 
                    query in link['description'].lower() or
                    query in link['url'].lower()):
                    results.append({
                        'category': category['name'],
                        'link': link
                    })
        
        if results:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Category", style="cyan")
            table.add_column("Tool/Service", style="green")
            table.add_column("URL", style="white")
            table.add_column("Description", style="yellow")
            
            for result in results:
                table.add_row(
                    result['category'],
                    result['link']['name'],
                    result['link']['url'],
                    result['link']['description']
                )
            
            self.console.print(Panel(table, title=f"[bold]Search Results for '{query}'[/bold]"))
        else:
            self.console.print(f"[yellow]No results found for '{query}'[/yellow]")
    
    @handle_errors("Display disclaimer", show_user=True)
    def display_disclaimer(self) -> None:
        """Display legal and ethical use disclaimer."""
        disclaimer = """
        [bold yellow]LEGAL AND ETHICAL USE DISCLAIMER[/bold yellow]
        
        The resources and tools provided in this application are intended for:
        - Educational purposes only
        - Authorized security research
        - Systems you own or have explicit permission to test
        - Legitimate business intelligence gathering
        
        [red]Unauthorized use of these tools may be illegal and unethical.[/red]
        
        Always:
        - Obtain proper authorization before conducting any research
        - Respect privacy laws and regulations
        - Follow applicable terms of service for all platforms
        - Report vulnerabilities responsibly
        - Use your skills for constructive purposes
        
        The developers of this application are not responsible for misuse
        of these resources or any consequences resulting from such misuse.
        """
        
        self.console.print(Panel(disclaimer, title="[bold]IMPORTANT DISCLAIMER[/bold]", border_style="red"))
    
    def main(self) -> None:
        """Main entry point for resources module."""
        tools = [
            {
                'name': 'List All Categories',
                'description': 'Show all resource categories',
                'function': self.run_list_categories
            },
            {
                'name': 'Browse Category',
                'description': 'Browse resources in a specific category',
                'function': self.run_browse_category
            },
            {
                'name': 'Search Resources',
                'description': 'Search resources by name or description',
                'function': self.run_search
            },
            {
                'name': 'Display Disclaimer',
                'description': 'Show legal and ethical use disclaimer',
                'function': self.run_disclaimer
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("Resource Links", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_list_categories(self) -> None:
        """Run list categories."""
        self.list_all_categories()
    
    def run_browse_category(self) -> None:
        """Run browse category."""
        self.list_all_categories()
        
        category_keys = list(self.resources.keys())
        self.console.print("\n[bold cyan]Enter category number to browse (or 0 to go back):[/bold cyan]")
        
        try:
            choice = input().strip()
            if choice == '0':
                return
            
            choice_int = int(choice) - 1
            if 0 <= choice_int < len(category_keys):
                self.display_category(category_keys[choice_int])
            else:
                self.console.print("[red]Invalid category number[/red]")
        except ValueError:
            self.console.print("[red]Invalid input[/red]")
    
    def run_search(self) -> None:
        """Run search."""
        self.console.print("\n[bold cyan]Search Resources[/bold cyan]")
        query = input("Enter search query: ").strip()
        if query:
            self.search_resources(query)
    
    def run_disclaimer(self) -> None:
        """Run disclaimer."""
        self.display_disclaimer()


def main():
    """Entry point for resources module."""
    resources = ResourceLinks()
    resources.main()


if __name__ == "__main__":
    main()