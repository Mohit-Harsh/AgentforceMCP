# 🧩 MCP Server for Agentforce Agent Integration

This repository contains an implementation of a **Model Context Protocol (MCP) Server** that enables seamless connectivity between **any MCP client** and the **Agentforce Agent**.

The server leverages the **Agentforce Python SDK** to invoke and interact with the Agentforce Agent, allowing developers to integrate intelligent automation and AI-driven workflows directly into MCP-compatible environments.

---

## 🚀 Overview

The **MCP Server for Agentforce** acts as a bridge between your MCP client and Salesforce’s Agentforce Agent.
It provides a standardized interface for communication, authentication, and tool invocation through the MCP protocol.

### ✨ Key Features

* **MCP-compliant Server:** Connects effortlessly with any MCP-compatible client.
* **Agentforce SDK Integration:** Utilizes the official Python SDK to interact with Agentforce Agents.
* **Secure Authentication:** Uses Salesforce credentials via environment variables for safe access.
* **Plug-and-Play Setup:** Quick installation and configuration for local development or integration testing.

---

## ⚙️ Setup & Installation

Follow the steps below to set up and run the MCP server locally.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Mohit-Harsh/AgentforceMCP.git
cd AgentforceMCP
```

### 2️⃣ Create a `.env` File

In the project root directory, create a `.env` file with your Salesforce credentials:

```bash
UNAME=<your_salesforce_username>
PASSWORD=<your_salesforce_password>
SECURITY_TOKEN=<your_salesforce_security_token>
```

> ⚠️ **Important:** Do not share your `.env` file or commit it to version control.
> Keep your credentials secure.

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all necessary dependencies including the **Agentforce Python SDK**.

---

## 🧠 Running the MCP Server

### Start the MCP Inspector Server

To interact with and test the MCP tools, run:

```bash
npx @modelcontextprotocol/inspector
```

This launches the **MCP Inspector Server**, which allows you to visually inspect and interact with the MCP endpoints.

### Connect to the MCP Server

Once the inspector server is running:

1. Open the MCP Inspector UI in your browser.

2. Navigate to **Connect → Add MCP Server**.

3. Enter the host URL as:

   ```
   https://localhost:8000/mcp
   ```

4. Click **Connect**.

### Test the MCP Tools

After connecting, navigate to the **Tools** tab in the MCP Inspector.
Here you can trigger, inspect, and validate the available MCP tools integrated with the Agentforce Agent.

---

## 🧰 Tech Stack

| Component                        | Description                                                    |
| -------------------------------- | -------------------------------------------------------------- |
| **Python 3.9+**                  | Core language for MCP server implementation                    |
| **Agentforce Python SDK**        | Used for invoking Agentforce Agents                            |
| **Model Context Protocol (MCP)** | Enables standardized communication between clients and servers |
| **Node.js / npx**                | Used to launch the MCP Inspector                               |
| **dotenv**                       | Manages environment variables securely                         |

---

## 🤝 Contributing

Contributions are welcome!
If you’d like to improve or extend the MCP Server:

1. Fork the repository.
2. Create a new branch (`feature/your-feature-name`).
3. Submit a Pull Request with a clear description.

---

## 🧩 References

* [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
* [Salesforce Agentforce](https://www.salesforce.com/)
* [Agentforce Python SDK](https://pypi.org/project/agentforce-sdk/)

---

