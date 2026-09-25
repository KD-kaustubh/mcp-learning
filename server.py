import sqlite3

from mcp.server import MCPServer

mcp = MCPServer("My First MCP Server")

conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
)
""")

conn.commit()
conn.close()

@mcp.tool()
def say_hello(name: str) -> str:
    """Say hello to a person."""
    return f"Hello {name}! 👋"


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def add_note(title: str, content: str) -> str:
    """Add a new note."""

    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title, content)
    )

    conn.commit()

    return f"Note '{title}' added successfully."

@mcp.tool()
def list_notes() -> list:
    """Return all saved notes."""

    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, content FROM notes")
    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "content": row[2]
        }
        for row in rows
    ]

@mcp.tool()
def search_notes(keyword: str) -> list:
    """Search notes by title or content."""

    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    keyword = f"%{keyword}%"

    cursor.execute(
        """
        SELECT id, title, content
        FROM notes
        WHERE title LIKE ? OR content LIKE ?
        """,
        (keyword, keyword)
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "content": row[2]
        }
        for row in rows
    ]

@mcp.resource("notes://summary")
def notes_summary() -> str:
    """Return a summary of saved notes."""

    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM notes")
    count = cursor.fetchone()[0]

    conn.close()

    return f"You have {count} saved notes."

@mcp.prompt()
def summarize_note(title: str, content: str) -> str:
    """Create a prompt for summarizing a note."""

    return f"""Summarize the following note in 3 concise bullet points.

Title: {title}
Content: {content}
"""

if __name__ == "__main__":
    mcp.run()