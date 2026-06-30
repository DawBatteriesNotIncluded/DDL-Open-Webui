"""Create a short-lived local Open WebUI JWT inside the Docker container.

Run inside the Open WebUI container. This reads the admin user ID from
/app/backend/data/webui.db and signs a JWT with WEBUI_SECRET_KEY from the
container environment. It does not write secrets to repo files.
"""

from __future__ import annotations

import os
import sqlite3
import sys
import uuid
from datetime import datetime, timedelta, timezone

import jwt


DB_PATH = "/app/backend/data/webui.db"


def main() -> int:
    secret = os.environ.get("WEBUI_SECRET_KEY")
    if not secret:
        print("ERROR: WEBUI_SECRET_KEY is not set", file=sys.stderr)
        return 1

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

    now = datetime.now(timezone.utc)
    payload = {
        "id": user["id"],
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + timedelta(hours=2),
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    print(f"CREATED_JWT_FOR={user['email'] or user['name']}", file=sys.stderr)
    print(token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

