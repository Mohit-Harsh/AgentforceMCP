import uuid
from fastmcp import FastMCP
import requests
from typing import Any
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.auth import OAuthProxy
from fastmcp.server.auth.providers.jwt import JWTVerifier

load_dotenv()

app = FastAPI(title="Agentforce MCP Server")



# Configure token verification for your provider
# See the Token Verification guide for provider-specific setups
token_verifier = JWTVerifier(
    jwks_uri="https://login.salesforce.com/id/keys",
    issuer="https://login.salesforce.com",
    audience="3MVG9JJwBBbcN47IrefxgGiTNdY5a0b.ux1IQPul7xw51Q2SQtLGjxRgcoQb.EIO33e1wXNVG5LyIU5bG9fQU"
)

# Create the OAuth proxy
auth = OAuthProxy(
    # Provider's OAuth endpoints (from their documentation)
    upstream_authorization_endpoint="https://login.salesforce.com/services/oauth2/authorize",
    upstream_token_endpoint="https://login.salesforce.com/services/oauth2/token",

    # Your registered app credentials
    upstream_client_id=os.getenv("CLIENT_ID"),
    upstream_client_secret=os.getenv("CLIENT_SECRET"),

    # Token validation (see Token Verification guide)
    token_verifier=token_verifier,

    # Your FastMCP server's public URL
    base_url="https://2stmqvtv-8000.inc1.devtunnels.ms",

    # Optional: customize the callback path (default is "/auth/callback")
    # redirect_path="/custom/callback",
)

def createSession(agentId:str,token:str,domainUrl:str)->Any:

    url = f"https://api.salesforce.com/einstein/ai-agent/v1/agents/{agentId}/sessions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "externalSessionKey": str(uuid.uuid4()),  # Generates a random UUID
        "instanceConfig": {
            "endpoint": f"https://{domainUrl}"
        },
        "streamingCapabilities": {
            "chunkTypes": ["Text"]
        },
        "bypassUser": True
    }

    response = requests.post(url, json=payload, headers=headers)

    if(response.status_code != 200):
        
        raise Exception(f"Failed to create session: {response.text}")

    return response.json()

def deleteSession(session_id:str,token:str)->Any:

    url = f"https://api.salesforce.com/einstein/ai-agent/v1/sessions/{session_id}"

    headers = {
        "x-session-end-reason": "UserRequest",
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(url, headers=headers)

    return response.json()

class RequestModel(BaseModel):
    message: str

@app.post("/invokeAgent")
def invokeAgent(req:RequestModel,agentId: str=Header(...),domainUrl: str=Header(...))->Any:

    try:

             
        token = get_access_token()

        session = createSession(agentId, token, domainUrl)

        session_id = session['sessionId']

        url = f"https://api.salesforce.com/einstein/ai-agent/v1/sessions/{session_id}/messages"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        payload = {
            "message": {
                "sequenceId": 1, 
                "type": "Text",
                "text": req.message
            }
        }

        response = requests.post(url, json=payload, headers=headers)

        deleteSession(session_id, token)

        return response.json()["messages"]
    
    except Exception as e:

        print('Error invoking agent:', e)
        return f"Unable to connect to the agent: {str(e)}"

mcp = FastMCP.from_fastapi(app=app, name="Agentforce MCP Server",auth=auth)

if __name__ == "__main__":
    mcp.run('streamable-http', host='0.0.0.0', port=8000)