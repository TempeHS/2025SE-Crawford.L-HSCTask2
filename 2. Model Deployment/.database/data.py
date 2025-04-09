import sqlite3 as sql

conn = sql.connect("database.db")
cur = conn.cursor()


def remove_duplicates():
    cur.execute(
        "DELETE FROM data WHERE rowid NOT IN (SELECT MIN(rowid) FROM data GROUP BY *);"
    )
    conn.commit()
    conn.close()
