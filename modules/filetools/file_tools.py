"""
File Management Tools Module
Provides file operations and management utilities
Created by Yinuo
"""

import os
import shutil
import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class FileTools:
    """Main class for file management tools."""
    
    def __init__(self):
        """Initialize file tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
    
    @handle_errors("File hash calculation", show_user=True)
    def calculate_file_hash(self, file_path: str, algorithm: str = "sha256") -> Optional[Dict[str, Any]]:
        """
        Calculate hash of a file.
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm (md5, sha1, sha256, sha512)
            
        Returns:
            Hash information or None on error
        """
        try:
            path = Path(file_path)
            if not path.exists():
                self.console.print(f"[red]File not found: {file_path}[/red]")
                return None
            
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
            
            self.display_file_hash(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "File hash calculation")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_file_hash(self, data: Dict[str, Any]) -> None:
        """Display file hash results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("File", data['file_path'])
        table.add_row("Algorithm", data['algorithm'].upper())
        table.add_row("Hash", data['hash'])
        table.add_row("Size", f"{data['file_size']} bytes")
        table.add_row("Timestamp", data['timestamp'])
        
        self.console.print(Panel(table, title="[bold]File Hash[/bold]"))
    
    @handle_errors("File search", show_user=True)
    def search_files(self, directory: str, pattern: str, search_content: bool = False) -> Optional[List[str]]:
        """
        Search for files by name or content.
        
        Args:
            directory: Directory to search
            pattern: Search pattern
            search_content: Search file contents instead of names
            
        Returns:
            List of matching files or None on error
        """
        try:
            path = Path(directory)
            if not path.exists():
                self.console.print(f"[red]Directory not found: {directory}[/red]")
                return None
            
            self.console.print(f"[cyan]Searching in {directory}...[/cyan]")
            
            import re
            matches = []
            
            if search_content:
                # Search file contents
                for file_path in path.rglob('*'):
                    if file_path.is_file():
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if re.search(pattern, content, re.IGNORECASE):
                                    matches.append(str(file_path))
                                    self.console.print(f"[green]Found: {file_path}[/green]")
                        except:
                            pass
            else:
                # Search file names
                for file_path in path.rglob(pattern):
                    if file_path.is_file():
                        matches.append(str(file_path))
                        self.console.print(f"[green]Found: {file_path}[/green]")
            
            self.display_search_results(matches, pattern)
            return matches
            
        except Exception as e:
            self.error_handler.handle_exception(e, "File search")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_search_results(self, matches: List[str], pattern: str) -> None:
        """Display search results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan")
        table.add_column("File", style="green")
        
        for i, match in enumerate(matches[:20], 1):
            table.add_row(str(i), match)
        
        if len(matches) > 20:
            table.add_row("", f"... and {len(matches) - 20} more")
        
        self.console.print(Panel(table, title=f"[bold]Search Results for '{pattern}'[/bold]"))
        self.console.print(f"[green]Total matches: {len(matches)}[/green]")
    
    @handle_errors("File duplicates finder", show_user=True)
    def find_duplicates(self, directory: str) -> Optional[Dict[str, List[str]]]:
        """
        Find duplicate files by hash.
        
        Args:
            directory: Directory to scan
            
        Returns:
            Dictionary of hash to file paths or None on error
        """
        try:
            path = Path(directory)
            if not path.exists():
                self.console.print(f"[red]Directory not found: {directory}[/red]")
                return None
            
            self.console.print(f"[cyan]Scanning for duplicates in {directory}...[/cyan]")
            
            file_hashes = {}
            
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    try:
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.md5()
                            while chunk := f.read(8192):
                                file_hash.update(chunk)
                            hash_hex = file_hash.hexdigest()
                        
                        if hash_hex in file_hashes:
                            file_hashes[hash_hex].append(str(file_path))
                        else:
                            file_hashes[hash_hex] = [str(file_path)]
                    except:
                        pass
            
            # Find duplicates
            duplicates = {k: v for k, v in file_hashes.items() if len(v) > 1}
            
            self.display_duplicates(duplicates)
            return duplicates
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Duplicate finder")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_duplicates(self, duplicates: Dict[str, List[str]]) -> None:
        """Display duplicate files."""
        if not duplicates:
            self.console.print("[green]No duplicate files found[/green]")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Hash", style="cyan")
        table.add_column("Files", style="green")
        
        for hash_val, files in duplicates.items():
            table.add_row(hash_val[:16] + "...", "\n".join(files[:3]))
        
        self.console.print(Panel(table, title=f"[bold]Duplicate Files ({len(duplicates)} groups)[/bold]"))
    
    @handle_errors("File size analysis", show_user=True)
    def analyze_directory_size(self, directory: str) -> Optional[Dict[str, Any]]:
        """
        Analyze directory size and file distribution.
        
        Args:
            directory: Directory to analyze
            
        Returns:
            Size analysis or None on error
        """
        try:
            path = Path(directory)
            if not path.exists():
                self.console.print(f"[red]Directory not found: {directory}[/red]")
                return None
            
            self.console.print(f"[cyan]Analyzing directory: {directory}[/cyan]")
            
            total_size = 0
            file_count = 0
            dir_count = 0
            file_types = {}
            
            for item in path.rglob('*'):
                if item.is_file():
                    size = item.stat().st_size
                    total_size += size
                    file_count += 1
                    
                    # Get file type
                    mime_type = mimetypes.guess_type(str(item))[0] or "unknown"
                    file_types[mime_type] = file_types.get(mime_type, 0) + size
                elif item.is_dir():
                    dir_count += 1
            
            results = {
                'directory': directory,
                'total_size': total_size,
                'file_count': file_count,
                'directory_count': dir_count,
                'file_types': file_types,
                'average_file_size': total_size / file_count if file_count > 0 else 0
            }
            
            self.display_directory_analysis(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Directory analysis")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_directory_analysis(self, data: Dict[str, Any]) -> None:
        """Display directory analysis."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Directory", data['directory'])
        table.add_row("Total Size", self.format_size(data['total_size']))
        table.add_row("File Count", str(data['file_count']))
        table.add_row("Directory Count", str(data['directory_count']))
        table.add_row("Average File Size", self.format_size(data['average_file_size']))
        
        self.console.print(Panel(table, title="[bold]Directory Analysis[/bold]"))
        
        # File type breakdown
        if data['file_types']:
            type_table = Table(show_header=True, header_style="bold magenta")
            type_table.add_column("File Type", style="cyan")
            type_table.add_column("Size", style="green")
            type_table.add_column("Percentage", style="yellow")
            
            for file_type, size in sorted(data['file_types'].items(), key=lambda x: x[1], reverse=True)[:10]:
                percentage = (size / data['total_size'] * 100) if data['total_size'] > 0 else 0
                type_table.add_row(file_type, self.format_size(size), f"{percentage:.1f}%")
            
            self.console.print(Panel(type_table, title="[bold]File Type Breakdown[/bold]"))
    
    def format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable size."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} PB"
    
    @handle_errors("Batch file rename", show_user=True)
    def batch_rename(self, directory: str, pattern: str, replacement: str) -> Optional[int]:
        """
        Batch rename files in directory.
        
        Args:
            directory: Directory containing files
            pattern: Pattern to replace
            replacement: Replacement string
            
        Returns:
            Number of files renamed or None on error
        """
        try:
            path = Path(directory)
            if not path.exists():
                self.console.print(f"[red]Directory not found: {directory}[/red]")
                return None
            
            self.console.print(f"[cyan]Batch renaming in {directory}[/cyan]")
            self.console.print(f"Pattern: '{pattern}' -> '{replacement}'")
            
            import re
            renamed_count = 0
            
            for file_path in path.iterdir():
                if file_path.is_file():
                    old_name = file_path.name
                    new_name = re.sub(pattern, replacement, old_name)
                    
                    if old_name != new_name:
                        new_path = file_path.parent / new_name
                        file_path.rename(new_path)
                        renamed_count += 1
                        self.console.print(f"[green]Renamed: {old_name} -> {new_name}[/green]")
            
            self.console.print(f"[green]Total files renamed: {renamed_count}[/green]")
            return renamed_count
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Batch rename")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    @handle_errors("File permissions check", show_user=True)
    def check_permissions(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Check file permissions.
        
        Args:
            file_path: Path to file
            
        Returns:
            Permission information or None on error
        """
        try:
            path = Path(file_path)
            if not path.exists():
                self.console.print(f"[red]File not found: {file_path}[/red]")
                return None
            
            # Get file stats
            stat_info = path.stat()
            
            results = {
                'file_path': file_path,
                'size': stat_info.st_size,
                'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                'permissions': oct(stat_info.st_mode)[-3:],
                'is_readable': os.access(file_path, os.R_OK),
                'is_writable': os.access(file_path, os.W_OK),
                'is_executable': os.access(file_path, os.X_OK)
            }
            
            self.display_permissions(results)
            return results
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Permissions check")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_permissions(self, data: Dict[str, Any]) -> None:
        """Display file permissions."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("File", data['file_path'])
        table.add_row("Size", self.format_size(data['size']))
        table.add_row("Modified", data['modified'])
        table.add_row("Permissions", data['permissions'])
        table.add_row("Readable", str(data['is_readable']))
        table.add_row("Writable", str(data['is_writable']))
        table.add_row("Executable", str(data['is_executable']))
        
        self.console.print(Panel(table, title="[bold]File Permissions[/bold]"))
    
    @handle_errors("Empty directories cleaner", show_user=True)
    def clean_empty_dirs(self, directory: str) -> Optional[int]:
        """
        Find and optionally remove empty directories.
        
        Args:
            directory: Directory to scan
            
        Returns:
            Number of empty directories found
        """
        try:
            path = Path(directory)
            if not path.exists():
                self.console.print(f"[red]Directory not found: {directory}[/red]")
                return None
            
            self.console.print(f"[cyan]Scanning for empty directories in {directory}...[/cyan]")
            
            empty_dirs = []
            
            for dir_path in path.rglob('*'):
                if dir_path.is_dir():
                    # Check if directory is empty
                    if not any(dir_path.iterdir()):
                        empty_dirs.append(str(dir_path))
                        self.console.print(f"[yellow]Empty: {dir_path}[/yellow]")
            
            self.console.print(f"[green]Found {len(empty_dirs)} empty directories[/green]")
            return len(empty_dirs)
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Empty dirs cleaner")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def main(self) -> None:
        """Main entry point for file tools."""
        tools = [
            {
                'name': 'File Hash',
                'description': 'Calculate file hash',
                'function': self.run_file_hash
            },
            {
                'name': 'Search Files',
                'description': 'Search files by name or content',
                'function': self.run_file_search
            },
            {
                'name': 'Find Duplicates',
                'description': 'Find duplicate files by hash',
                'function': self.run_find_duplicates
            },
            {
                'name': 'Directory Analysis',
                'description': 'Analyze directory size and contents',
                'function': self.run_directory_analysis
            },
            {
                'name': 'Batch Rename',
                'description': 'Batch rename files',
                'function': self.run_batch_rename
            },
            {
                'name': 'Check Permissions',
                'description': 'Check file permissions',
                'function': self.run_permissions
            },
            {
                'name': 'Clean Empty Dirs',
                'description': 'Find empty directories',
                'function': self.run_clean_empty_dirs
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("File Tools", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_file_hash(self) -> None:
        """Run file hash."""
        self.console.print("\n[bold cyan]File Hash[/bold cyan]")
        file_path = input("Enter file path: ").strip()
        algorithm = input("Enter algorithm (md5/sha1/sha256/sha512, default sha256): ").strip()
        if not algorithm:
            algorithm = "sha256"
        if file_path:
            self.calculate_file_hash(file_path, algorithm)
    
    def run_file_search(self) -> None:
        """Run file search."""
        self.console.print("\n[bold cyan]File Search[/bold cyan]")
        directory = input("Enter directory: ").strip()
        pattern = input("Enter search pattern: ").strip()
        search_content = input("Search file contents? (y/n, default n): ").strip().lower() == 'y'
        if directory and pattern:
            self.search_files(directory, pattern, search_content)
    
    def run_find_duplicates(self) -> None:
        """Run find duplicates."""
        self.console.print("\n[bold cyan]Find Duplicates[/bold cyan]")
        directory = input("Enter directory: ").strip()
        if directory:
            self.find_duplicates(directory)
    
    def run_directory_analysis(self) -> None:
        """Run directory analysis."""
        self.console.print("\n[bold cyan]Directory Analysis[/bold cyan]")
        directory = input("Enter directory: ").strip()
        if directory:
            self.analyze_directory_size(directory)
    
    def run_batch_rename(self) -> None:
        """Run batch rename."""
        self.console.print("\n[bold cyan]Batch Rename[/bold cyan]")
        directory = input("Enter directory: ").strip()
        pattern = input("Enter pattern to replace: ").strip()
        replacement = input("Enter replacement: ").strip()
        if directory and pattern:
            self.batch_rename(directory, pattern, replacement)
    
    def run_permissions(self) -> None:
        """Run permissions check."""
        self.console.print("\n[bold cyan]Check Permissions[/bold cyan]")
        file_path = input("Enter file path: ").strip()
        if file_path:
            self.check_permissions(file_path)
    
    def run_clean_empty_dirs(self) -> None:
        """Run clean empty dirs."""
        self.console.print("\n[bold cyan]Clean Empty Directories[/bold cyan]")
        directory = input("Enter directory: ").strip()
        if directory:
            self.clean_empty_dirs(directory)


def main():
    """Entry point for file tools."""
    tools = FileTools()
    tools.main()


if __name__ == "__main__":
    main()