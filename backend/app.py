from flask import Flask, request, jsonify, redirect, abort
from flask_cors import CORS
import LPE
import json
from datetime import datetime, timezone, timedelta
from linkValidation import CheckURL
import sqlite3
from urllib.parse import urlencode

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DATABASE = "analytics.db"

def get_db():
    """Get a new database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist (safe to call multiple times)"""
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS links (
                token           TEXT PRIMARY KEY,
                original_url    TEXT NOT NULL,
                host            TEXT NOT NULL,
                tokenized_url   TEXT NOT NULL,
                created_at      TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
                last_id         INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clicks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                token       TEXT NOT NULL,
                click_time  TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
                hour        INTEGER NOT NULL CHECK(hour BETWEEN 0 AND 23),
                FOREIGN KEY (token) REFERENCES links(token) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_stats (
                token       TEXT NOT NULL,
                date        TEXT NOT NULL,
                total_clicks INTEGER DEFAULT 0,
                PRIMARY KEY (token, date),
                FOREIGN KEY (token) REFERENCES links(token) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hourly_stats (
                token       TEXT NOT NULL,
                date        TEXT NOT NULL,
                hour        INTEGER NOT NULL CHECK(hour BETWEEN 0 AND 23),
                clicks      INTEGER DEFAULT 0,
                PRIMARY KEY (token, date, hour),
                FOREIGN KEY (token) REFERENCES links(token) ON DELETE CASCADE
            )
        """)

        conn.commit()


# Run DB initialization once on startup
init_db()

def safeData(data):
    with open("DB.json", "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)

# ── Validate token + host match ──────────────────────────────────────────────────
def validate(token, host):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT host FROM links WHERE token = ?",
            (token,)
        )
        row = cursor.fetchone()
        return row is not None and row['host'].lower() == host.lower()

def addClick(token):
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    hour = now.hour

    with get_db() as conn:
        cursor = conn.cursor()

        # 1. Raw click log
        cursor.execute("""
            INSERT INTO clicks (token, click_time, hour)
            VALUES (?, ?, ?)
        """, (token, now.isoformat(), hour))

        # 2. Update daily total (UPSERT)
        cursor.execute("""
            INSERT INTO daily_stats (token, date, total_clicks)
            VALUES (?, ?, 1)
            ON CONFLICT(token, date)
            DO UPDATE SET total_clicks = total_clicks + 1
        """, (token, date_str))

        # 3. Update hourly count (UPSERT)
        cursor.execute("""
            INSERT INTO hourly_stats (token, date, hour, clicks)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(token, date, hour)
            DO UPDATE SET clicks = clicks + 1
        """, (token, date_str, hour))

        cursor.execute("""
            ALTER TABLE links ADD COLUMN affiliate_params TEXT DEFAULT '{}'
        """)

        conn.commit()
    return True


@app.post("/api/buttonClick")
def buttonClick():
    data = request.get_json()
    url = data.get("url")

    # Validation
    testedurl = CheckURL(url)
    tested = testedurl.runTests()
    if tested["error"] == 1:
        return jsonify({"message": tested["message"], "error": 1, "errorCode": tested["errorCode"]})

    protector = LPE.Tokenize(url)
    token = protector.token
    tokenized_url = protector.getTokenizedLink()
    host = protector.getHost()
    base_url = protector.getBaseUrl()          # without params
    params_json = json.dumps(protector.getParams())  # for storage

    # Store encrypted or plain (your choice)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO links (token, original_url, host, tokenized_url, affiliate_params, last_id)
            VALUES (?, ?, ?, ?, ?, 
                (SELECT COALESCE(MAX(last_id), 0) + 1 FROM links)
            )
        """, (token, base_url, host, tokenized_url, params_json))
        conn.commit()

        conn.commit()
    
    return jsonify({
        "message": f"Your protected url: {tokenized_url}",
        "error": 0
    })
    

@app.get("/affiliate/<host>/<token>")
def redirect302(host, token):
    if not validate(token, host):
        abort(404)

    # Get original URL
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT original_url, affiliate_params
            FROM links WHERE token = ?
        """, (token,))
        row = cursor.fetchone()

    base_url = row['original_url']
    params = json.loads(row['affiliate_params'] or '{}')

    # Rebuild full URL with params
    query_string = urlencode(params, doseq=True)
    full_url = base_url + ('?' + query_string if query_string else '')

    addClick(token)
    return redirect(full_url, code=302)

@app.post("/api/getUserUrls")
def getUserUrls():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT token, host, tokenized_url AS originalUrl, last_id AS ID
            FROM links
            ORDER BY last_id DESC
        """)
        rows = cursor.fetchall()

    if not rows:
        return jsonify({"error": 1})

    result = {
        "tokens": [r['token'] for r in rows],
        "IDs": [r['ID'] for r in rows],
        "URLs": [r['originalUrl'] for r in rows],
        "hosts": [r['host'] for r in rows],
        "error": 0
    }
    return jsonify(result)

# ── Hourly stats ──────────────────────────────────────────────────────────────────
@app.post("/api/<token>/getHours")
def getHours(token):
    now = datetime.now(timezone.utc)
    hourlyData = {}

    with get_db() as conn:
        cursor = conn.cursor()

        # Get last 24 hours from hourly_stats
        for i in range(24):
            dt = now - timedelta(hours=i)
            date_str = dt.strftime("%Y-%m-%d")
            hour = dt.hour

            cursor.execute("""
                SELECT clicks 
                FROM hourly_stats 
                WHERE token = ? AND date = ? AND hour = ?
            """, (token, date_str, hour))

            row = cursor.fetchone()
            clicks = row['clicks'] if row else 0

            label = dt.strftime("%Y-%m-%d %H")
            hourlyData[label] = clicks

    return jsonify({"hourlyData": dict(sorted(hourlyData.items()))})

@app.post("/api/<token>/getDays")
def getDays(token):
    parsed = request.get_json() or {}
    timeframe_str = parsed.get("timeframe", "7d")

    if timeframe_str == "all":
        days_limit = None
    else:
        try:
            days_limit = int(timeframe_str.rstrip("d"))
        except:
            days_limit = 7

    with get_db() as conn:
        cursor = conn.cursor()

        today_utc = datetime.now(timezone.utc).date()
        today_str = today_utc.isoformat()

        # Always ensure today's UTC date exists (even with 0 clicks)
        cursor.execute("""
            INSERT OR IGNORE INTO daily_stats (token, date, total_clicks)
            VALUES (?, ?, 0)
        """, (token, today_str))

        # If limited timeframe: fill the last N days (including today)
        if days_limit is not None:
            for i in range(days_limit + 1):  # +1 includes today
                day = today_utc - timedelta(days=i)
                date_str = day.isoformat()
                cursor.execute("""
                    INSERT OR IGNORE INTO daily_stats (token, date, total_clicks)
                    VALUES (?, ?, 0)
                """, (token, date_str))

        # Query the data
        if days_limit is None:
            cursor.execute("""
                SELECT date, total_clicks
                FROM daily_stats
                WHERE token = ?
                ORDER BY date ASC
            """, (token,))
        else:
            cutoff = (today_utc - timedelta(days=days_limit)).isoformat()
            cursor.execute("""
                SELECT date, total_clicks
                FROM daily_stats
                WHERE token = ? AND date >= ?
                ORDER BY date ASC
            """, (token, cutoff))

        rows = cursor.fetchall()

    # Build dictionary (already sorted by query)
    dateDaysDictionary = {r['date']: r['total_clicks'] for r in rows}

    return jsonify({"dateDaysDictionary": dateDaysDictionary})


def fillMissingData(token, days_limit):
    """
    Ensure that the last `days_limit` days (including today) exist in the stats tables.
    Creates zero-filled entries for missing days and hours.
    
    This replaces the old JSON version — no file I/O, no full data reload.
    """
    if days_limit is None:
        return  # we don't pre-fill infinite history

    today = datetime.now(timezone.utc).date()
    
    with get_db() as conn:
        cursor = conn.cursor()

        for i in range(days_limit + 1):
            day = today - timedelta(days=i)
            date_str = day.isoformat()

            # 1. Check & create daily entry if missing
            cursor.execute("""
                INSERT OR IGNORE INTO daily_stats 
                (token, date, total_clicks)
                VALUES (?, ?, 0)
            """, (token, date_str))

            # 2. Create all 24 hourly entries for this day if they don't exist
            for h in range(24):
                cursor.execute("""
                    INSERT OR IGNORE INTO hourly_stats 
                    (token, date, hour, clicks)
                    VALUES (?, ?, ?, 0)
                """, (token, date_str, h))

        conn.commit()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

"""

FUTURE GAME PLAN


3️⃣ Optional secret/ID per creator
Assign each creator a unique internal ID (could be a UUID or numeric).
Store the ID alongside the token.
Validate that the token belongs to that creator ID rather than relying on a human-readable name.
This is more secure and harder to spoof.

4️⃣ Reject unknown creators
If the creator in the URL doesn’t exist in your DB → return a 404 immediately.
Never attempt to “guess” or auto-fix.
Keeps analytics accurate and prevents misuse.
"""



"""
(A) Hide Affiliate Parameters Until the Last Moment

Keep the real affiliate tag secret on your server.

Instead of embedding ?tag=creator123 in the public link, add it right before redirecting.

Extensions scanning URLs won’t see any affiliate params.

(B) Use Encrypted Links

Encrypt the creator’s affiliate URL.

Store encrypted data in your backend.

Extensions can’t reverse-engineer the link, since they only see your short link.

(C) Delay Script Execution

On the final Amazon / eBay / Shopify site, extensions often run scripts within the first 200ms.

By controlling the redirect flow, we can land users deeper into the purchase funnel, where it’s harder for Honey to hijack.
"""
"""
7. Why Creators Will Trust You

To make creators believe your tool works, we’ll add:

✅ Preview button → Show creators the exact destination of the protected link

✅ Debug page → Show affiliate tag intact

✅ Analytics → Show how many clicks + successful redirects happened

✅ Test mode → Creators can test on their own affiliate dashboards

✅ Open-source redirect logic → Transparency builds trust
"""