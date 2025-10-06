from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth, DirectAuth, JwtBearerAuth, SalesforceLogin, ClientCredentialsAuth
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("AgentForce MCP", host='localhost', port=8000)


@mcp.tool()
async def send_message(name: str, message: str) -> str:

    """Send a message to agentforce agent

    Args:
        name: Name of the agentforce agent
        message: message to be sent to the agent
    """
    try:
        
        # Initialize AgentForce client
        auth = BasicAuth(
            username=os.getenv("UNAME"),
            password=os.getenv("PASSWORD"),
            security_token=os.getenv("SECURITY_TOKEN")
        )

        agent_force = Agentforce(auth=auth)

        response = agent_force.send_message(
            agent_name=name,
            user_message=message
        )

        return response['agent_response']
    
    except Exception as e:

        print('Exception: ',e)
        return f"Unable to connect to {name} agent"
    
def main():
    # Initialize and run the server
    mcp.run(transport='streamable-http')

if __name__ == "__main__":
    main()

    

