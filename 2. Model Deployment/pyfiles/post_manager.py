import sqlite3 as sql
import os
from flask import Flask, request, jsonify, session
import pyfiles.register_manager as rm
import logging

# Configure logging

app = Flask(__name__)
app.config["DATABASE"] = "./data/posts.db"


def all_posts():
    con = sql.connect(app.config["DATABASE"])
    cur = con.cursor()
    cur.execute("SELECT * FROM AWCuWion_posts")
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    con.close()
    return [dict(zip(columns, row)) for row in rows]



def add_post(data, uuid):
    con = sql.connect(app.config["DATABASE"])
    cur = con.cursor()
    try:
        if isinstance(uuid, list):
            uuid = uuid[0]  # Assuming the first element is the correct UUID
        cur.execute(
            "INSERT INTO AWCuWion_posts (Wj89c_uuid, developer, project, start_time, end_time, diary_time, time_worked, repo, dev_notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                uuid,
                data.get("developer"),
                data.get("project"),
                data.get("start_time"),
                data.get("end_time"),
                data.get("diary_time"),
                data.get("time_worked"),
                data.get("repo"),
                data.get("dev_notes"),
            ),
        )
        con.commit()
        con.close()
        return {"message": "Post created successfully"}, 201
    except Exception as e:
        con.close()
        return {"error": str(e)}, 500


def get_similar_posts(data):
    con = sql.connect(app.config["DATABASE"])
    cur = con.cursor()
    cur.execute(
        """
        SELECT p.*, u.vX8hR_username, u.ajkSC_email
        FROM AWCuWion_posts p
        JOIN e50PMSBi_users u ON p.Wj89c_uuid = u.Wj89c_uuid
        WHERE p.developer LIKE ? OR p.project LIKE ? OR p.start_time LIKE ? OR p.end_time LIKE ? OR p.diary_time LIKE ? OR p.time_worked LIKE ? OR p.repo LIKE ? OR p.dev_notes LIKE ?
        """,
        (
            f"%{data.get('developer')}%",
            f"%{data.get('project')}%",
            f"%{data.get('start_time')}%",
            f"%{data.get('end_time')}%",
            f"%{data.get('diary_time')}%",
            f"%{data.get('time_worked')}%",
            f"%{data.get('repo')}%",
            f"%{data.get('dev_notes')}%",
        ),
    )
    posts = cur.fetchall()
    con.close()
    return posts


if __name__ == "__main__":
    if not os.path.exists(app.config["DATABASE"]):
        con = sql.connect(app.config["DATABASE"])
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE AWCuWion_posts (Wj89c_uuid TEXT NOT NULL, developer TEXT NOT NULL, project TEXT NOT NULL, start_time TEXT, end_time TEXT, diary_time TEXT NOT NULL, time_worked TEXT, repo TEXT NOT NULL, dev_notes TEXT NOT NULL)"
        )
        con.commit()
        con.close()
    else:
        print("Database already exists.")
