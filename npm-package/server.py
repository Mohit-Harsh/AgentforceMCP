from typing import Any
from mcp.server.fastmcp import FastMCP
from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth
import argparse

# Create the argument parser
parser = argparse.ArgumentParser(
    description="Parse Salesforce login credentials from CLI arguments"
)

# Define the arguments
parser.add_argument(
    "--username",
    type=str,
    required=True,
    help="Salesforce username"
)

parser.add_argument(
    "--password",
    type=str,
    required=True,
    help="Salesforce password"
)

parser.add_argument(
    "--securityToken",
    type=str,
    required=True,
    help="Salesforce security token"
)


# Initialize FastMCP server
mcp = FastMCP("AgentForce MCP")


@mcp.tool()
async def send_message(name: str, message: str) -> str:

    """Send a message to agentforce agent

    Args:
        name: Name of the agentforce agent
        message: message to be sent to the agent
    """
    try:

        # Parse the arguments
        args = parser.parse_args()
        
        # Initialize AgentForce client
        auth = BasicAuth(
            username=args.username,
            password=args.password,
            security_token=args.securityToken
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

if __name__ == "__main__":
    mcp.run(transport='stdio')

    

