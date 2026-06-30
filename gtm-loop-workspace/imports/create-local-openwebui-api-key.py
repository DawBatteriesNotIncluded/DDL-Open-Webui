"""Create or reuse a local Open WebUI API key inside the Docker container.

Run inside the Open WebUI container. This updates /app/backend/data/webui.db.
It prints the API key to stdout and does not write secrets to repo files.
"""

from __future__ import annotations

import secrets
import sqlite3
import sys
import time
import uuid


DB_PATH = "/app/backend/data/webui.db"


def main() -> int:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    user = cur.execute(
        "select id, name, email, role from user where role = 'admin' order by created_at asc limit 1"
    ).fetchone()
    if user is None:
        user = cur.execute(
            "select id, name, email, role from user order by created_at asc limit 1"
        ).fetchone()

    if user is None:
        print("ERROR: no Open WebUI users found", file=sys.stderr)
        return 1

    tables = {row["name"] for row in cur.execute("select name from sqlite_master where type='table'")}
    if "api_key" in tables:
        existing = cur.execute(
            "select key from api_key where user_id = ? order by created_at desc limit 1",
            (user["id"],),
        ).fetchone()
        if existing and existing["key"]:
            print(f"REUSED_API_KEY_FOR={user['email'] or user['name']}", file=sys.stderr)
            print(existing["key"])
            return 0

        api_key = f"sk-{secrets.token_urlsafe(48)}"
        now = int(time.time())
        cur.execute(
            """
            insert into api_key (id, user_id, key, data, expires_at, last_used_at, created_at, updated_at)
            values (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (str(uuid.uuid4()), user["id"], api_key, "{}", None, None, now, now),
        )
        con.commit()
        print(f"CREATED_API_KEY_FOR={user['email'] or user['name']}", file=sys.stderr)
        print(api_key)
        return 0

    columns = {row["name"] for row in cur.execute("pragma table_info(user)")}
    if "api_key" in columns:
        existing = cur.execute("select api_key from user where id = ?", (user["id"],)).fetchone()
        if existing and existing["api_key"]:
            print(f"REUSED_API_KEY_FOR={user['email'] or user['name']}", file=sys.stderr)
            print(existing["api_key"])
            return 0

        api_key = f"sk-{secrets.token_urlsafe(48)}"
        cur.execute("update user set api_key = ? where id = ?", (api_key, user["id"]))
        con.commit()
        print(f"CREATED_API_KEY_FOR={user['email'] or user['name']}", file=sys.stderr)
        print(api_key)
        return 0

    print("ERROR: no supported API key storage found", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
