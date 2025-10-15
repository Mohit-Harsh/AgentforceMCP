### Agentforce MCP  Template

```py
from typing import Any
from pydantic import BaseModel
from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth
import os
from dotenv import load_dotenv
from fastapi import FastAPI


load_dotenv()

# Initialize FastAPI server

app = FastAPI()

class Request(BaseModel):
    name: str = None
    message: str

class Response(BaseModel):
    message: str
    session_id: str=None

@app.post("/send_message")
def send_message(req:Request)->Response:
    
    try:
        
        # Initialize AgentForce client
        auth = BasicAuth(
            username=os.getenv("UNAME"),
            password=os.getenv("PASSWORD"),
            security_token=os.getenv("SECURITY_TOKEN")
        )

        agent_force = Agentforce(auth=auth)

        response = agent_force.send_message(
            agent_name=req.name,
            user_message=req.message
        )

        return Response(message=response['agent_response'],session_id=response['session_id'])
    
    except Exception as e:

        print('Exception: ',e)
        return Response(message="Unable to connect to the agent",session_id=None)

```

---