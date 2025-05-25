from fastapi import FastAPI, Request
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount
from starlette.responses import JSONResponse, Response
import logging
from typing import List
from typing import List, Dict
from starlette.responses import PlainTextResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory mock database with 20 leave days to start
employee_leaves = {
    "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
    "E002": {"balance": 20, "history": []}
}

# Initialize FastMCP
mcp = FastMCP("LeaveManager")

# Tool: Check Leave Balance
@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check how many leave days are left for the employee"""
    logging.info(f"Checking leave balance for Employee ID: {employee_id}")
    data = employee_leaves.get(employee_id)
    if data:
        response = f"{employee_id} has {data['balance']} leave days remaining."
        logging.info(f"Balance check result: {response}")
        return response
    logging.warning(f"Employee ID {employee_id} not found.")
    return "Employee ID not found."

# Tool: Apply for Leave with specific dates
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """
    Apply leave for specific dates (e.g., ["2025-04-17", "2025-05-01"])
    """
    logging.info(f"Applying leave for Employee ID: {employee_id} on dates: {leave_dates}")

    if employee_id not in employee_leaves:
        logging.warning(f"Employee ID {employee_id} not found.")
        return "Employee ID not found."

    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_id]["balance"]

    logging.info(f"Requested: {requested_days} day(s), Available: {available_balance} day(s)")

    if available_balance < requested_days:
        response = (f"Insufficient leave balance. You requested {requested_days} day(s) "
                    f"but have only {available_balance}.")
        logging.warning(response)
        return response

    # Deduct balance and add to history
    employee_leaves[employee_id]["balance"] -= requested_days
    employee_leaves[employee_id]["history"].extend(leave_dates)

    logging.info(f"Leave applied. New balance: {employee_leaves[employee_id]['balance']}")
    return f"Leave applied for {requested_days} day(s). Remaining balance: {employee_leaves[employee_id]['balance']}."

# Tool: Get Leave History
@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """Get leave history for the employee"""
    logging.info(f"Fetching leave history for Employee ID: {employee_id}")
    data = employee_leaves.get(employee_id)
    if data:
        history = ', '.join(data['history']) if data['history'] else "No leaves taken."
        response = f"Leave history for {employee_id}: {history}"
        logging.info(f"History fetch result: {response}")
        return response
    logging.warning(f"Employee ID {employee_id} not found.")
    return "Employee ID not found."

# Resource: Greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! How can I assist you with leave management today?"

# Create FastAPI application
app = FastAPI(
    title="Leave Management System",
    description="A FastAPI application with MCP integration for managing employee leaves",
    version="1.0.0"
)


# Create SSE transport instance for handling server-sent events
sse = SseServerTransport("/messages/")

# Mount the /messages path to handle SSE message posting
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))


# Add documentation for the /messages endpoint
@app.get("/messages", tags=["MCP"], include_in_schema=True)
def messages_docs():
    """
    Messages endpoint for SSE communication

    This endpoint is used for posting messages to SSE clients.
    Note: This route is for documentation purposes only.
    The actual implementation is handled by the SSE transport.
    """
    pass  # This is just for documentation, the actual handler is mounted above


@app.get("/sse", tags=["MCP"])
async def handle_sse(request: Request):
    """
    SSE endpoint that connects to the MCP server

    This endpoint establishes a Server-Sent Events connection with the client
    and forwards communication to the Model Context Protocol server.
    """
    # Use sse.connect_sse to establish an SSE connection with the MCP server
    async with sse.connect_sse(request.scope, request.receive, request._send) as (
        read_stream,
        write_stream,
    ):
        # Run the MCP server with the established streams
        await mcp._mcp_server.run(
            read_stream,
            write_stream,
            mcp._mcp_server.create_initialization_options(),
        )


# Import routes at the end to avoid circular imports
# This ensures all routes are registered to the app
import routes  # noqa