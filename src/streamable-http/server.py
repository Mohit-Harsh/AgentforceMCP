from typing import Any
import httpx
from fastmcp import FastMCP
from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth
from dotenv import load_dotenv
from fastapi import FastAPI,Header

app = FastAPI(title="Agentforce MCP Server")

@app.get("/ping")
async def ping() -> str:
    """A simple ping tool to check if the server is running"""
    return "Pong!"

@app.post("/send_message")
async def send_message(message: str, username: str = Header(...),
                       password: str = Header(...),
                       securityToken: str = Header(...)) -> str:

    """Send a message to Agentforce Agent

    Args:
        message: message to be sent to the agent
    """
    try:

        print('Credentials: ', username, password, securityToken)
        
        # Initialize AgentForce client
        auth = BasicAuth(
            username=username,
            password=password,
            security_token=securityToken
        )

        agent_force = Agentforce(auth=auth)

        response = agent_force.send_message(
            agent_name='Copilot_for_Salesforce',
            user_message=message
        )

        return response['agent_response']
    
    except Exception as e:

        print('Exception: ',e)
        return f"Unable to connect to Copilot_for_Salesforce agent"
    
# Initialize FastMCP server
mcp = FastMCP.from_fastapi(app=app,name="AgentforceMCPServer", 
              instructions="Use this MCP server to interact with Agentforce agents.")

if __name__ == "__main__":
    mcp.run(transport='streamable-http')

