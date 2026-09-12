"""
Generators Module
Provides demo/format generators for educational purposes
"""

import secrets
import string
import json
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class GeneratorTools:
    """Main class for generator tools."""
    
    def __init__(self):
        """Initialize generator tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
    
    @handle_errors("UUID generator", show_user=True)
    def generate_uuid(self, version: int = 4) -> Optional[str]:
        """
        Generate a UUID.
        
        Args:
            version: UUID version (1, 4, or 7)
            
        Returns:
            Generated UUID or None on error
        """
        try:
            if version == 1:
                generated_uuid = uuid.uuid1()
            elif version == 4:
                generated_uuid = uuid.uuid4()
            elif version == 7:
                generated_uuid = uuid.uuid7() if hasattr(uuid, 'uuid7') else uuid.uuid4()
            else:
                self.console.print("[red]Invalid UUID version. Using version 4[/red]")
                generated_uuid = uuid.uuid4()
            
            self.console.print(f"[green]Generated UUID (v{version}): {generated_uuid}[/green]")
            return str(generated_uuid)
            
        except Exception as e:
            self.error_handler.handle_exception(e, "UUID generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("Password generator", show_user=True)
    def generate_password(self, length: int = 16, include_symbols: bool = True, 
                         include_numbers: bool = True) -> Optional[str]:
        """
        Generate a secure random password.
        
        Args:
            length: Password length
            include_symbols: Include special characters
            include_numbers: Include numbers
            
        Returns:
            Generated password or None on error
        """
        try:
            if length < 8:
                self.console.print("[yellow]Password length too short. Using minimum 8[/yellow]")
                length = 8
            if length > 128:
                self.console.print("[yellow]Password length too long. Using maximum 128[/yellow]")
                length = 128
            
            chars = string.ascii_letters
            if include_numbers:
                chars += string.digits
            if include_symbols:
                chars += string.punctuation
            
            password = ''.join(secrets.choice(chars) for _ in range(length))
            
            self.display_generated_password(password, length)
            return password
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Password generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_generated_password(self, password: str, length: int) -> None:
        """Display generated password."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Password", password)
        table.add_row("Length", str(length))
        table.add_row("Entropy (bits)", str(len(password) * 4))  # Approximate
        
        self.console.print(Panel(table, title="[bold]Generated Password[/bold]"))
        self.console.print("[yellow]WARNING: Store this password securely![/yellow]")
    
    @handle_errors("API key generator", show_user=True)
    def generate_api_key(self, prefix: str = "", length: int = 32) -> Optional[str]:
        """
        Generate a random API key.
        
        Args:
            prefix: Optional prefix for the key
            length: Length of the random part
            
        Returns:
            Generated API key or None on error
        """
        try:
            chars = string.ascii_letters + string.digits
            random_part = ''.join(secrets.choice(chars) for _ in range(length))
            
            if prefix:
                api_key = f"{prefix}_{random_part}"
            else:
                api_key = random_part
            
            self.console.print(f"[green]Generated API Key: {api_key}[/green]")
            self.console.print("[yellow]WARNING: Store this key securely![/yellow]")
            return api_key
            
        except Exception as e:
            self.error_handler.handle_exception(e, "API key generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("JSON data generator", show_user=True)
    def generate_json_data(self, record_count: int = 5) -> Optional[List[Dict[str, Any]]]:
        """
        Generate sample JSON data for testing.
        
        Args:
            record_count: Number of records to generate
            
        Returns:
            Generated JSON data or None on error
        """
        try:
            if record_count < 1:
                record_count = 1
            if record_count > 100:
                self.console.print("[yellow]Limiting to 100 records[/yellow]")
                record_count = 100
            
            data = []
            first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Emma"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
            
            for i in range(record_count):
                record = {
                    "id": i + 1,
                    "uuid": str(uuid.uuid4()),
                    "name": f"{secrets.choice(first_names)} {secrets.choice(last_names)}",
                    "email": f"user{i}@example.com",
                    "active": secrets.choice([True, False]),
                    "score": secrets.randbelow(100),
                    "created_at": (datetime.now() - timedelta(days=secrets.randbelow(365))).isoformat()
                }
                data.append(record)
            
            self.display_json_data(data)
            return data
            
        except Exception as e:
            self.error_handler.handle_exception(e, "JSON data generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_json_data(self, data: List[Dict[str, Any]]) -> None:
        """Display generated JSON data."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Email", style="white")
        table.add_column("Active", style="yellow")
        
        for record in data[:10]:  # Show first 10
            table.add_row(
                str(record['id']),
                record['name'],
                record['email'],
                str(record['active'])
            )
        
        if len(data) > 10:
            table.add_row("...", f"and {len(data) - 10} more", "", "")
        
        self.console.print(Panel(table, title=f"[bold]Generated JSON Data ({len(data)} records)[/bold]"))
        
        # Show full JSON for first record
        if data:
            self.console.print("\n[bold cyan]Sample Record (JSON):[/bold cyan]")
            self.console.print(json.dumps(data[0], indent=2))
    
    @handle_errors("Timestamp generator", show_user=True)
    def generate_timestamps(self, count: int = 5, format_type: str = "iso") -> Optional[List[str]]:
        """
        Generate timestamps in various formats.
        
        Args:
            count: Number of timestamps to generate
            format_type: Format type (iso, unix, readable)
            
        Returns:
            Generated timestamps or None on error
        """
        try:
            if count < 1:
                count = 1
            if count > 50:
                count = 50
            
            timestamps = []
            now = datetime.now()
            
            for i in range(count):
                # Generate timestamps at random times in the past year
                random_days = secrets.randbelow(365)
                dt = now - timedelta(days=random_days)
                
                if format_type == "iso":
                    timestamp = dt.isoformat()
                elif format_type == "unix":
                    timestamp = str(int(dt.timestamp()))
                elif format_type == "readable":
                    timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    timestamp = dt.isoformat()
                
                timestamps.append(timestamp)
            
            self.display_timestamps(timestamps, format_type)
            return timestamps
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Timestamp generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_timestamps(self, timestamps: List[str], format_type: str) -> None:
        """Display generated timestamps."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan")
        table.add_column(f"Timestamp ({format_type.upper()})", style="green")
        
        for i, ts in enumerate(timestamps, 1):
            table.add_row(str(i), ts)
        
        self.console.print(Panel(table, title="[bold]Generated Timestamps[/bold]"))
    
    @handle_errors("Lorem ipsum generator", show_user=True)
    def generate_lorem_ipsum(self, paragraphs: int = 3, words_per_paragraph: int = 50) -> Optional[str]:
        """
        Generate lorem ipsum text.
        
        Args:
            paragraphs: Number of paragraphs
            words_per_paragraph: Words per paragraph
            
        Returns:
            Generated text or None on error
        """
        try:
            lorem_words = [
                "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
                "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
                "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
                "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
                "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
                "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur"
            ]
            
            text = []
            for _ in range(paragraphs):
                paragraph_words = [secrets.choice(lorem_words) for _ in range(words_per_paragraph)]
                paragraph = ' '.join(paragraph_words)
                paragraph = paragraph[0].upper() + paragraph[1:] + '.'
                text.append(paragraph)
            
            full_text = '\n\n'.join(text)
            
            self.display_lorem_ipsum(full_text, paragraphs)
            return full_text
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Lorem ipsum generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_lorem_ipsum(self, text: str, paragraph_count: int) -> None:
        """Display generated lorem ipsum text."""
        self.console.print(Panel(text[:500], title=f"[bold]Lorem Ipsum ({paragraph_count} paragraphs)[/bold]"))
        if len(text) > 500:
            self.console.print(f"[yellow]... ({len(text) - 500} more characters)[/yellow]")
    
    @handle_errors("Hash generator", show_user=True)
    def generate_hash(self, text: str, algorithm: str = "sha256") -> Optional[str]:
        """
        Generate hash of input text.
        
        Args:
            text: Text to hash
            algorithm: Hash algorithm (md5, sha1, sha256, sha512)
            
        Returns:
            Generated hash or None on error
        """
        try:
            import hashlib
            
            algorithm = algorithm.lower()
            if algorithm not in ['md5', 'sha1', 'sha256', 'sha512']:
                self.console.print("[red]Invalid algorithm. Using sha256[/red]")
                algorithm = 'sha256'
            
            hash_func = getattr(hashlib, algorithm)
            hash_obj = hash_func(text.encode())
            hash_hex = hash_obj.hexdigest()
            
            self.display_hash(text, algorithm, hash_hex)
            return hash_hex
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Hash generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_hash(self, text: str, algorithm: str, hash_hex: str) -> None:
        """Display hash result."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Algorithm", algorithm.upper())
        table.add_row("Input", text[:50] + "..." if len(text) > 50 else text)
        table.add_row("Hash", hash_hex)
        
        self.console.print(Panel(table, title="[bold]Hash Result[/bold]"))
    
    def main(self) -> None:
        """Main entry point for generators module."""
        tools = [
            {
                'name': 'UUID Generator',
                'description': 'Generate random UUIDs',
                'function': self.run_uuid_generator
            },
            {
                'name': 'Password Generator',
                'description': 'Generate secure random passwords',
                'function': self.run_password_generator
            },
            {
                'name': 'API Key Generator',
                'description': 'Generate random API keys',
                'function': self.run_api_key_generator
            },
            {
                'name': 'JSON Data Generator',
                'description': 'Generate sample JSON data',
                'function': self.run_json_generator
            },
            {
                'name': 'Timestamp Generator',
                'description': 'Generate timestamps in various formats',
                'function': self.run_timestamp_generator
            },
            {
                'name': 'Lorem Ipsum Generator',
                'description': 'Generate placeholder text',
                'function': self.run_lorem_generator
            },
            {
                'name': 'Hash Generator',
                'description': 'Generate hashes of text',
                'function': self.run_hash_generator
            },
            {
                'name': 'Barcode Generator',
                'description': 'Generate barcode numbers',
                'function': self.run_barcode_generator
            },
            {
                'name': 'QR Code Data',
                'description': 'Generate QR code data strings',
                'function': self.run_qr_generator
            },
            {
                'name': 'Color Generator',
                'description': 'Generate random color codes',
                'function': self.run_color_generator
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("Generators", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_uuid_generator(self) -> None:
        """Run UUID generator."""
        self.console.print("\n[bold cyan]UUID Generator[/bold cyan]")
        version = input("Enter UUID version (1, 4, or 7, default 4): ").strip()
        if not version:
            version = 4
        else:
            version = int(version)
        self.generate_uuid(version)
    
    def run_password_generator(self) -> None:
        """Run password generator."""
        self.console.print("\n[bold cyan]Password Generator[/bold cyan]")
        length = input("Enter password length (default 16): ").strip()
        if not length:
            length = 16
        else:
            length = int(length)
        
        include_symbols = input("Include symbols? (y/n, default y): ").strip().lower() != 'n'
        include_numbers = input("Include numbers? (y/n, default y): ").strip().lower() != 'n'
        
        self.generate_password(length, include_symbols, include_numbers)
    
    def run_api_key_generator(self) -> None:
        """Run API key generator."""
        self.console.print("\n[bold cyan]API Key Generator[/bold cyan]")
        prefix = input("Enter prefix (optional): ").strip()
        length = input("Enter length (default 32): ").strip()
        if not length:
            length = 32
        else:
            length = int(length)
        self.generate_api_key(prefix, length)
    
    def run_json_generator(self) -> None:
        """Run JSON data generator."""
        self.console.print("\n[bold cyan]JSON Data Generator[/bold cyan]")
        count = input("Enter number of records (default 5): ").strip()
        if not count:
            count = 5
        else:
            count = int(count)
        self.generate_json_data(count)
    
    def run_timestamp_generator(self) -> None:
        """Run timestamp generator."""
        self.console.print("\n[bold cyan]Timestamp Generator[/bold cyan]")
        count = input("Enter number of timestamps (default 5): ").strip()
        if not count:
            count = 5
        else:
            count = int(count)
        
        format_type = input("Enter format (iso/unix/readable, default iso): ").strip()
        if not format_type:
            format_type = "iso"
        
        self.generate_timestamps(count, format_type)
    
    def run_lorem_generator(self) -> None:
        """Run lorem ipsum generator."""
        self.console.print("\n[bold cyan]Lorem Ipsum Generator[/bold cyan]")
        paragraphs = input("Enter number of paragraphs (default 3): ").strip()
        if not paragraphs:
            paragraphs = 3
        else:
            paragraphs = int(paragraphs)
        
        words = input("Enter words per paragraph (default 50): ").strip()
        if not words:
            words = 50
        else:
            words = int(words)
        
        self.generate_lorem_ipsum(paragraphs, words)
    
    def run_hash_generator(self) -> None:
        """Run hash generator."""
        self.console.print("\n[bold cyan]Hash Generator[/bold cyan]")
        text = input("Enter text to hash: ").strip()
        if not text:
            self.console.print("[red]Text cannot be empty[/red]")
            return
        
        algorithm = input("Enter algorithm (md5/sha1/sha256/sha512, default sha256): ").strip()
        if not algorithm:
            algorithm = "sha256"
        
        self.generate_hash(text, algorithm)
    
    @handle_errors("Barcode generator", show_user=True)
    def generate_barcode(self, barcode_type: str = "EAN13") -> Optional[str]:
        """
        Generate a random barcode number.
        
        Args:
            barcode_type: Type of barcode (EAN13, UPC, ISBN)
            
        Returns:
            Generated barcode or None on error
        """
        try:
            if barcode_type == "EAN13":
                # Generate 12 random digits, calculate checksum
                digits = [secrets.randbelow(10) for _ in range(12)]
                # Calculate checksum
                checksum = sum(digits[::2]) + 3 * sum(digits[1::2])
                checksum = (10 - (checksum % 10)) % 10
                digits.append(checksum)
                barcode = ''.join(map(str, digits))
            elif barcode_type == "UPC":
                digits = [secrets.randbelow(10) for _ in range(11)]
                checksum = sum(digits[::2]) + 3 * sum(digits[1::2])
                checksum = (10 - (checksum % 10)) % 10
                digits.append(checksum)
                barcode = ''.join(map(str, digits))
            else:
                # Generic barcode
                barcode = ''.join([str(secrets.randbelow(10)) for _ in range(13)])
            
            self.console.print(f"[green]Generated {barcode_type} barcode: {barcode}[/green]")
            return barcode
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Barcode generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("QR code data generator", show_user=True)
    def generate_qr_data(self, data_type: str = "url") -> Optional[str]:
        """
        Generate QR code data string.
        
        Args:
            data_type: Type of data (url, text, wifi, contact)
            
        Returns:
            Generated QR data or None on error
        """
        try:
            if data_type == "url":
                url = f"https://example.com/{secrets.token_urlsafe(8)}"
                qr_data = url
            elif data_type == "text":
                qr_data = secrets.token_hex(16)
            elif data_type == "wifi":
                ssid = f"WiFi_{secrets.token_hex(4)}"
                password = secrets.token_urlsafe(12)
                qr_data = f"WIFI:S:{ssid};T:WPA;P:{password};;"
            elif data_type == "contact":
                name = f"User{secrets.randbelow(1000)}"
                phone = f"+1{secrets.randbelow(10000000000)}"
                qr_data = f"BEGIN:VCARD\nVERSION:3.0\nN:{name}\nTEL:{phone}\nEND:VCARD"
            else:
                qr_data = secrets.token_hex(16)
            
            self.console.print(f"[green]Generated QR data ({data_type}): {qr_data[:100]}...[/green]")
            return qr_data
            
        except Exception as e:
            self.error_handler.handle_exception(e, "QR data generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("Color generator", show_user=True)
    def generate_color(self, color_format: str = "hex") -> Optional[Dict[str, str]]:
        """
        Generate random color codes.
        
        Args:
            color_format: Color format (hex, rgb, hsl)
            
        Returns:
            Color values or None on error
        """
        try:
            # Generate random RGB values
            r = secrets.randbelow(256)
            g = secrets.randbelow(256)
            b = secrets.randbelow(256)
            
            colors = {
                'rgb': f"rgb({r}, {g}, {b})",
                'hex': f"#{r:02x}{g:02x}{b:02x}",
                'decimal': f"{r}, {g}, {b}"
            }
            
            # Calculate HSL
            r_norm, g_norm, b_norm = r/255, g/255, b/255
            c_max = max(r_norm, g_norm, b_norm)
            c_min = min(r_norm, g_norm, b_norm)
            delta = c_max - c_min
            
            if delta == 0:
                h = 0
            elif c_max == r_norm:
                h = 60 * (((g_norm - b_norm) / delta) % 6)
            elif c_max == g_norm:
                h = 60 * (((b_norm - r_norm) / delta) + 2)
            else:
                h = 60 * (((r_norm - g_norm) / delta) + 4)
            
            l = (c_max + c_min) / 2
            s = 0 if delta == 0 else delta / (1 - abs(2*l - 1))
            
            colors['hsl'] = f"hsl({h:.0f}, {s*100:.0f}%, {l*100:.0f}%)"
            
            self.display_color(colors)
            return colors
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Color generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_color(self, colors: Dict[str, str]) -> None:
        """Display generated color."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Format", style="cyan")
        table.add_column("Value", style="green")
        
        for format_name, value in colors.items():
            table.add_row(format_name.upper(), value)
        
        self.console.print(Panel(table, title="[bold]Generated Color[/bold]"))
    
    def run_barcode_generator(self) -> None:
        """Run barcode generator."""
        self.console.print("\n[bold cyan]Barcode Generator[/bold cyan]")
        barcode_type = input("Enter type (EAN13/UPC, default EAN13): ").strip()
        if not barcode_type:
            barcode_type = "EAN13"
        self.generate_barcode(barcode_type)
    
    def run_qr_generator(self) -> None:
        """Run QR generator."""
        self.console.print("\n[bold cyan]QR Code Data Generator[/bold cyan]")
        data_type = input("Enter type (url/text/wifi/contact, default url): ").strip()
        if not data_type:
            data_type = "url"
        self.generate_qr_data(data_type)
    
    def run_color_generator(self) -> None:
        """Run color generator."""
        self.console.print("\n[bold cyan]Color Generator[/bold cyan]")
        color_format = input("Enter format (hex/rgb/hsl, default hex): ").strip()
        if not color_format:
            color_format = "hex"
        self.generate_color(color_format)


def main():
    """Entry point for generators module."""
    generators = GeneratorTools()
    generators.main()


if __name__ == "__main__":
    main()