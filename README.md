\# Gemini MCP Notes Assistant



A hands-on Model Context Protocol (MCP) project that connects Google Gemini with an MCP server to create an AI-powered notes assistant.



The assistant can understand natural-language requests, decide which MCP tool to use, execute that tool through the MCP server, and use the result to generate a natural-language response.



\## Architecture



User

&#x20; ↓

Gemini

&#x20; ↓

MCP Client

&#x20; ↓

MCP Server

&#x20; ↓

SQLite



\## Features



\- MCP server built with the Python MCP SDK

\- Gemini-powered natural-language interface

\- Gemini function calling for MCP tool selection

\- Persistent SQLite note storage

\- Add notes

\- List notes

\- Search notes

\- Basic greeting tool

\- Calculator tool

\- MCP resource for note statistics

\- MCP prompt for note summarization

\- MCP Inspector testing



\## MCP Tools



| Tool | Description |

|------|-------------|

| `say\_hello` | Returns a greeting |

| `add\_numbers` | Adds two numbers |

| `add\_note` | Saves a note to SQLite |

| `list\_notes` | Returns all saved notes |

| `search\_notes` | Searches notes by title or content |



\## MCP Resource



`notes://summary`



Returns the total number of saved notes.



\## MCP Prompt



`summarize\_note`



Creates a structured prompt for summarizing a note.



\## Tech Stack



\- Python

\- Model Context Protocol (MCP)

\- Google Gemini API

\- SQLite

\- `google-genai`

\- `python-dotenv`



\## Project Structure



```text

MCP/

├── client.py

├── server.py

├── requirements.txt

├── .env.example

├── .gitignore

└── README.md

