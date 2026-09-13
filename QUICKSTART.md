# Terminal Multi Tool - Quick Start Guide

## Installation (Windows)

1. **Double-click `setup.bat`** to install dependencies
   - This will create a virtual environment and install required packages
   - Follow the on-screen prompts

2. **Double-click `start.bat`** to launch the application
   - The application will start in a new terminal window
   - Accept the disclaimer by pressing Enter

## First Run

When you first launch Terminal Multi Tool:

1. You'll see the main dashboard with 7 tool categories
2. Each category is numbered (1-7) for easy selection
3. Press `0` to exit the application

## Quick Examples

### Check IP Geolocation
```
1. Select "IP & Network" (option 4)
2. Choose "IP Geolocation" (option 1)
3. Enter an IP address (e.g., 8.8.8.8)
4. View the geolocation results
```

### Generate a Secure Password
```
1. Select "Crypto & Utils" (option 6)
2. Choose "Secure Password Generator" (option 7)
3. Enter desired length (default 20)
4. Choose character types
5. Copy the generated password
```

### Lookup GitHub User
```
1. Select "OSINT & Research" (option 1)
2. Choose "GitHub User Lookup" (option 2)
3. Enter a GitHub username
4. View user information
```

## Navigation Tips

- **Number keys** - Select menu options
- **Enter** - Confirm input or continue
- **0** - Go back to previous menu
- **Ctrl+C** - Exit application anytime

## Configuration

### API Keys (Optional)
For enhanced features, add API keys to `config/api_keys.yaml`:

```yaml
discord:
  bot_token: "your_token_here"

shodan:
  api_key: "your_key_here"
```

### Settings
Edit `config/config.yaml` to customize:
- UI theme
- Network timeout
- Log level
- Default generator settings

## Troubleshooting

### "Python not found"
- Run `python_installer.bat`
- Or install Python from python.org
- **Important:** Check "Add Python to PATH" during installation

### Module import errors
- Make sure you ran `setup.bat`
- Try running it again
- Check that virtual environment exists

### Network errors
- Check internet connection
- Some APIs may have rate limits
- Configure API keys for better access

## Project Structure

```
Terminal Multi Tool/
├── main.py              # Launch this to run
├── setup.bat            # Run this first
├── start.bat            # Run this to start
├── config/              # Settings and API keys
├── logs/                # Application logs
└── modules/             # All tool modules
```

## Security Notes

- Never share your `api_keys.yaml` file
- The application does not store sensitive data
- Logs are kept in the `logs/` directory
- Always use a virtual environment

## Next Steps

1. Explore each tool category
2. Configure API keys for enhanced features
3. Customize settings in `config.yaml`
4. Read the full README.md for detailed documentation

## Support

For detailed documentation, see `README.md`

---

**Remember:** This tool is for education and authorized research only.