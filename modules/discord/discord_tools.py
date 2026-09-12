"""
Discord Module
Provides server management and moderation utilities
"""

from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.utils.logger import setup_logger
from modules.utils.validators import InputValidator
from modules.utils.error_handler import ErrorHandler, handle_errors
from modules.utils.config import ConfigManager


class DiscordTools:
    """Main class for Discord tools."""
    
    def __init__(self):
        """Initialize Discord tools."""
        self.logger = setup_logger()
        self.validator = InputValidator()
        self.error_handler = ErrorHandler()
        self.console = Console()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.client = None
        
        # Try to import discord.py
        try:
            import discord
            self.discord = discord
            self.discord_available = True
        except ImportError:
            self.discord_available = False
            self.console.print("[yellow]discord.py not installed. Install with: pip install discord.py[/yellow]")
    
    @handle_errors("Discord bot connection", show_user=True)
    def connect_bot(self, token: str) -> bool:
        """
        Connect to Discord using bot token.
        
        Args:
            token: Discord bot token
            
        Returns:
            True if successful, False otherwise
        """
        if not self.discord_available:
            self.console.print("[red]discord.py not available[/red]")
            return False
        
        try:
            # Define intents
            intents = self.discord.Intents.default()
            intents.message_content = True
            intents.guilds = True
            intents.members = True
            
            self.client = self.discord.Client(intents=intents)
            
            @self.client.event
            async def on_ready():
                self.console.print(f"[green]Connected as {self.client.user}[/green]")
            
            # Run the bot (this would normally be async)
            self.console.print("[cyan]Bot connection requires async context[/cyan]")
            self.console.print("[yellow]This is a placeholder for full bot implementation[/yellow]")
            
            return True
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Discord bot connection")
            self.console.print(f"[red]Error connecting to Discord: {e}[/red]")
            return False
    
    @handle_errors("Server info lookup", show_user=True)
    def get_server_info(self, server_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a Discord server.
        
        Args:
            server_id: Discord server ID
            
        Returns:
            Server information or None on error
        """
        if not self.validator.validate_discord_id(server_id):
            self.console.print("[red]Invalid Discord server ID format[/red]")
            return None
        
        self.console.print("[cyan]Server info lookup requires connected bot[/cyan]")
        self.console.print("[yellow]This is a placeholder for full implementation[/yellow]")
        
        # Placeholder response
        return {
            'server_id': server_id,
            'name': 'Server Name (requires bot connection)',
            'member_count': 0,
            'channel_count': 0
        }
    
    @handle_errors("User info lookup", show_user=True)
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a Discord user.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            User information or None on error
        """
        if not self.validator.validate_discord_id(user_id):
            self.console.print("[red]Invalid Discord user ID format[/red]")
            return None
        
        self.console.print("[cyan]User info lookup requires connected bot[/cyan]")
        self.console.print("[yellow]This is a placeholder for full implementation[/yellow]")
        
        # Placeholder response
        return {
            'user_id': user_id,
            'username': 'Username (requires bot connection)',
            'discriminator': '0000',
            'avatar': None
        }
    
    @handle_errors("Invite link generator", show_user=True)
    def generate_invite_link(self, server_id: str, permissions: int = 0) -> Optional[str]:
        """
        Generate a Discord server invite link.
        
        Args:
            server_id: Discord server ID
            permissions: Permission level for the invite
            
        Returns:
            Invite link or None on error
        """
        if not self.validator.validate_discord_id(server_id):
            self.console.print("[red]Invalid Discord server ID format[/red]")
            return None
        
        # Generate a standard invite link format
        invite_link = f"https://discord.gg/{server_id}"
        
        self.console.print(f"[green]Generated invite link: {invite_link}[/green]")
        self.console.print("[yellow]Note: This is a formatted link. Actual invites require bot API access[/yellow]")
        
        return invite_link
    
    @handle_errors("Permission calculator", show_user=True)
    def calculate_permissions(self, permission_bits: str) -> Optional[Dict[str, Any]]:
        """
        Calculate Discord permissions from permission bits.
        
        Args:
            permission_bits: Permission bits as string or integer
            
        Returns:
            Permission breakdown or None on error
        """
        try:
            permissions = int(permission_bits)
            
            # Permission flags (simplified)
            permission_flags = {
                1 << 0: "CREATE_INSTANT_INVITE",
                1 << 1: "KICK_MEMBERS",
                1 << 2: "BAN_MEMBERS",
                1 << 3: "ADMINISTRATOR",
                1 << 4: "MANAGE_CHANNELS",
                1 << 5: "MANAGE_GUILD",
                1 << 6: "ADD_REACTIONS",
                1 << 7: "VIEW_AUDIT_LOG",
                1 << 8: "PRIORITY_SPEAKER",
                1 << 10: "SEND_MESSAGES",
                1 << 11: "SEND_TTS_MESSAGES",
                1 << 12: "MANAGE_MESSAGES",
                1 << 13: "EMBED_LINKS",
                1 << 14: "ATTACH_FILES",
                1 << 15: "READ_MESSAGE_HISTORY",
                1 << 16: "MENTION_EVERYONE",
                1 << 17: "EXTERNAL_EMOJIS",
                1 << 18: "VIEW_GUILD_INSIGHTS",
            }
            
            active_permissions = []
            for bit, name in permission_flags.items():
                if permissions & bit:
                    active_permissions.append(name)
            
            self.display_permissions(active_permissions, permissions)
            
            return {
                'bits': permissions,
                'permissions': active_permissions
            }
            
        except ValueError:
            self.console.print("[red]Invalid permission bits format[/red]")
            return None
        except Exception as e:
            self.error_handler.handle_exception(e, "Permission calculator")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_permissions(self, permissions: List[str], bits: int) -> None:
        """Display permission breakdown."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Permission Bits", style="cyan")
        table.add_column("Active Permissions", style="green")
        
        table.add_row(str(bits), ', '.join(permissions[:10]))
        
        if len(permissions) > 10:
            table.add_row("", f"... and {len(permissions) - 10} more")
        
        self.console.print(Panel(table, title="[bold]Permission Breakdown[/bold]"))
    
    @handle_errors("Snowflake timestamp", show_user=True)
    def get_snowflake_timestamp(self, snowflake: str) -> Optional[Dict[str, Any]]:
        """
        Get timestamp from Discord snowflake ID.
        
        Args:
            snowflake: Discord snowflake ID
            
        Returns:
            Timestamp information or None on error
        """
        if not self.validator.validate_discord_id(snowflake):
            self.console.print("[red]Invalid Discord snowflake format[/red]")
            return None
        
        try:
            snowflake_int = int(snowflake)
            
            # Discord epoch: 2015-01-01 00:00:00 UTC
            discord_epoch = 1420070400000
            
            # Extract timestamp (first 42 bits)
            timestamp = (snowflake_int >> 22) + discord_epoch
            
            from datetime import datetime
            dt = datetime.fromtimestamp(timestamp / 1000)
            
            result = {
                'snowflake': snowflake,
                'timestamp': timestamp,
                'datetime': dt.strftime('%Y-%m-%d %H:%M:%S UTC'),
                'worker_id': (snowflake_int & 0x3E0000) >> 17,
                'process_id': (snowflake_int & 0x1F000) >> 12,
                'sequence': snowflake_int & 0xFFF
            }
            
            self.display_snowflake_info(result)
            return result
            
        except Exception as e:
            self.error_handler.handle_exception(e, "Snowflake timestamp")
            self.console.print(f"[red]Error: {e}[/red]")
            return None
    
    def display_snowflake_info(self, data: Dict[str, Any]) -> None:
        """Display snowflake information."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Snowflake", data.get('snowflake', 'N/A'))
        table.add_row("Timestamp", data.get('datetime', 'N/A'))
        table.add_row("Worker ID", str(data.get('worker_id', 'N/A')))
        table.add_row("Process ID", str(data.get('process_id', 'N/A')))
        table.add_row("Sequence", str(data.get('sequence', 'N/A')))
        
        self.console.print(Panel(table, title="[bold]Snowflake Information[/bold]"))
    
    def main(self) -> None:
        """Main entry point for Discord module."""
        tools = [
            {
                'name': 'Bot Connection',
                'description': 'Connect Discord bot (requires token)',
                'function': self.run_bot_connection
            },
            {
                'name': 'Server Info',
                'description': 'Get Discord server information',
                'function': self.run_server_info
            },
            {
                'name': 'User Info',
                'description': 'Get Discord user information',
                'function': self.run_user_info
            },
            {
                'name': 'Invite Link Generator',
                'description': 'Generate server invite links',
                'function': self.run_invite_generator
            },
            {
                'name': 'Permission Calculator',
                'description': 'Calculate permissions from bits',
                'function': self.run_permission_calculator
            },
            {
                'name': 'Snowflake Timestamp',
                'description': 'Get timestamp from snowflake ID',
                'function': self.run_snowflake_timestamp
            }
        ]
        
        while True:
            from modules.ui.dashboard import Dashboard
            dashboard = Dashboard(self.config)
            choice = dashboard.display_module_menu("Discord", tools)
            
            if choice is None:
                break
            
            try:
                choice['function']()
            except Exception as e:
                self.error_handler.handle_exception(e, choice['name'])
                self.console.print(f"[red]Error: {e}[/red]")
            
            input("\nPress Enter to continue...")
    
    def run_bot_connection(self) -> None:
        """Run bot connection."""
        self.console.print("\n[bold cyan]Discord Bot Connection[/bold cyan]")
        token = input("Enter Discord bot token (leave blank to skip): ").strip()
        if token:
            self.connect_bot(token)
    
    def run_server_info(self) -> None:
        """Run server info lookup."""
        self.console.print("\n[bold cyan]Server Info Lookup[/bold cyan]")
        server_id = input("Enter Discord server ID: ").strip()
        if server_id:
            self.get_server_info(server_id)
    
    def run_user_info(self) -> None:
        """Run user info lookup."""
        self.console.print("\n[bold cyan]User Info Lookup[/bold cyan]")
        user_id = input("Enter Discord user ID: ").strip()
        if user_id:
            self.get_user_info(user_id)
    
    def run_invite_generator(self) -> None:
        """Run invite link generator."""
        self.console.print("\n[bold cyan]Invite Link Generator[/bold cyan]")
        server_id = input("Enter Discord server ID: ").strip()
        if server_id:
            self.generate_invite_link(server_id)
    
    def run_permission_calculator(self) -> None:
        """Run permission calculator."""
        self.console.print("\n[bold cyan]Permission Calculator[/bold cyan]")
        bits = input("Enter permission bits (integer): ").strip()
        if bits:
            self.calculate_permissions(bits)
    
    def run_snowflake_timestamp(self) -> None:
        """Run snowflake timestamp."""
        self.console.print("\n[bold cyan]Snowflake Timestamp[/bold cyan]")
        snowflake = input("Enter Discord snowflake ID: ").strip()
        if snowflake:
            self.get_snowflake_timestamp(snowflake)


def main():
    """Entry point for Discord module."""
    discord = DiscordTools()
    discord.main()


if __name__ == "__main__":
    main()