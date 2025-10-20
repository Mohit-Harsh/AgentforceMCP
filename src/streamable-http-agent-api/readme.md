# Agentforce Streamable-HTTP MCP Server

The **Agentforce Streamable-HTTP MCP Server** enables seamless communication with **any Agentforce Agent** in **any Salesforce Org** using **streamable HTTP connections**. It supports real-time queries from MCP clients such as **GitHub Copilot**, allowing developers to integrate Salesforce Agentforce agents into their workflow securely and efficiently.

---

## Prerequisites

Before using the server, ensure the following:

1. **Salesforce Org** with Agentforce enabled.
2. **Connected App** configured and associated with the Agent.
3. **Active Agentforce Agent** in the org.
4. **Python 3.10+** installed on the system.

---

## Getting Started

### Server Inputs

The server accepts the following inputs from MCP clients via HTTP:

| Input          | Type | Description                             |
| -------------- | ---- | --------------------------------------- |
| `clientId`     | str  | Connected App Client ID (Header)        |
| `clientSecret` | str  | Connected App Client Secret (Header)    |
| `agentId`      | str  | API ID of the Agentforce Agent (Header) |
| `message`      | str  | Query or message content (Body)         |

---

### Start Server

Run the server using Python:

```bash
python server.py
```

* By default, the server runs at:

  ```
  http://localhost:8000/mcp
  ```

* The server accepts **HTTP POST** requests with the inputs defined above and returns streamed responses from the Agentforce agent.

---

## MCP Client Configuration

For **GitHub Copilot** or similar MCP clients, configure `mcp.json` as follows:

```json
"Agent API": {
    "url": "http://127.0.0.1:8000/mcp",
    "type": "http",
    "headers": {
        "clientId": "",
        "clientSecret": "",
        "agentId": "",
        "domainUrl": ""
    }
}
```

* Fill in `clientId`, `clientSecret`, `agentId`, and optionally `domainUrl` according to your Salesforce Connected App and Agentforce configuration.
* Once configured, the MCP client can send messages directly to the Agentforce agent and receive responses in real-time.

---

