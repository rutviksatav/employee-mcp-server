# MCP Server Employee Leaves

This is a Flask-based REST API server for managing employee leaves in the MCP system. The server provides endpoints for handling leave requests, approvals, and employee management.

## Project Structure

```
├── app.py              # Main application logic and database models
├── routes.py           # API route definitions
├── server.py           # Server initialization and configuration
├── requirements.txt    # Python dependencies
└── openapi.yaml       # API documentation
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

1. Make sure your virtual environment is activated

2. Start the server:
   ```bash
   python server.py
   ```

## Configuring MCP Server in Cursor AI

To use the MCP server with Cursor AI, you need to add its configuration to the `.cursor/mcp.json` file in your workspace root. If the file doesn't exist, create it.

Here's an example configuration:

```json
{
    "mcpServers": {
      "server-name": {
        "url": "http://127.0.0.1:8000/sse"
      }
    }
  }
```

Replace `"server-name"` with a descriptive name for your server.
