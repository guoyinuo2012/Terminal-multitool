"""
Crypto & Utils Module
Provides hash tools, password generation, and temporary email helpers
"""

import hashlib
import base64
import secrets
import string
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class CryptoTools:
    """Main class for crypto and utility tools."""
    
    def __init__(self):
        """Initialize crypto tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
    
    @handle_errors("MD5 hash", show_user=True)
    def hash_md5(self, text: str) -> Optional[str]:
        """
        Generate MD5 hash of text.
        
        Args:
            text: Text to hash
            
        Returns:
            MD5 hash or None on error
        """
        try:
            hash_obj = hashlib.md5(text.encode())
            hash_hex = hash_obj.hexdigest()
            
            self.display_hash_result("MD5", text, hash_hex)
            return hash_hex
            
        except Exception as e:
            self.error_handler.handle_exception(e, "MD5 hash")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("SHA1 hash", show_user=True)
    def hash_sha1(self, text: str) -> Optional[str]:
        """
        Generate SHA1 hash of text.
        
        Args:
            text: Text to hash
            
        Returns:
            SHA1 hash or None on error
        """
        try:
            hash_obj = hashlib.sha1(text.encode())
            hash_hex = hash_obj.hexdigest()
            
            self.display_hash_result("SHA1", text, hash_hex)
            return hash_hex
            
        except Exception as e:
            self.error_handler.handle_exception(e, "SHA1 hash")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("SHA256 hash", show_user=True)
    def hash_sha256(self, text: str) -> Optional[str]:
        """
        Generate SHA256 hash of text.
        
        Args:
            text: Text to hash
            
        Returns:
            SHA256 hash or None on error
        """
        try:
            hash_obj = hashlib.sha256(text.encode())
            hash_hex = hash_obj.hexdigest()
            
            self.display_hash_result("SHA256", text, hash_hex)
            return hash_hex
            
        except Exception as e:
            self.error_handler.handle_exception(e, "SHA256 hash")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("SHA512 hash", show_user=True)
    def hash_sha512(self, text: str) -> Optional[str]:
        """
        Generate SHA512 hash of text.
        
        Args:
            text: Text to hash
            
        Returns:
            SHA512 hash or None on error
        """
        try:
            hash_obj = hashlib.sha512(text.encode())
            hash_hex = hash_obj.hexdigest()
            
            self.display_hash_result("SHA512", text, hash_hex)
            return hash_hex
            
        except Exception as e:
            self.error_handler.handle_exception(e, "SHA512 hash")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_hash_result(self, algorithm: str, text: str, hash_hex: str) -> None:
        """Display hash result."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Algorithm", algorithm)
        table.add_row("Input", text[:50] + "..." if len(text) > 50 else text)
        table.add_row("Hash", hash_hex)
        
        self.console.print(Panel(table, title="[bold]Hash Result[/bold]"))
    
    @handle_errors("Base64 encode", show_user=True)
    def base64_encode(self, text: str) -> Optional[str]:
        """
        Encode text to Base64.
        
        Args:
            text: Text to encode
            
        Returns:
            Base64 encoded string or None on error
        """
        try:
            encoded = base64.b64encode(text.encode()).decode()
            
            self.display_base64_result("Encode", text, encoded)
            return encoded
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Base64 encode")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("Base64 decode", show_user=True)
    def base64_decode(self, encoded: str) -> Optional[str]:
        """
        Decode Base64 string.
        
        Args:
            encoded: Base64 encoded string
            
        Returns:
            Decoded string or None on error
        """
        try:
            decoded = base64.b64decode(encoded).decode()
            
            self.display_base64_result("Decode", encoded, decoded)
            return decoded
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Base64 decode")
            self.console.print(f"[red]Error: Invalid Base64 string[/red]")
            return None
    
    def display_base64_result(self, operation: str, input_text: str, output_text: str) -> None:
        """Display Base64 result."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Operation", operation)
        table.add_row("Input", input_text[:50] + "..." if len(input_text) > 50 else input_text)
        table.add_row("Output", output_text[:50] + "..." if len(output_text) > 50 else output_text)
        
        self.console.print(Panel(table, title="[bold]Base64 Result[/bold]"))
    
    @handle_errors("Secure password generator", show_user=True)
    def generate_secure_password(self, length: int = 20, use_uppercase: bool = True,
                                 use_lowercase: bool = True, use_numbers: bool = True,
                                 use_symbols: bool = True) -> Optional[str]:
        """
        Generate a cryptographically secure password.
        
        Args:
            length: Password length
            use_uppercase: Include uppercase letters
            use_lowercase: Include lowercase letters
            use_numbers: Include numbers
            use_symbols: Include symbols
            
        Returns:
            Generated password or None on error
        """
        try:
            if length < 8:
                self.console.print("[yellow]Minimum length is 8[/yellow]")
                length = 8
            if length > 128:
                self.console.print("[yellow]Maximum length is 128[/yellow]")
                length = 128
            
            chars = ""
            if use_uppercase:
                chars += string.ascii_uppercase
            if use_lowercase:
                chars += string.ascii_lowercase
            if use_numbers:
                chars += string.digits
            if use_symbols:
                chars += string.punctuation
            
            if not chars:
                self.console.print("[red]At least one character type must be selected[/red]")
                return None
            
            password = ''.join(secrets.choice(chars) for _ in range(length))
            
            self.display_password_result(password, length)
            return password
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Password generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_password_result(self, password: str, length: int) -> None:
        """Display generated password."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Password", password)
        table.add_row("Length", str(length))
        
        self.console.print(Panel(table, title="[bold]Generated Password[/bold]"))
        self.console.print("[yellow]WARNING: Store this password securely![/yellow]")
    
    @handle_errors("Password strength checker", show_user=True)
    def check_password_strength(self, password: str) -> Optional[Dict[str, Any]]:
        """
        Check password strength.
        
        Args:
            password: Password to check
            
        Returns:
            Strength analysis or None on error
        """
        try:
            score = 0
            feedback = []
            
            # Length check
            if len(password) >= 8:
                score += 1
            else:
                feedback.append("Password should be at least 8 characters")
            
            if len(password) >= 12:
                score += 1
            
            # Character variety
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_symbol = any(c in string.punctuation for c in password)
            
            if has_upper:
                score += 1
            else:
                feedback.append("Add uppercase letters")
            
            if has_lower:
                score += 1
            else:
                feedback.append("Add lowercase letters")
            
            if has_digit:
                score += 1
            else:
                feedback.append("Add numbers")
            
            if has_symbol:
                score += 1
            else:
                feedback.append("Add special characters")
            
            # Strength rating
            if score <= 2:
                strength = "Weak"
            elif score <= 4:
                strength = "Medium"
            else:
                strength = "Strong"
            
            result = {
                'password': password,
                'score': score,
                'strength': strength,
                'feedback': feedback
            }
            
            self.display_password_strength(result)
            return result
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Password strength check")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_password_strength(self, result: Dict[str, Any]) -> None:
        """Display password strength analysis."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Password", result['password'])
        table.add_row("Score", f"{result['score']}/6")
        table.add_row("Strength", result['strength'])
        table.add_row("Feedback", ', '.join(result['feedback']) if result['feedback'] else "Good!")
        
        self.console.print(Panel(table, title="[bold]Password Strength[/bold]"))
    
    @handle_errors("Temporary email info", show_user=True)
    def get_temp_email_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about temporary email services.
        
        Returns:
            Temp email service information or None on error
        """
        try:
            # Common temporary email services
            services = [
                {
                    'name': '10 Minute Mail',
                    'url': 'https://10minutemail.com',
                    'duration': '10 minutes',
                    'features': ['No registration', 'Auto-refresh']
                },
                {
                    'name': 'Guerrilla Mail',
                    'url': 'https://www.guerrillamail.com',
                    'duration': '60 minutes',
                    'features': ['Custom domain', 'Attachments']
                },
                {
                    'name': 'Temp Mail',
                    'url': 'https://temp-mail.org',
                    'duration': 'Variable',
                    'features': ['Multiple domains', 'Mobile app']
                },
                {
                    'name': 'Mailinator',
                    'url': 'https://www.mailinator.com',
                    'duration': 'Temporary',
                    'features': ['Public inbox', 'API access']
                }
            ]
            
            self.display_temp_email_services(services)
            return {'services': services}
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Temp email info")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_temp_email_services(self, services: List[Dict[str, Any]]) -> None:
        """Display temporary email services."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Service", style="cyan")
        table.add_column("Duration", style="green")
        table.add_column("Features", style="white")
        table.add_column("URL", style="yellow")
        
        for service in services:
            table.add_row(
                service['name'],
                service['duration'],
                ', '.join(service['features']),
                service['url']
            )
        
        self.console.print(Panel(table, title="[bold]Temporary Email Services[/bold]"))
        self.console.print("[yellow]Note: These services are for temporary use only. Do not use for important accounts.[/yellow]")
    
    @handle_errors("Token generator", show_user=True)
    def generate_token(self, length: int = 32) -> Optional[str]:
        """
        Generate a random token.
        
        Args:
            length: Token length in bytes
            
        Returns:
            Hex-encoded token or None on error
        """
        try:
            token = secrets.token_hex(length)
            
            self.console.print(f"[green]Generated Token: {token}[/green]")
            self.console.print("[yellow]WARNING: Store this token securely![/yellow]")
            return token
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Token generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("HMAC generator", show_user=True)
    def generate_hmac(self, text: str, key: str, algorithm: str = "sha256") -> Optional[str]:
        """
        Generate HMAC of text with key.
        
        Args:
            text: Text to authenticate
            key: Secret key
            algorithm: Hash algorithm (sha256, sha512, md5, sha1)
            
        Returns:
            HMAC hex digest or None on error
        """
        try:
            algorithm = algorithm.lower()
            if algorithm not in ['sha256', 'sha512', 'md5', 'sha1']:
                self.console.print("[red]Invalid algorithm. Using sha256[/red]")
                algorithm = 'sha256'
            
            hash_func = getattr(hashlib, algorithm)
            hmac_obj = hmac.new(key.encode(), text.encode(), hash_func)
            hmac_hex = hmac_obj.hexdigest()
            
            self.display_hmac_result(algorithm, text, hmac_hex)
            return hmac_hex
            
        except NameError:
            import hmac
            hash_func = getattr(hashlib, algorithm)
            hmac_obj = hmac.new(key.encode(), text.encode(), hash_func)
            hmac_hex = hmac_obj.hexdigest()
            
            self.display_hmac_result(algorithm, text, hmac_hex)
            return hmac_hex
        except Exception as e:
            self.error_handler.handle_exception(e, "HMAC generation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_hmac_result(self, algorithm: str, text: str, hmac_hex: str) -> None:
        """Display HMAC result."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Algorithm", algorithm.upper())
        table.add_row("Input", text[:50] + "..." if len(text) > 50 else text)
        table.add_row("HMAC", hmac_hex)
        
        self.console.print(Panel(table, title="[bold]HMAC Result[/bold]"))
    
    def main(self) -> None:
        """Main entry point for crypto module."""
        tools = [
            {
                'name': 'MD5 Hash',
                'description': 'Generate MD5 hash',
                'function': self.run_md5_hash
            },
            {
                'name': 'SHA1 Hash',
                'description': 'Generate SHA1 hash',
                'function': self.run_sha1_hash
            },
            {
                'name': 'SHA256 Hash',
                'description': 'Generate SHA256 hash',
                'function': self.run_sha256_hash
            },
            {
                'name': 'SHA512 Hash',
                'description': 'Generate SHA512 hash',
                'function': self.run_sha512_hash
            },
            {
                'name': 'Base64 Encode',
                'description': 'Encode text to Base64',
                'function': self.run_base64_encode
            },
            {
                'name': 'Base64 Decode',
                'description': 'Decode Base64 string',
                'function': self.run_base64_decode
            },
            {
                'name': 'Secure Password Generator',
                'description': 'Generate cryptographically secure passwords',
                'function': self.run_password_generator
            },
            {
                'name': 'Password Strength Checker',
                'description': 'Check password strength',
                'function': self.run_password_strength
            },
            {
                'name': 'Temporary Email Info',
                'description': 'Get temp email service information',
                'function': self.run_temp_email_info
            },
            {
                'name': 'Token Generator',
                'description': 'Generate random tokens',
                'function': self.run_token_generator
            },
            {
                'name': 'HMAC Generator',
                'description': 'Generate HMAC with key',
                'function': self.run_hmac_generator
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("Crypto & Utils", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_md5_hash(self) -> None:
        """Run MD5 hash."""
        self.console.print("\n[bold cyan]MD5 Hash[/bold cyan]")
        text = input("Enter text to hash: ").strip()
        if text:
            self.hash_md5(text)
    
    def run_sha1_hash(self) -> None:
        """Run SHA1 hash."""
        self.console.print("\n[bold cyan]SHA1 Hash[/bold cyan]")
        text = input("Enter text to hash: ").strip()
        if text:
            self.hash_sha1(text)
    
    def run_sha256_hash(self) -> None:
        """Run SHA256 hash."""
        self.console.print("\n[bold cyan]SHA256 Hash[/bold cyan]")
        text = input("Enter text to hash: ").strip()
        if text:
            self.hash_sha256(text)
    
    def run_sha512_hash(self) -> None:
        """Run SHA512 hash."""
        self.console.print("\n[bold cyan]SHA512 Hash[/bold cyan]")
        text = input("Enter text to hash: ").strip()
        if text:
            self.hash_sha512(text)
    
    def run_base64_encode(self) -> None:
        """Run Base64 encode."""
        self.console.print("\n[bold cyan]Base64 Encode[/bold cyan]")
        text = input("Enter text to encode: ").strip()
        if text:
            self.base64_encode(text)
    
    def run_base64_decode(self) -> None:
        """Run Base64 decode."""
        self.console.print("\n[bold cyan]Base64 Decode[/bold cyan]")
        encoded = input("Enter Base64 string to decode: ").strip()
        if encoded:
            self.base64_decode(encoded)
    
    def run_password_generator(self) -> None:
        """Run password generator."""
        self.console.print("\n[bold cyan]Secure Password Generator[/bold cyan]")
        length = input("Enter password length (default 20): ").strip()
        if not length:
            length = 20
        else:
            length = int(length)
        
        use_uppercase = input("Use uppercase? (y/n, default y): ").strip().lower() != 'n'
        use_lowercase = input("Use lowercase? (y/n, default y): ").strip().lower() != 'n'
        use_numbers = input("Use numbers? (y/n, default y): ").strip().lower() != 'n'
        use_symbols = input("Use symbols? (y/n, default y): ").strip().lower() != 'n'
        
        self.generate_secure_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols)
    
    def run_password_strength(self) -> None:
        """Run password strength checker."""
        self.console.print("\n[bold cyan]Password Strength Checker[/bold cyan]")
        password = input("Enter password to check: ").strip()
        if password:
            self.check_password_strength(password)
    
    def run_temp_email_info(self) -> None:
        """Run temp email info."""
        self.console.print("\n[bold cyan]Temporary Email Services[/bold cyan]")
        self.get_temp_email_info()
    
    def run_token_generator(self) -> None:
        """Run token generator."""
        self.console.print("\n[bold cyan]Token Generator[/bold cyan]")
        length = input("Enter token length in bytes (default 32): ").strip()
        if not length:
            length = 32
        else:
            length = int(length)
        self.generate_token(length)
    
    def run_hmac_generator(self) -> None:
        """Run HMAC generator."""
        self.console.print("\n[bold cyan]HMAC Generator[/bold cyan]")
        text = input("Enter text to authenticate: ").strip()
        if not text:
            self.console.print("[red]Text cannot be empty[/red]")
            return
        
        key = input("Enter secret key: ").strip()
        if not key:
            self.console.print("[red]Key cannot be empty[/red]")
            return
        
        algorithm = input("Enter algorithm (sha256/sha512/md5/sha1, default sha256): ").strip()
        if not algorithm:
            algorithm = "sha256"
        
        self.generate_hmac(text, key, algorithm)


def main():
    """Entry point for crypto module."""
    crypto = CryptoTools()
    crypto.main()


if __name__ == "__main__":
    main()