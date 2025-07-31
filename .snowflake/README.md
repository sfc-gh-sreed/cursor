# Snowflake Authentication Setup for Cursor Projects

This directory contains all the necessary files for Snowflake authentication and connection management across your Cursor projects.

## 📁 Directory Structure

```
.snowflake/
├── keys/
│   └── snowflake_rsa_key.pem     # Private key for JWT authentication
├── connections.toml              # Connection configurations
└── README.md                     # This file
```

## 🔐 Authentication Method

This setup uses **JWT Key-Pair Authentication** which provides:
- ✅ No browser popups or OAuth complications
- ✅ Secure, programmatic access
- ✅ Reliable connections across all tools
- ✅ No password or MFA prompts

## 🚀 Quick Start

### For VS Code/Cursor:

1. **Install Snowflake Extension**: Install the "Snowflake" extension in VS Code/Cursor
2. **Use Connection**: Select `DEFAULT_SCOTT_KEYPAIR` from the connection dropdown
3. **Connect**: Should connect automatically without any prompts

### For Python Projects:

```python
import snowflake.connector
import os

# Load connection using the key file
conn = snowflake.connector.connect(
    account='SFSENORTHAMERICA-DC202',
    user='scott',
    private_key_path=os.path.expanduser('~/cursor/.snowflake/keys/snowflake_rsa_key.pem'),
    warehouse='SCOTT_WH',
    database='DEMO_DB',
    schema='PUBLIC',
    role='ACCOUNTADMIN'
)
```

### For Other Tools:

Use the connection parameters from `connections.toml` and point to the key file at:
`/Users/sreed/cursor/.snowflake/keys/snowflake_rsa_key.pem`

## 📝 Creating New Project Connections

1. **Copy the template** from `connections.toml`
2. **Modify the parameters** for your specific project needs
3. **Keep using the same key file** (no need to create new keys)

Example for a new project:
```toml
[MY_PROJECT]
name = "MY_PROJECT"
account = "SFSENORTHAMERICA-DC202"
user = "scott"
authenticator = "SNOWFLAKE_JWT"
private_key_path = "/Users/sreed/cursor/.snowflake/keys/snowflake_rsa_key.pem"
warehouse = "MY_PROJECT_WH"
database = "MY_PROJECT_DB"
schema = "PUBLIC"
role = "ACCOUNTADMIN"
```

## 🔒 Security Notes

- Private key has `600` permissions (owner read/write only)
- Key is stored locally and never transmitted
- JWT tokens are generated locally and expire automatically
- No passwords stored in configuration files

## 🛠 Troubleshooting

### Connection Issues:
1. Verify key file exists: `ls -la .snowflake/keys/snowflake_rsa_key.pem`
2. Check permissions: Should show `-rw-------`
3. Restart VS Code completely if using the extension

### For New Machines:
1. Copy this entire `.snowflake/` directory to your new setup
2. Update paths in `connections.toml` if needed
3. Ensure key permissions are set: `chmod 600 .snowflake/keys/snowflake_rsa_key.pem`

## 📋 Available Connections

- **DEFAULT_SCOTT_KEYPAIR**: Primary production connection
- **DC202**: Backup connection with password auth

---

**Note**: This setup is portable and can be copied to any new Cursor project directory for consistent Snowflake access. 