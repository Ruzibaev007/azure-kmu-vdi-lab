from fastapi import FastAPI
from app.api.database import fetch_all, fetch_one

app = FastAPI(title="Azure KMU VDI Lab API", version="1.0.0")

@app.get("/")
def root():
    return {"status": "running", "project": "Azure KMU VDI Lab"}

@app.get("/dashboard")
def dashboard():
    return {
        "employees": fetch_one("SELECT COUNT(*) AS count FROM employees")["count"],
        "user_accounts": fetch_one("SELECT COUNT(*) AS count FROM user_accounts")["count"],
        "assets": fetch_one("SELECT COUNT(*) AS count FROM assets")["count"],
        "tickets": fetch_one("SELECT COUNT(*) AS count FROM tickets")["count"],
        "security_policies": fetch_one("SELECT COUNT(*) AS count FROM security_policies")["count"],
        "backup_policies": fetch_one("SELECT COUNT(*) AS count FROM backup_policies")["count"],
        "security_events": fetch_one("SELECT COUNT(*) AS count FROM security_events")["count"],
    }

@app.get("/employees")
def employees():
    items = fetch_all("SELECT * FROM employees ORDER BY personalnummer")
    return {"count": len(items), "items": items}

@app.get("/assets")
def assets():
    items = fetch_all("SELECT * FROM assets ORDER BY asset_tag")
    return {"count": len(items), "items": items}

@app.get("/tickets")
def tickets():
    items = fetch_all("SELECT * FROM tickets ORDER BY ticket_number")
    return {"count": len(items), "items": items}

@app.get("/security/policies")
def security_policies():
    items = fetch_all("SELECT * FROM security_policies ORDER BY category, policy_name")
    return {"count": len(items), "items": items}

@app.get("/security/events")
def security_events():
    items = fetch_all("SELECT * FROM security_events ORDER BY detected_at DESC")
    return {"count": len(items), "items": items}

@app.get("/reports/management")
def management_report():
    departments = fetch_all("""
        SELECT abteilung AS department, COUNT(*) AS employees
        FROM employees
        GROUP BY abteilung
        ORDER BY employees DESC
    """)

    zones = fetch_all("""
        SELECT network_zone, vlan_id, COUNT(*) AS assets
        FROM assets
        GROUP BY network_zone, vlan_id
        ORDER BY vlan_id
    """)

    return {
        "departments": departments,
        "network_zones": zones
    }
