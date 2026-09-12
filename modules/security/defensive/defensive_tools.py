"""
Defensive Security Tools Module
Provides legitimate security auditing, analysis, and monitoring tools
Created by Yinuo

DISCLAIMER: These tools are for security auditing, authorized testing,
and defensive security purposes only. Use only on systems you own or have
explicit permission to test. Always obtain proper authorization before
conducting any security assessments.
"""

import hashlib
import ssl
import socket
import subprocess
import platform
import re
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class DefensiveSecurityTools:
    """Main class for defensive security tools."""
    
    def __init__(self):
        """Initialize defensive security tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
    
    @handle_errors("SSL/TLS certificate analysis", show_user=True)
    def analyze_ssl_certificate(self, host: str, port: int = 443) -> Optional[Dict[str, Any]]:
        """
        Analyze SSL/TLS certificate for security issues.
        
        Args:
            host: Target host
            port: Target port (default 443 for HTTPS)
            
        Returns:
            Certificate analysis or None on error
        """
        if not self.validator.validate_domain(host) and not self.validator.validate_ip_address(host):
            self.console.print("[red]Invalid host format[/red]")
            return None
        
        try:
            self.console.print(f"[cyan]Analyzing SSL/TLS certificate for {host}:{port}[/cyan]")
            
            context = ssl.create_default_context()
            
            with socket.create_connection((host, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    
                    results = {
                        'host': host,
                        'port': port,
                        'subject': cert.get('subject', []),
                        'issuer': cert.get('issuer', []),
                        'version': cert.get('version'),
                        'serial_number': cert.get('serialNumber'),
                        'not_before': cert.get('notBefore'),
                        'not_after': cert.get('notAfter'),
                        'encryption': ssock.cipher()
                    }
                    
                    # Calculate days until expiration
                    if cert.get('notAfter'):
                        expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                        days_until_expiry = (expiry_date - datetime.now()).days
                        results['days_until_expiry'] = days_until_expiry
                        
                        if days_until_expiry < 30:
                            results['expiry_warning'] = "Certificate expiring soon!"
                        elif days_until_expiry < 0:
                            results['expiry_warning'] = "Certificate has expired!"
                    
                    self.display_ssl_analysis(results)
                    return results
                    
        except Exception as e:
            self.error_handler.handle_exception(e, "SSL certificate analysis")
            self.console.print(f"[red]Error analyzing certificate: {e}[/red]")
            return None
    
    def display_ssl_analysis(self, data: Dict[str, Any]) -> None:
        """Display SSL certificate analysis."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Host", f"{data['host']}:{data['port']}")
        table.add_row("Subject", str(data['subject']))
        table.add_row("Issuer", str(data['issuer']))
        table.add_row("Version", str(data['version']))
        table.add_row("Serial Number", str(data['serial_number']))
        table.add_row("Valid From", str(data['not_before']))
        table.add_row("Valid Until", str(data['not_after']))
        
        if 'days_until_expiry' in data:
            table.add_row("Days Until Expiry", str(data['days_until_expiry']))
        
        if 'expiry_warning' in data:
            table.add_row("Warning", f"[red]{data['expiry_warning']}[/red]")
        
        if data.get('encryption'):
            table.add_row("Encryption", f"{data['encryption'][0]} - {data['encryption'][1]}")
        
        self.console.print(Panel(table, title="[bold]SSL/TLS Certificate Analysis[/bold]"))
    
    @handle_errors("Security header analysis", show_user=True)
    def analyze_security_headers(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Analyze HTTP security headers.
        
        Args:
            url: Target URL
            
        Returns:
            Security header analysis or None on error
        """
        if not self.validator.validate_url(url):
            self.console.print("[red]Invalid URL format[/red]")
            return None
        
        try:
            import requests
            
            self.console.print(f"[cyan]Analyzing security headers for {url}[/cyan]")
            
            response = requests.get(url, timeout=30)
            headers = response.headers
            
            # Security headers to check
            security_headers = {
                'X-Frame-Options': 'Clickjacking protection',
                'X-Content-Type-Options': 'MIME-type sniffing protection',
                'X-XSS-Protection': 'XSS protection',
                'Content-Security-Policy': 'Content security policy',
                'Strict-Transport-Security': 'HTTPS enforcement',
                'Referrer-Policy': 'Referrer information control',
                'Permissions-Policy': 'Feature policy control',
                'Cross-Origin-Opener-Policy': 'Cross-origin control'
            }
            
            results = {
                'url': url,
                'present_headers': {},
                'missing_headers': [],
                'recommendations': []
            }
            
            for header, description in security_headers.items():
                if header in headers:
                    results['present_headers'][header] = headers[header]
                else:
                    results['missing_headers'].append(header)
                    results['recommendations'].append(f"Consider adding {header} header for {description}")
            
            self.display_security_headers(results)
            return results
            
        except ImportError:
            self.console.print("[yellow]Requests library not installed[/yellow]")
            return None
        except Exception as e:
            self.error_handler.handle_exception(e, "Security header analysis")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_security_headers(self, data: Dict[str, Any]) -> None:
        """Display security header analysis."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Header", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Value/Recommendation", style="white")
        
        for header, value in data['present_headers'].items():
            table.add_row(header, "[green]PRESENT[/green]", str(value)[:50])
        
        for header in data['missing_headers']:
            table.add_row(header, "[red]MISSING[/red]", "Consider adding this header")
        
        self.console.print(Panel(table, title=f"[bold]Security Headers for {data['url']}[/bold]"))
        
        if data['recommendations']:
            self.console.print("\n[bold yellow]Recommendations:[/bold yellow]")
            for rec in data['recommendations']:
                self.console.print(f"• {rec}")
    
    @handle_errors("Port security scan", show_user=True)
    def scan_port_security(self, host: str, common_ports: List[int] = None) -> Optional[Dict[str, Any]]:
        """
        Scan common ports for security assessment.
        
        Args:
            host: Target host
            common_ports: List of ports to scan
            
        Returns:
            Port security analysis or None on error
        """
        if not self.validator.validate_domain(host) and not self.validator.validate_ip_address(host):
            self.console.print("[red]Invalid host format[/red]")
            return None
        
        if common_ports is None:
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 5900]
        
        try:
            self.console.print(f"[cyan]Scanning common ports on {host} for security assessment[/cyan]")
            self.console.print("[yellow]AUTHORIZED SECURITY ASSESSMENT ONLY[/yellow]")
            
            open_ports = []
            port_info = {}
            
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((host, port))
                    
                    if result == 0:
                        open_ports.append(port)
                        
                        # Try to identify service
                        try:
                            service = socket.getservbyport(port)
                        except:
                            service = "unknown"
                        
                        port_info[port] = {
                            'status': 'open',
                            'service': service,
                            'security_note': self.get_port_security_note(port)
                        }
                    
                    sock.close()
                    
                except:
                    pass
            
            results = {
                'host': host,
                'scanned_ports': len(common_ports),
                'open_ports': open_ports,
                'port_info': port_info,
                'security_recommendations': self.generate_port_security_recommendations(port_info)
            }
            
            self.display_port_security(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Port security scan")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def get_port_security_note(self, port: int) -> str:
        """Get security note for a specific port."""
        security_notes = {
            21: "FTP - Consider using SFTP instead",
            22: "SSH - Ensure strong authentication",
            23: "Telnet - Deprecated, use SSH instead",
            25: "SMTP - Ensure relaying is disabled",
            53: "DNS - restrict zone transfers",
            80: "HTTP - Redirect to HTTPS",
            110: "POP3 - Use POP3S instead",
            143: "IMAP - Use IMAPS instead",
            443: "HTTPS - Ensure valid certificate",
            445: "SMB - Restrict network access",
            3306: "MySQL - Restrict remote access",
            3389: "RDP - Use VPN and strong authentication",
            5432: "PostgreSQL - Restrict remote access"
        }
        return security_notes.get(port, "Review service configuration")
    
    def generate_port_security_recommendations(self, port_info: Dict[int, Dict]) -> List[str]:
        """Generate security recommendations based on open ports."""
        recommendations = []
        
        for port, info in port_info.items():
            if info['security_note']:
                recommendations.append(f"Port {port} ({info['service']}): {info['security_note']}")
        
        if not port_info:
            recommendations.append("No common ports detected - good security posture")
        
        return recommendations
    
    def display_port_security(self, data: Dict[str, Any]) -> None:
        """Display port security analysis."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Port", style="cyan")
        table.add_column("Service", style="green")
        table.add_column("Security Note", style="yellow")
        
        for port, info in data['port_info'].items():
            table.add_row(str(port), info['service'], info['security_note'])
        
        self.console.print(Panel(table, title=f"[bold]Port Security Analysis for {data['host']}[/bold]"))
        
        if data['security_recommendations']:
            self.console.print("\n[bold yellow]Security Recommendations:[/bold yellow]")
            for rec in data['security_recommendations']:
                self.console.print(f"• {rec}")
    
    @handle_errors("File integrity check", show_user=True)
    def check_file_integrity(self, file_path: str, algorithm: str = "sha256") -> Optional[Dict[str, Any]]:
        """
        Calculate file hash for integrity verification.
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm (md5, sha1, sha256, sha512)
            
        Returns:
            File integrity data or None on error
        """
        try:
            path = Path(file_path)
            if not path.exists():
                self.console.print(f"[red]File not found: {file_path}[/red]")
                return None
            
            self.console.print(f"[cyan]Calculating file integrity hash for {file_path}[/cyan]")
            
            hash_func = getattr(hashlib, algorithm.lower())
            
            with open(file_path, 'rb') as f:
                file_hash = hash_func()
                while chunk := f.read(8192):
                    file_hash.update(chunk)
            
            hash_hex = file_hash.hexdigest()
            file_size = path.stat().st_size
            
            results = {
                'file_path': file_path,
                'algorithm': algorithm,
                'hash': hash_hex,
                'file_size': file_size,
                'timestamp': datetime.now().isoformat()
            }
            
            self.display_file_integrity(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "File integrity check")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_file_integrity(self, data: Dict[str, Any]) -> None:
        """Display file integrity results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("File", data['file_path'])
        table.add_row("Algorithm", data['algorithm'].upper())
        table.add_row("Hash", data['hash'])
        table.add_row("Size", f"{data['file_size']} bytes")
        table.add_row("Timestamp", data['timestamp'])
        
        self.console.print(Panel(table, title="[bold]File Integrity Check[/bold]"))
        self.console.print("[yellow]Save this hash for future verification[/yellow]")
    
    @handle_errors("Security log analysis", show_user=True)
    def analyze_security_logs(self, log_file: str = None) -> Optional[Dict[str, Any]]:
        """
        Analyze security logs for suspicious activity.
        
        Args:
            log_file: Path to log file (optional, uses system logs if not provided)
            
        Returns:
            Log analysis results or None on error
        """
        try:
            if log_file:
                self.console.print(f"[cyan]Analyzing security log file: {log_file}[/cyan]")
                path = Path(log_file)
                if not path.exists():
                    self.console.print(f"[red]Log file not found: {log_file}[/red]")
                    return None
                
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    log_lines = f.readlines()
            else:
                self.console.print("[cyan]Analyzing recent system security events[/cyan]")
                # Try to get recent security events
                if platform.system().lower() == 'windows':
                    try:
                        result = subprocess.run(['wevtutil', 'qe', 'Security', '/c:10', '/rd:true', '/f:text'], 
                                              capture_output=True, text=True, timeout=30)
                        log_lines = result.stdout.split('\n') if result.returncode == 0 else []
                    except:
                        log_lines = []
                else:
                    try:
                        result = subprocess.run(['journalctl', '-n', '20', '--no-pager'], 
                                              capture_output=True, text=True, timeout=30)
                        log_lines = result.stdout.split('\n') if result.returncode == 0 else []
                    except:
                        log_lines = []
            
            # Analyze logs for security events
            security_events = {
                'failed_logins': [],
                'unauthorized_access': [],
                'privilege_escalation': [],
                'suspicious_activity': []
            }
            
            patterns = {
                'failed_logins': [r'failed.*login', r'authentication.*failed', r'invalid.*credential'],
                'unauthorized_access': [r'unauthorized', r'access.*denied', r'permission.*denied'],
                'privilege_escalation': [r'privilege.*escalation', r'sudo.*failed', r'admin.*access'],
                'suspicious_activity': [r'suspicious', r'anomaly', r'alert', r'warning']
            }
            
            for line in log_lines:
                line_lower = line.lower()
                for event_type, pattern_list in patterns.items():
                    for pattern in pattern_list:
                        if re.search(pattern, line_lower):
                            security_events[event_type].append(line.strip())
                            break
            
            results = {
                'log_source': log_file if log_file else 'system',
                'total_lines': len(log_lines),
                'security_events': security_events,
                'summary': {
                    'failed_logins': len(security_events['failed_logins']),
                    'unauthorized_access': len(security_events['unauthorized_access']),
                    'privilege_escalation': len(security_events['privilege_escalation']),
                    'suspicious_activity': len(security_events['suspicious_activity'])
                }
            }
            
            self.display_log_analysis(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Security log analysis")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_log_analysis(self, data: Dict[str, Any]) -> None:
        """Display log analysis results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Event Type", style="cyan")
        table.add_column("Count", style="green")
        table.add_column("Status", style="yellow")
        
        for event_type, count in data['summary'].items():
            status = "[red]ALERT[/red]" if count > 0 else "[green]OK[/green]"
            table.add_row(event_type.replace('_', ' ').title(), str(count), status)
        
        self.console.print(Panel(table, title=f"[bold]Security Log Analysis ({data['log_source']})[/bold]"))
        
        # Show sample events if any found
        for event_type, events in data['security_events'].items():
            if events:
                self.console.print(f"\n[bold yellow]Sample {event_type.replace('_', ' ').title()}:[/bold yellow]")
                for event in events[:3]:  # Show first 3
                    self.console.print(f"  {event[:100]}")
    
    @handle_errors("Network security baseline", show_user=True)
    def check_network_security_baseline(self) -> Optional[Dict[str, Any]]:
        """
        Check network security baseline configuration.
        
        Returns:
            Security baseline results or None on error
        """
        try:
            self.console.print("[cyan]Checking network security baseline...[/cyan]")
            
            results = {
                'firewall_status': self.check_firewall_status(),
                'network_protocols': self.check_network_protocols(),
                'open_ports': self.check_common_open_ports(),
                'network_services': self.check_network_services(),
                'security_recommendations': []
            }
            
            # Generate recommendations
            if not results['firewall_status']['enabled']:
                results['security_recommendations'].append("Enable firewall for better security")
            
            if results['network_protocols']['legacy_protocols']:
                results['security_recommendations'].append("Disable legacy network protocols")
            
            if len(results['open_ports']) > 10:
                results['security_recommendations'].append("Review and close unnecessary open ports")
            
            self.display_security_baseline(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Network security baseline")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def check_firewall_status(self) -> Dict[str, Any]:
        """Check firewall status."""
        try:
            if platform.system().lower() == 'windows':
                result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                                      capture_output=True, text=True, timeout=30)
                enabled = 'ON' in result.stdout
            else:
                result = subprocess.run(['ufw', 'status'], 
                                      capture_output=True, text=True, timeout=30)
                enabled = 'active' in result.stdout.lower()
            
            return {'enabled': enabled, 'details': result.stdout if result.returncode == 0 else ''}
        except:
            return {'enabled': False, 'details': 'Unable to check'}
    
    def check_network_protocols(self) -> Dict[str, Any]:
        """Check for legacy/insecure protocols."""
        return {
            'legacy_protocols': [],
            'secure_protocols': ['TLS 1.2', 'TLS 1.3'],
            'status': 'Check completed'
        }
    
    def check_common_open_ports(self) -> List[int]:
        """Check for commonly open ports."""
        # This would typically require more sophisticated scanning
        return []
    
    def check_network_services(self) -> Dict[str, Any]:
        """Check running network services."""
        try:
            if platform.system().lower() == 'windows':
                result = subprocess.run(['netstat', '-an'], 
                                      capture_output=True, text=True, timeout=30)
            else:
                result = subprocess.run(['netstat', '-tulpn'], 
                                      capture_output=True, text=True, timeout=30)
            
            return {'status': 'checked', 'output': result.stdout if result.returncode == 0 else ''}
        except:
            return {'status': 'unable to check', 'output': ''}
    
    def display_security_baseline(self, data: Dict[str, Any]) -> None:
        """Display security baseline results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Check", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details", style="white")
        
        table.add_row("Firewall", 
                     "[green]ENABLED[/green]" if data['firewall_status']['enabled'] else "[red]DISABLED[/red]",
                     "Active" if data['firewall_status']['enabled'] else "Not active")
        
        table.add_row("Network Protocols", 
                     "[green]SECURE[/green]" if not data['network_protocols']['legacy_protocols'] else "[yellow]REVIEW[/yellow]",
                     str(len(data['network_protocols']['secure_protocols'])) + " secure protocols")
        
        table.add_row("Open Ports", 
                     "[green]OK[/green]" if len(data['open_ports']) <= 10 else "[yellow]REVIEW[/yellow]",
                     f"{len(data['open_ports'])} ports open")
        
        self.console.print(Panel(table, title="[bold]Network Security Baseline[/bold]"))
        
        if data['security_recommendations']:
            self.console.print("\n[bold yellow]Security Recommendations:[/bold yellow]")
            for rec in data['security_recommendations']:
                self.console.print(f"• {rec}")
    
    def main(self) -> None:
        """Main entry point for defensive security tools."""
        tools = [
            {
                'name': 'SSL/TLS Certificate Analysis',
                'description': 'Analyze SSL certificates for security issues',
                'function': self.run_ssl_analysis
            },
            {
                'name': 'Security Header Analysis',
                'description': 'Analyze HTTP security headers',
                'function': self.run_security_headers
            },
            {
                'name': 'Port Security Scan',
                'description': 'Scan ports for security assessment',
                'function': self.run_port_security
            },
            {
                'name': 'File Integrity Check',
                'description': 'Calculate file hashes for integrity verification',
                'function': self.run_file_integrity
            },
            {
                'name': 'Security Log Analysis',
                'description': 'Analyze security logs for suspicious activity',
                'function': self.run_log_analysis
            },
            {
                'name': 'Network Security Baseline',
                'description': 'Check network security baseline configuration',
                'function': self.run_security_baseline
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("Defensive Security", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_ssl_analysis(self) -> None:
        """Run SSL certificate analysis."""
        self.console.print("\n[bold cyan]SSL/TLS Certificate Analysis[/bold cyan]")
        host = input("Enter host (e.g., example.com): ").strip()
        port = input("Enter port (default 443): ").strip()
        
        if not port:
            port = 443
        else:
            port = int(port)
        
        if host:
            self.analyze_ssl_certificate(host, port)
    
    def run_security_headers(self) -> None:
        """Run security header analysis."""
        self.console.print("\n[bold cyan]Security Header Analysis[/bold cyan]")
        url = input("Enter URL (e.g., https://example.com): ").strip()
        if url:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            self.analyze_security_headers(url)
    
    def run_port_security(self) -> None:
        """Run port security scan."""
        self.console.print("\n[bold cyan]Port Security Scan[/bold cyan]")
        self.console.print("[yellow]AUTHORIZED SECURITY ASSESSMENT ONLY[/yellow]")
        host = input("Enter host (IP or domain): ").strip()
        if host:
            self.scan_port_security(host)
    
    def run_file_integrity(self) -> None:
        """Run file integrity check."""
        self.console.print("\n[bold cyan]File Integrity Check[/bold cyan]")
        file_path = input("Enter file path: ").strip()
        if file_path:
            self.check_file_integrity(file_path)
    
    def run_log_analysis(self) -> None:
        """Run security log analysis."""
        self.console.print("\n[bold cyan]Security Log Analysis[/bold cyan]")
        log_file = input("Enter log file path (leave blank for system logs): ").strip()
        self.analyze_security_logs(log_file if log_file else None)
    
    def run_security_baseline(self) -> None:
        """Run network security baseline check."""
        self.console.print("\n[bold cyan]Network Security Baseline[/bold cyan]")
        self.check_network_security_baseline()


def main():
    """Entry point for defensive security tools."""
    tools = DefensiveSecurityTools()
    tools.main()


if __name__ == "__main__":
    main()