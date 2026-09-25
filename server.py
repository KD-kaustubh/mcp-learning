from mcp.server import MCPServer

mcp = MCPServer("My First MCP Server")


@mcp.tool()
def say_hello(name: str) -> str:
    """Say hello to a person."""
    return f"Hello {name}! 👋"


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b
notes = []


@mcp.tool()
def add_note(title: str, content: str) -> str:
    """Add a new note."""
    notes.append({
        "title": title,
        "content": content
    })

    return f"Note '{title}' added successfully."

@mcp.tool()
def list_notes() -> list:
    """Return all saved notes."""
    return notes

@mcp.tool()
def search_notes(keyword: str) -> list:
    """Search notes by title or content."""
    keyword = keyword.lower()

    return [
        note
        for note in notes
        if keyword in note["title"].lower()
        or keyword in note["content"].lower()
    ]

if __name__ == "__main__":
    mcp.run()