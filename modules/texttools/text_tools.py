"""
Text Processing & Encoding Tools Module
Provides text manipulation, encoding, and decoding utilities
Created by Yinuo
"""

import base64
import hashlib
import re
import json
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class TextTools:
    """Main class for text processing tools."""
    
    def __init__(self):
        """Initialize text tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
    
    @handle_errors("Text encoding/decoding", show_user=True)
    def process_encoding(self, text: str, operation: str = "encode", encoding: str = "base64") -> Optional[str]:
        """
        Encode or decode text.
        
        Args:
            text: Text to process
            operation: 'encode' or 'decode'
            encoding: 'base64', 'url', 'hex'
            
        Returns:
            Processed text or None on error
        """
        try:
            if operation == "encode":
                if encoding == "base64":
                    result = base64.b64encode(text.encode()).decode()
                elif encoding == "url":
                    import urllib.parse
                    result = urllib.parse.quote(text)
                elif encoding == "hex":
                    result = text.encode().hex()
                else:
                    self.console.print(f"[red]Unknown encoding: {encoding}[/red]")
                    return None
            elif operation == "decode":
                if encoding == "base64":
                    result = base64.b64decode(text).decode()
                elif encoding == "url":
                    import urllib.parse
                    result = urllib.parse.unquote(text)
                elif encoding == "hex":
                    result = bytes.fromhex(text).decode()
                else:
                    self.console.print(f"[red]Unknown encoding: {encoding}[/red]")
                    return None
            else:
                self.console.print("[red]Unknown operation. Use 'encode' or 'decode'[/red]")
                return None
            
            self.display_encoding_result(text, operation, encoding, result)
            return result
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Text encoding")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_encoding_result(self, original: str, operation: str, encoding: str, result: str) -> None:
        """Display encoding/decoding result."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Operation", operation)
        table.add_row("Encoding", encoding)
        table.add_row("Original", original[:50] + "..." if len(original) > 50 else original)
        table.add_row("Result", result[:50] + "..." if len(result) > 50 else result)
        
        self.console.print(Panel(table, title="[bold]Encoding Result[/bold]"))
    
    @handle_errors("Text transformation", show_user=True)
    def transform_text(self, text: str, transformations: List[str]) -> Optional[str]:
        """
        Apply text transformations.
        
        Args:
            text: Text to transform
            transformations: List of transformations (upper, lower, title, reverse, etc.)
            
        Returns:
            Transformed text or None on error
        """
        try:
            result = text
            
            for transform in transformations:
                if transform == "upper":
                    result = result.upper()
                elif transform == "lower":
                    result = result.lower()
                elif transform == "title":
                    result = result.title()
                elif transform == "reverse":
                    result = result[::-1]
                elif transform == "swapcase":
                    result = result.swapcase()
                elif transform == "strip":
                    result = result.strip()
                elif transform == "strip_html":
                    import re
                    result = re.sub(r'<[^<]+?>', '', result)
                elif transform == "remove_numbers":
                    result = re.sub(r'\d+', '', result)
                elif transform == "remove_special":
                    result = re.sub(r'[^a-zA-Z\s]', '', result)
                elif transform == "remove_whitespace":
                    result = re.sub(r'\s+', '', result)
                else:
                    self.console.print(f"[yellow]Unknown transformation: {transform}[/yellow]")
            
            self.display_transformation(text, transformations, result)
            return result
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Text transformation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_transformation(self, original: str, transformations: List[str], result: str) -> None:
        """Display transformation result."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Original", original[:50] + "..." if len(original) > 50 else original)
        table.add_row("Transformations", ', '.join(transformations))
        table.add_row("Result", result[:50] + "..." if len(result) > 50 else result)
        
        self.console.print(Panel(table, title="[bold]Text Transformation[/bold]"))
    
    @handle_errors("Regex match", show_user=True)
    def regex_match(self, text: str, pattern: str) -> Optional[List[str]]:
        """
        Find regex matches in text.
        
        Args:
            text: Text to search
            pattern: Regex pattern
            
        Returns:
            List of matches or None on error
        """
        try:
            matches = re.findall(pattern, text)
            
            if matches:
                self.console.print(f"[green]Found {len(matches)} matches[/green]")
                for i, match in enumerate(matches[:10]):
                    self.console.print(f"  {i+1}. {match}")
            else:
                self.console.print("[yellow]No matches found[/yellow]")
            
            return matches
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Regex match")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("Text statistics", show_user=True)
    def text_statistics(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyze text statistics.
        
        Args:
            text: Text to analyze
            
        Returns:
            Text statistics or None on error
        """
        try:
            stats = {
                'length': len(text),
                'words': len(text.split()),
                'lines': text.count('\n') + 1,
                'characters': len(text.replace(' ', '')),
                'uppercase': sum(1 for c in text if c.isupper()),
                'lowercase': sum(1 for c in text if c.islower()),
                'digits': sum(1 for c in text if c.isdigit()),
                'special': sum(1 for c in text if not c.isalnum() and not c.isspace()),
                'spaces': text.count(' ')
            }
            
            self.display_text_statistics(stats)
            return stats
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Text statistics")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_text_statistics(self, stats: Dict[str, Any]) -> None:
        """Display text statistics."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="green")
        
        table.add_row("Total Length", str(stats['length']))
        table.add_row("Words", str(stats['words']))
        table.add_row("Lines", str(stats['lines']))
        table.add_row("Characters", str(stats['characters']))
        table.add_row("Uppercase", str(stats['uppercase']))
        table.add_row("Lowercase", str(stats['lowercase']))
        table.add_row("Digits", str(stats['digits']))
        table.add_row("Special Chars", str(stats['special']))
        table.add_row("Spaces", str(stats['spaces']))
        
        self.console.print(Panel(table, title="[bold]Text Statistics[/bold]"))
    
    @handle_errors("JSON formatting", show_user=True)
    def format_json(self, json_str: str) -> Optional[str]:
        """
        Format JSON string.
        
        Args:
            json_str: JSON string to format
            
        Returns:
            Formatted JSON or None on error
        """
        try:
            data = json.loads(json_str)
            formatted = json.dumps(data, indent=2)
            
            self.console.print("[green]Formatted JSON:[/green]")
            self.console.print(formatted)
            return formatted
            
        except Exception as e:
            self.error_handler.handle_exception(e, "JSON formatting")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("URL encoding/decoding", show_user=True)
    def process_url(self, url: str, operation: str = "encode") -> Optional[str]:
        """
        Encode or decode URL.
        
        Args:
            url: URL to process
            operation: 'encode' or 'decode'
            
        Returns:
            Processed URL or None on error
        """
        try:
            import urllib.parse
            
            if operation == "encode":
                result = urllib.parse.quote(url)
            elif operation == "decode":
                result = urllib.parse.unquote(url)
            else:
                self.console.print("[red]Unknown operation. Use 'encode' or 'decode'[/red]")
                return None
            
            self.display_url_result(url, operation, result)
            return result
            
        except Exception as e:
            self.error_handler.handle_exception(e, "URL processing")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_url_result(self, original: str, operation: str, result: str) -> None:
        """Display URL processing result."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Operation", operation)
        table.add_row("Original", original[:50] + "..." if len(original) > 50 else original)
        table.add_row("Result", result[:50] + "..." if len(result) > 50 else result)
        
        self.console.print(Panel(table, title="[bold]URL Processing[/bold]"))
    
    @handle_errors("Character count", show_user=True)
    def count_characters(self, text: str, char: str = None) -> Optional[int]:
        """
        Count character occurrences in text.
        
        Args:
            text: Text to analyze
            char: Specific character to count (None for all chars)
            
        Returns:
            Character count or None on error
        """
        try:
            if char:
                count = text.count(char)
                self.console.print(f"[green]Character '{char}' appears {count} times[/green]")
            else:
                count = len(text)
                self.console.print(f"[green]Total characters: {count}[/green]")
            
            return count
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Character count")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("Line operations", show_user=True)
    def process_lines(self, text: str, operation: str = "count") -> Optional[List[str]]:
        """
        Process text by lines.
        
        Args:
            text: Text to process
            operation: 'count', 'reverse', 'sort', 'unique', 'remove_empty'
            
        Returns:
            Processed lines or None on error
        """
        try:
            lines = text.split('\n')
            
            if operation == "count":
                result = lines
                self.console.print(f"[green]Total lines: {len(lines)}[/green]")
            elif operation == "reverse":
                result = lines[::-1]
                self.console.print("[green]Lines reversed[/green]")
            elif operation == "sort":
                result = sorted(lines)
                self.console.print("[green]Lines sorted[/green]")
            elif operation == "unique":
                result = list(dict.fromkeys(lines))
                self.console.print(f"[green]Unique lines: {len(result)}[/green]")
            elif operation == "remove_empty":
                result = [line for line in lines if line.strip()]
                self.console.print(f"[green]Removed {len(lines) - len(result)} empty lines[/green]")
            else:
                self.console.print(f"[red]Unknown operation: {operation}[/red]")
                return None
            
            return result
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Line processing")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def main(self) -> None:
        """Main entry point for text tools."""
        tools = [
            {
                'name': 'Encode/Decode',
                'description': 'Base64, URL, hex encoding/decoding',
                'function': self.run_encoding
            },
            {
                'name': 'Text Transform',
                'description': 'Upper, lower, reverse, strip operations',
                'function': self.run_transform
            },
            {
                'name': 'Regex Match',
                'description': 'Find regex patterns in text',
                'function': self.run_regex
            },
            {
                'name': 'Text Statistics',
                'description': 'Character, word, line counts',
                'function': self.run_statistics
            },
            {
                'name': 'JSON Format',
                'description': 'Format JSON strings',
                'function': self.run_json_format
            },
            {
                'name': 'URL Process',
                'description': 'URL encode/decode',
                'function': self.run_url_process
            },
            {
                'name': 'Character Count',
                'description': 'Count character occurrences',
                'function': self.run_char_count
            },
            {
                'name': 'Line Operations',
                'description': 'Process text by lines',
                'function': self.run_line_ops
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("Text Tools", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_encoding(self) -> None:
        """Run encoding/decoding."""
        self.console.print("\n[bold cyan]Encode/Decode[/bold cyan]")
        text = input("Enter text: ").strip()
        operation = input("Operation (encode/decode, default encode): ").strip()
        encoding = input("Encoding (base64/url/hex, default base64): ").strip()
        if not operation:
            operation = "encode"
        if not encoding:
            encoding = "base64"
        if text:
            self.process_encoding(text, operation, encoding)
    
    def run_transform(self) -> None:
        """Run text transformation."""
        self.console.print("\n[bold cyan]Text Transformation[/bold cyan]")
        text = input("Enter text: ").strip()
        if not text:
            self.console.print("[red]Text required[/red]")
            return
        
        print("Available transformations: upper, lower, title, reverse, swapcase, strip, strip_html, remove_numbers, remove_special, remove_whitespace")
        transforms = input("Enter transformations (comma-separated): ").strip().split(',')
        if transforms:
            self.transform_text(text, [t.strip() for t in transforms])
    
    def run_regex(self) -> None:
        """Run regex match."""
        self.console.print("\n[bold cyan]Regex Match[/bold cyan]")
        text = input("Enter text to search: ").strip()
        pattern = input("Enter regex pattern: ").strip()
        if text and pattern:
            self.regex_match(text, pattern)
    
    def run_statistics(self) -> None:
        """Run text statistics."""
        self.console.print("\n[bold cyan]Text Statistics[/bold cyan]")
        text = input("Enter text: ").strip()
        if text:
            self.text_statistics(text)
    
    def run_json_format(self) -> None:
        """Run JSON formatting."""
        self.console.print("\n[bold cyan]JSON Format[/bold cyan]")
        json_str = input("Enter JSON string: ").strip()
        if json_str:
            self.format_json(json_str)
    
    def run_url_process(self) -> None:
        """Run URL processing."""
        self.console.print("\n[bold cyan]URL Processing[/bold cyan]")
        url = input("Enter URL: ").strip()
        operation = input("Operation (encode/decode, default encode): ").strip()
        if not operation:
            operation = "encode"
        if url:
            self.process_url(url, operation)
    
    def run_char_count(self) -> None:
        """Run character count."""
        self.console.print("\n[bold cyan]Character Count[/bold cyan]")
        text = input("Enter text: ").strip()
        char = input("Enter character to count (leave blank for total): ").strip()
        if text:
            if char:
                self.count_characters(text, char)
            else:
                self.count_characters(text)
    
    def run_line_ops(self) -> None:
        """Run line operations."""
        self.console.print("\n[bold cyan]Line Operations[/bold cyan]")
        text = input("Enter text: ").strip()
        operation = input("Operation (count/reverse/sort/unique/remove_empty): ").strip()
        if text and operation:
            self.process_lines(text, operation)


def main():
    """Entry point for text tools."""
    tools = TextTools()
    tools.main()


if __name__ == "__main__":
    main()
