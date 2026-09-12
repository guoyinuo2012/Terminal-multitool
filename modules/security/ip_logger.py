"""
IP Logger Module
Provides legitimate IP logging for security monitoring and analytics
Created by Yinuo

DISCLAIMER: This tool is for legitimate security monitoring, analytics,
and system administration only. Use in compliance with privacy laws and
regulations. Obtain proper consent where required. Do not use for stalking,
harassment, or malicious tracking.
"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class IPLogger:
    """Legitimate IP logger for security monitoring and analytics."""
    
    def __init__(self, db_path: str = None):
        """
        Initialize IP logger.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        # Set database path
        if db_path:
            self.db_path = db_path
        else:
            # Default to logs directory
            logs_dir = Path(__file__).parent.parent.parent / "logs"
            logs_dir.mkdir(exist_ok=True)
            self.db_path = logs_dir / "ip_logs.db"
        
        # Initialize database
        self.init_database()
    
    def init_database(self) -> None:
        """Initialize SQLite database for IP logging."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create IP logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ip_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_agent TEXT,
                    request_method TEXT,
                    request_path TEXT,
                    status_code INTEGER,
                    referer TEXT,
                    purpose TEXT,
                    notes TEXT
                )
            ''')
            
            # Create index for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_ip_address 
                ON ip_logs(ip_address)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON ip_logs(timestamp)
            ''')
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"IP logger database initialized: {self.db_path}")
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Database initialization")
            self.console.print(f"[red]Error initializing database: {e}[/red]")
    
    @handle_errors("Log IP address", show_user=True)
    def log_ip(self, ip_address: str, user_agent: str = None, request_method: str = "GET",
               request_path: str = "/", status_code: int = 200, referer: str = None,
               purpose: str = "monitoring", notes: str = None) -> bool:
        """
        Log an IP address with associated information.
        
        Args:
            ip_address: IP address to log
            user_agent: User agent string
            request_method: HTTP method (GET, POST, etc.)
            request_path: Request path/endpoint
            status_code: HTTP status code
            referer: HTTP referer
            purpose: Purpose of logging (monitoring, analytics, security, etc.)
            notes: Additional notes
            
        Returns:
            True if successful, False otherwise
        """
        if not self.validator.validate_ip_address(ip_address):
            self.console.print("[red]Invalid IP address format[/red]")
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO ip_logs 
                (ip_address, user_agent, request_method, request_path, status_code, referer, purpose, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ip_address, user_agent, request_method, request_path, status_code, referer, purpose, notes))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Logged IP address: {ip_address} for purpose: {purpose}")
            self.console.print(f"[green]Successfully logged IP: {ip_address}[/green]")
            
            return True
            
        except Exception as e:
            self.error_handler.handle_exception(e, "IP logging")
            self.console.print(f"[red]Error logging IP: {e}[/red]")
            return False
    
    @handle_errors("View IP logs", show_user=True)
    def view_logs(self, limit: int = 50, ip_filter: str = None) -> List[Dict[str, Any]]:
        """
        View IP logs from the database.
        
        Args:
            limit: Maximum number of logs to display
            ip_filter: Filter by specific IP address
            
        Returns:
            List of log entries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if ip_filter:
                cursor.execute('''
                    SELECT * FROM ip_logs 
                    WHERE ip_address = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (ip_filter, limit))
            else:
                cursor.execute('''
                    SELECT * FROM ip_logs 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            # Convert to list of dictionaries
            logs = []
            for row in rows:
                logs.append({
                    'id': row[0],
                    'ip_address': row[1],
                    'timestamp': row[2],
                    'user_agent': row[3],
                    'request_method': row[4],
                    'request_path': row[5],
                    'status_code': row[6],
                    'referer': row[7],
                    'purpose': row[8],
                    'notes': row[9]
                })
            
            self.display_logs(logs)
            return logs
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Viewing logs")
            self.console.print(f"[red]Error viewing logs: {e}[/red]")
            return []
    
    def display_logs(self, logs: List[Dict[str, Any]]) -> None:
        """Display IP logs in a formatted table."""
        if not logs:
            self.console.print("[yellow]No logs found[/yellow]")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan")
        table.add_column("IP Address", style="green")
        table.add_column("Timestamp", style="white")
        table.add_column("Method", style="yellow")
        table.add_column("Path", style="white")
        table.add_column("Status", style="cyan")
        table.add_column("Purpose", style="magenta")
        
        for log in logs:
            table.add_row(
                str(log['id']),
                log['ip_address'],
                log['timestamp'][:19] if log['timestamp'] else 'N/A',
                log['request_method'] or 'N/A',
                (log['request_path'] or '/')[:20],
                str(log['status_code']) if log['status_code'] else 'N/A',
                log['purpose'] or 'N/A'
            )
        
        self.console.print(Panel(table, title=f"[bold]IP Logs ({len(logs)} entries)[/bold]"))
    
    @handle_errors("Get IP statistics", show_user=True)
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about logged IP addresses.
        
        Returns:
            Dictionary with statistics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total logs
            cursor.execute('SELECT COUNT(*) FROM ip_logs')
            total_logs = cursor.fetchone()[0]
            
            # Unique IPs
            cursor.execute('SELECT COUNT(DISTINCT ip_address) FROM ip_logs')
            unique_ips = cursor.fetchone()[0]
            
            # Top IPs
            cursor.execute('''
                SELECT ip_address, COUNT(*) as count 
                FROM ip_logs 
                GROUP BY ip_address 
                ORDER BY count DESC 
                LIMIT 10
            ''')
            top_ips = cursor.fetchall()
            
            # Logs by purpose
            cursor.execute('''
                SELECT purpose, COUNT(*) as count 
                FROM ip_logs 
                GROUP BY purpose 
                ORDER BY count DESC
            ''')
            purpose_stats = cursor.fetchall()
            
            # Recent activity
            cursor.execute('''
                SELECT DATE(timestamp) as date, COUNT(*) as count 
                FROM ip_logs 
                WHERE timestamp >= date('now', '-7 days')
                GROUP BY date 
                ORDER BY date DESC
            ''')
            recent_activity = cursor.fetchall()
            
            conn.close()
            
            stats = {
                'total_logs': total_logs,
                'unique_ips': unique_ips,
                'top_ips': top_ips,
                'purpose_stats': purpose_stats,
                'recent_activity': recent_activity
            }
            
            self.display_statistics(stats)
            return stats
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Getting statistics")
            self.console.print(f"[red]Error getting statistics: {e}[/red]")
            return {}
    
    def display_statistics(self, stats: Dict[str, Any]) -> None:
        """Display IP logging statistics."""
        # Overview table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Logs", str(stats['total_logs']))
        table.add_row("Unique IP Addresses", str(stats['unique_ips']))
        
        self.console.print(Panel(table, title="[bold]IP Logger Statistics[/bold]"))
        
        # Top IPs
        if stats['top_ips']:
            top_table = Table(show_header=True, header_style="bold magenta")
            top_table.add_column("IP Address", style="cyan")
            top_table.add_column("Request Count", style="green")
            
            for ip, count in stats['top_ips']:
                top_table.add_row(ip, str(count))
            
            self.console.print(Panel(top_table, title="[bold]Top IP Addresses[/bold]"))
        
        # Purpose breakdown
        if stats['purpose_stats']:
            purpose_table = Table(show_header=True, header_style="bold magenta")
            purpose_table.add_column("Purpose", style="cyan")
            purpose_table.add_column("Count", style="green")
            
            for purpose, count in stats['purpose_stats']:
                purpose_table.add_row(purpose or 'Unknown', str(count))
            
            self.console.print(Panel(purpose_table, title="[bold]Logs by Purpose[/bold]"))
    
    @handle_errors("Export logs", show_user=True)
    def export_logs(self, export_format: str = "json", output_file: str = None) -> bool:
        """
        Export IP logs to a file.
        
        Args:
            export_format: Export format (json, csv)
            output_file: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM ip_logs ORDER BY timestamp DESC')
            rows = cursor.fetchall()
            conn.close()
            
            # Convert to list of dictionaries
            logs = []
            for row in rows:
                logs.append({
                    'id': row[0],
                    'ip_address': row[1],
                    'timestamp': row[2],
                    'user_agent': row[3],
                    'request_method': row[4],
                    'request_path': row[5],
                    'status_code': row[6],
                    'referer': row[7],
                    'purpose': row[8],
                    'notes': row[9]
                })
            
            # Generate output filename if not provided
            if not output_file:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = f"ip_logs_export_{timestamp}.{export_format}"
            
            # Export based on format
            if export_format.lower() == 'json':
                with open(output_file, 'w') as f:
                    json.dump(logs, f, indent=2, default=str)
            elif export_format.lower() == 'csv':
                import csv
                with open(output_file, 'w', newline='') as f:
                    if logs:
                        writer = csv.DictWriter(f, fieldnames=logs[0].keys())
                        writer.writeheader()
                        writer.writerows(logs)
            else:
                self.console.print("[red]Unsupported export format[/red]")
                return False
            
            self.console.print(f"[green]Exported {len(logs)} logs to {output_file}[/green]")
            return True
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Exporting logs")
            self.console.print(f"[red]Error exporting logs: {e}[/red]")
            return False
    
    @handle_errors("Clear old logs", show_user=True)
    def clear_old_logs(self, days: int = 30) -> bool:
        """
        Clear logs older than specified days.
        
        Args:
            days: Number of days to keep logs
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM ip_logs 
                WHERE timestamp < datetime('now', '-' || ? || ' days')
            ''', (days,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            self.console.print(f"[green]Cleared {deleted_count} logs older than {days} days[/green]")
            self.logger.info(f"Cleared {deleted_count} logs older than {days} days")
            
            return True
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Clearing old logs")
            self.console.print(f"[red]Error clearing logs: {e}[/red]")
            return False
    
    @handle_errors("Search logs", show_user=True)
    def search_logs(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search logs for specific terms.
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of matching log entries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM ip_logs 
                WHERE ip_address LIKE ? 
                OR user_agent LIKE ? 
                OR request_path LIKE ? 
                OR purpose LIKE ? 
                OR notes LIKE ?
                ORDER BY timestamp DESC
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', 
                  f'%{search_term}%', f'%{search_term}%'))
            
            rows = cursor.fetchall()
            conn.close()
            
            # Convert to list of dictionaries
            logs = []
            for row in rows:
                logs.append({
                    'id': row[0],
                    'ip_address': row[1],
                    'timestamp': row[2],
                    'user_agent': row[3],
                    'request_method': row[4],
                    'request_path': row[5],
                    'status_code': row[6],
                    'referer': row[7],
                    'purpose': row[8],
                    'notes': row[9]
                })
            
            self.console.print(f"[green]Found {len(logs)} matching logs[/green]")
            self.display_logs(logs[:20])  # Show first 20
            
            return logs
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Searching logs")
            self.console.print(f"[red]Error searching logs: {e}[/red]")
            return []
    
    def display_privacy_notice(self) -> None:
        """Display privacy and legal notice."""
        notice = """
        [bold yellow]PRIVACY AND LEGAL NOTICE[/bold yellow]
        
        This IP logger is intended for legitimate purposes only:
        - Security monitoring and incident response
        - Website analytics and traffic analysis
        - System administration and troubleshooting
        - Fraud detection and prevention
        
        [red]IMPORTANT LEGAL REQUIREMENTS:[/red]
        - Comply with GDPR, CCPA, and other privacy laws
        - Obtain proper consent where required
        - Provide privacy policies to users
        - Implement data retention policies
        - Secure stored data appropriately
        - Do not use for stalking, harassment, or malicious tracking
        
        Users are responsible for ensuring their use of this tool
        complies with all applicable laws and regulations.
        """
        
        self.console.print(Panel(notice, title="[bold]Legal Compliance[/bold]", border_style="red"))
    
    def main(self) -> None:
        """Main entry point for IP logger."""
        self.display_privacy_notice()
        input("\nPress Enter to continue...")
        
        tools = [
            {
                'name': 'Log IP Address',
                'description': 'Manually log an IP address with details',
                'function': self.run_log_ip
            },
            {
                'name': 'View Logs',
                'description': 'View IP logs from database',
                'function': self.run_view_logs
            },
            {
                'name': 'Get Statistics',
                'description': 'View IP logging statistics',
                'function': self.run_statistics
            },
            {
                'name': 'Search Logs',
                'description': 'Search logs for specific terms',
                'function': self.run_search_logs
            },
            {
                'name': 'Export Logs',
                'description': 'Export logs to file',
                'function': self.run_export_logs
            },
            {
                'name': 'Clear Old Logs',
                'description': 'Remove logs older than specified days',
                'function': self.run_clear_logs
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("IP Logger", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_log_ip(self) -> None:
        """Run IP logging."""
        self.console.print("\n[bold cyan]Log IP Address[/bold cyan]")
        ip_address = input("Enter IP address: ").strip()
        
        if not ip_address:
            self.console.print("[red]IP address required[/red]")
            return
        
        user_agent = input("Enter user agent (optional): ").strip()
        request_method = input("Enter request method (default GET): ").strip()
        request_path = input("Enter request path (default /): ").strip()
        status_code = input("Enter status code (default 200): ").strip()
        purpose = input("Enter purpose (monitoring/analytics/security): ").strip()
        notes = input("Enter notes (optional): ").strip()
        
        if not request_method:
            request_method = "GET"
        if not request_path:
            request_path = "/"
        if not status_code:
            status_code = 200
        else:
            status_code = int(status_code)
        if not purpose:
            purpose = "monitoring"
        
        self.log_ip(ip_address, user_agent, request_method, request_path, 
                   status_code, None, purpose, notes)
    
    def run_view_logs(self) -> None:
        """Run view logs."""
        self.console.print("\n[bold cyan]View IP Logs[/bold cyan]")
        limit = input("Enter number of logs to view (default 50): ").strip()
        ip_filter = input("Filter by IP address (optional): ").strip()
        
        if not limit:
            limit = 50
        else:
            limit = int(limit)
        
        self.view_logs(limit, ip_filter if ip_filter else None)
    
    def run_statistics(self) -> None:
        """Run statistics."""
        self.console.print("\n[bold cyan]IP Logger Statistics[/bold cyan]")
        self.get_statistics()
    
    def run_search_logs(self) -> None:
        """Run search logs."""
        self.console.print("\n[bold cyan]Search IP Logs[/bold cyan]")
        search_term = input("Enter search term: ").strip()
        if search_term:
            self.search_logs(search_term)
    
    def run_export_logs(self) -> None:
        """Run export logs."""
        self.console.print("\n[bold cyan]Export IP Logs[/bold cyan]")
        export_format = input("Enter export format (json/csv, default json): ").strip()
        output_file = input("Enter output file path (optional): ").strip()
        
        if not export_format:
            export_format = "json"
        
        self.export_logs(export_format, output_file if output_file else None)
    
    def run_clear_logs(self) -> None:
        """Run clear logs."""
        self.console.print("\n[bold cyan]Clear Old Logs[/bold cyan]")
        days = input("Enter days to keep (default 30): ").strip()
        
        if not days:
            days = 30
        else:
            days = int(days)
        
        confirm = input(f"Confirm clearing logs older than {days} days? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.clear_old_logs(days)
        else:
            self.console.print("[yellow]Operation cancelled[/yellow]")


def main():
    """Entry point for IP logger."""
    logger = IPLogger()
    logger.main()


if __name__ == "__main__":
    main()