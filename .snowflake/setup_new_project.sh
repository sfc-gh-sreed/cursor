#!/bin/bash

# Snowflake Setup Script for New Cursor Projects
# This script copies the Snowflake authentication setup to a new project directory

set -e

echo "🚀 Snowflake Setup for New Cursor Project"
echo "========================================="

# Check if target directory is provided
if [ $# -eq 0 ]; then
    echo "❌ Error: Please provide the target project directory"
    echo "Usage: ./setup_new_project.sh /path/to/new/project"
    echo "Example: ./setup_new_project.sh ~/cursor/my-new-project"
    exit 1
fi

TARGET_DIR="$1"
SOURCE_DIR="/Users/sreed/cursor/.snowflake"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ Error: Source Snowflake directory not found at $SOURCE_DIR"
    exit 1
fi

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Check if target already has .snowflake directory
if [ -d "$TARGET_DIR/.snowflake" ]; then
    echo "⚠️  Warning: $TARGET_DIR/.snowflake already exists"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Setup cancelled"
        exit 1
    fi
    rm -rf "$TARGET_DIR/.snowflake"
fi

# Copy the entire .snowflake directory
echo "📂 Copying Snowflake configuration..."
cp -r "$SOURCE_DIR" "$TARGET_DIR/"

# Update the connections.toml to use the new project path
NEW_KEY_PATH="$TARGET_DIR/.snowflake/keys/snowflake_rsa_key.pem"
sed -i '' "s|/Users/sreed/cursor/.snowflake/keys/snowflake_rsa_key.pem|$NEW_KEY_PATH|g" "$TARGET_DIR/.snowflake/connections.toml"

# Ensure proper permissions on the key file
chmod 600 "$TARGET_DIR/.snowflake/keys/snowflake_rsa_key.pem"

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. cd $TARGET_DIR"
echo "2. Open the project in Cursor"
echo "3. Use the Snowflake extension with DEFAULT_SCOTT_KEYPAIR connection"
echo ""
echo "📝 To customize connections for this project:"
echo "   Edit: $TARGET_DIR/.snowflake/connections.toml"
echo ""
echo "📖 For more information:"
echo "   Read: $TARGET_DIR/.snowflake/README.md" 