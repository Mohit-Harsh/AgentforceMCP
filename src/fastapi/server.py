from typing import Any
from pydantic import BaseModel
from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Header
from fastapi import Request
import requests
import uuid

load_dotenv()

app = FastAPI()


class RequestWrapper(BaseModel):
    agentName: str
    message: str

class Response(BaseModel):
    message: str
    session_id: str=None


def createToken(clientId: str, clientSecret: str, domainUrl: str) -> Any:

    url = f"https://{domainUrl}/services/oauth2/token"

    payload = {
        'scopes': 'full',
        'grant_type': 'client_credentials',
        'client_id': clientId,
        'client_secret': clientSecret
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=payload, headers=headers)

    return response.json()


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

    return response.json()

def deleteSession(session_id:str,token:str)->Any:

    url = f"https://api.salesforce.com/einstein/ai-agent/v1/sessions/{session_id}"

    headers = {
        "x-session-end-reason": "UserRequest",
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(url, headers=headers)

    return response.json()


@app.post("/invokeAgent")
def invokeAgent(message:str,
                clientId: str=Header(...),
                clientSecret: str=Header(...),
                agentId: str=Header(...),
                domainUrl: str=Header(...))->Any:

    token = createToken(clientId, clientSecret, domainUrl)['access_token']

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
            "text": message
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    deleteSession(session_id, token)

    return response.json()["messages"]

@app.post("/send_message")
def send_message(req:RequestWrapper)->Response:
    
    try:
        
        # Initialize AgentForce client
        auth = BasicAuth(
            username=os.getenv('UNAME'),
            password=os.getenv('PASSWORD'),
            security_token=os.getenv('SECURITY_TOKEN')
        )

        agent_force = Agentforce(auth=auth)

        response = agent_force.send_message(
            agent_name=req.agentName,
            user_message=req.message
        )

        return Response(message=response['agent_response'],session_id=response['session_id'])
    
    except Exception as e:

        print('Exception: ',e)
        if response.status_code == 401:
            print("Authorization Error: Invalid username or password.")
        elif response.status_code == 403:
            print("Access Forbidden: You don’t have permission to access this resource.")
        return Response(message="Unable to connect to the agent")


    

