from fastmcp import FastMCP
import os
import sqlite3

DB_path=os.path.join(os.path.dirname(__file__),"expenses.db")
Cat_path=os.path.join(os.path.dirname(__file__),"categories.db")


mcp=FastMCP("expense tracker")

def init_db():
    with sqlite3.connect(DB_path) as c:
                c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)


init_db()

@mcp.tool()
def add_expenses(date, amount, category, subcategory=" ", note=" "):
    """Add a new expense entry to the database"""
    with sqlite3.connect (DB_path) as c:
        cur=c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status":"ok","id":cur.lastrowid}
    
    
@mcp.tool()
def list_expenses(start_date, end_date):
    """List expense entries within an inclusive date range."""

    with sqlite3.connect(DB_path) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,                       # <-- comma here
            (start_date, end_date)
        )

        cols = [d[0] for d in cur.description]

        return [
            dict(zip(cols, r))
            for r in cur.fetchall()
@mcp.tool()
def summarize(start_date, end_date, category=None):
    '''Summarize expenses by category within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
        ]
  
if __name__=="__main__":
    mcp.run()