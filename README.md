# Void - Terminal-Based Multitool Application

A comprehensive terminal-based multitool application inspired by Void-Tools, providing a Rich TUI (Terminal User Interface) dashboard organizing various utilities for OSINT research, network diagnostics, Discord helpers, generators, and CLI tools.

**Created by Yinuo**

## ⚠️ DISCLAIMER

**This tool is for education and authorized research only. Use only on systems you own or have explicit permission to test.**

The developers of this application are not responsible for misuse of these tools or any consequences resulting from such misuse. Always obtain proper authorization before conducting any research and respect privacy laws and regulations.

## Features

### Tool Categories

1. **OSINT & Research** - Public-data lookups and open-source intelligence tools
   - Email reputation checking
   - GitHub user lookup
   - Domain research
   - Username search across platforms

2. **Utilities** - Productivity and network-related helpers
   - Ping host connectivity testing
   - DNS lookup
   - Port scanning
   - System information display
   - HTTP headers checking

3. **Discord** - Server management and moderation utilities
   - Bot connection (requires token)
   - Server info lookup
   - User info lookup
   - Invite link generation
   - Permission calculator
   - Snowflake timestamp extraction

4. **IP & Network** - IP geolocation, WHOIS info, port checks
   - IP geolocation lookup
   - WHOIS information
   - Reverse DNS lookup
   - HTTP(S) port checking
   - Blacklist checking

5. **Generators** - Demo/format generators for educational purposes
   - UUID generation
   - Password generation
   - API key generation
   - JSON data generation
   - Timestamp generation
   - Lorem ipsum text generation
   - Hash generation

6. **Crypto & Utils** - Hash tools, password generation, temporary email helpers
   - MD5, SHA1, SHA256, SHA512 hashing
   - Base64 encoding/decoding
   - Secure password generation
   - Password strength checking
   - Temporary email service information
   - Token generation
   - HMAC generation

7. **Security Testing** - Network testing and security analysis tools
   - Connection rate testing (legitimate load testing)
   - Network latency analysis
   - Active connection monitoring
   - Bandwidth estimation
   - Port availability scanning
   - DNS resolution testing

8. **Defensive Security** - Security auditing and monitoring tools
   - SSL/TLS certificate analysis
   - Security header analysis
   - Port security scanning
   - File integrity checking
   - Security log analysis
   - Network security baseline checks

9. **Resource Links** - Curated public OSINT and research bookmarks
   - OSINT tools directory
   - Social media intelligence resources
   - Domain & DNS tools
   - Geolocation services
   - Specialized search engines
   - Data breach resources
   - And more...

## Installation

### Prerequisites

- Python 3.11 or higher
- Windows (batch scripts provided)
- Optional: Node.js (for certain features)

### Quick Start (Windows)

1. Navigate to the Void directory
2. Run `setup.bat` to install dependencies
3. Run `start.bat` to launch the application

### Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Python Installation

If Python is not installed, run `python_installer.bat` or download Python from [python.org](https://www.python.org/downloads/).

**Important:** During Python installation, check the box "Add Python to PATH".

## Configuration

### Application Settings

Edit `config/config.yaml` to customize application settings:

```yaml
app:
  name: Void
  version: 1.0.0
  debug: false
  log_level: INFO

ui:
  theme: dark
  refresh_rate: 1.0
  max_history: 100

network:
  timeout: 30
  max_retries: 3
  user_agent: Void/1.0
```

### API Keys

For enhanced functionality, add API keys to `config/api_keys.yaml`:

```yaml
discord:
  bot_token: "your_discord_bot_token"

virustotal:
  api_key: "your_virustotal_api_key"

shodan:
  api_key: "your_shodan_api_key"
```

**Warning:** Never commit `api_keys.yaml` to version control. This file is already included in `.gitignore`.

## Usage

### Starting the Application

Run `start.bat` (Windows) or `python main.py` (cross-platform).

### Navigation

1. Use the main menu to select a tool category
2. Navigate within each category using the numbered options
3. Press `0` to return to the previous menu
4. Press `Ctrl+C` to exit the application at any time

### Example Workflow

```
1. Launch the application
2. Select "IP & Network" (option 4)
3. Choose "IP Geolocation" (option 1)
4. Enter an IP address to lookup
5. View the results
6. Press Enter to continue
7. Select another tool or return to main menu
```

## Project Structure

```
Void/
├── main.py                 # Application entry point
├── setup.bat              # Installation script
├── start.bat              # Application launcher
├── python_installer.bat   # Python installation helper
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
├── config/               # Configuration files
│   ├── config.yaml       # Main configuration
│   └── api_keys.yaml     # API keys (not in git)
├── logs/                 # Application logs
└── modules/              # Application modules
    ├── ui/              # User interface
    │   └── dashboard.py # Main TUI dashboard
    ├── utils/           # Utility functions
    │   ├── logger.py    # Logging setup
    │   ├── config.py    # Configuration management
    │   ├── validators.py # Input validation
    │   └── error_handler.py # Error handling
    ├── osint/           # OSINT tools
    ├── utilities/       # General utilities
    ├── discord/         # Discord tools
    ├── network/         # Network tools
    ├── generators/      # Generator tools
    ├── crypto/          # Crypto utilities
    └── resources/       # Resource links
```

## Development

### Adding New Tools

1. Create a new module in the appropriate directory under `modules/`
2. Implement the tool class with appropriate methods
3. Add entry points and menu integration
4. Update the main dashboard to include the new category

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Implement proper error handling
- Validate all user inputs

### Testing

Test individual modules by running them directly:

```bash
python modules/osint/osint_tools.py
python modules/network/network_tools.py
```

## Dependencies

### Core Dependencies

- `rich>=13.7.0` - Terminal UI framework
- `textual>=0.47.0` - Advanced TUI components
- `requests>=2.31.0` - HTTP requests
- `aiohttp>=3.9.0` - Async HTTP client
- `pyyaml>=6.0.1` - YAML configuration parsing
- `python-dotenv>=1.0.0` - Environment variable management

### Module-Specific Dependencies

- `discord.py>=2.3.0` - Discord API client
- `dnspython>=2.4.2` - DNS queries
- `whois>=0.9.27` - WHOIS lookups
- `cryptography>=41.0.0` - Cryptographic operations
- `passlib>=1.7.4` - Password hashing
- `validators>=0.22.0` - Input validation
- `pyperclip>=1.8.2` - Clipboard operations

## Troubleshooting

### Common Issues

**Python not found:**
- Run `python_installer.bat` or install Python from python.org
- Ensure "Add Python to PATH" is checked during installation

**Module import errors:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Network errors:**
- Check internet connection
- Verify API keys are configured in `config/api_keys.yaml`
- Some APIs may have rate limits

**Permission errors:**
- Run as administrator if needed (not recommended for security)
- Check file permissions in the Void directory

## Security Considerations

1. **API Keys:** Never share or commit API keys to version control
2. **Network Traffic:** Be aware that some tools make network requests
3. **Input Validation:** All user inputs are validated, but use caution
4. **Logging:** Sensitive data is not logged, but check logs directory
5. **Virtual Environment:** Always use a virtual environment

## Legal and Ethical Use

This application is designed for:

- Educational purposes and learning
- Authorized security research
- Testing systems you own or have permission to test
- Legitimate business intelligence gathering

**Unauthorized use is illegal and unethical.** Always:

- Obtain proper authorization before conducting research
- Respect privacy laws and regulations
- Follow platform terms of service
- Report vulnerabilities responsibly
- Use skills for constructive purposes

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper documentation
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational purposes. Use responsibly and in accordance with applicable laws and regulations.

## Support

For issues, questions, or contributions, please refer to the project repository or documentation.

## Credits

**Created by Yinuo**

This project was designed and developed by Yinuo as a comprehensive terminal-based multitool application for educational and authorized research purposes.

## Acknowledgments

- Inspired by Void-Tools and similar OSINT frameworks
- Built with Rich library for beautiful terminal interfaces
- Uses various public APIs for data lookup
- Community-contributed OSINT resources

## Version History

- **1.0.0** - Initial release
  - Core TUI dashboard
  - 7 tool categories
  - Configuration management
  - Error handling and validation
  - Windows batch installation scripts

---

**Remember:** With great power comes great responsibility. Use these tools ethically and legally.