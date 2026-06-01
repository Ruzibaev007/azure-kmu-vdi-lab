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

@app.get("/tickets/open")
def open_tickets():
    return {
        "count": len(fetch_all(
            "SELECT * FROM tickets WHERE status!='Closed'"
        )),
        "items": fetch_all(
            "SELECT * FROM tickets WHERE status!='Closed'"
        )
    }

@app.get("/tickets/open")
def open_tickets():
    return {
        "count": len(fetch_all(
            "SELECT * FROM tickets WHERE status!='Closed'"
        )),
        "items": fetch_all(
            "SELECT * FROM tickets WHERE status!='Closed'"
        )
    }

@app.get("/cmdb/relationships")
def cmdb_relationships():
    items = fetch_all("""
        SELECT *
        FROM cmdb_relationships
        ORDER BY source_type, source_id, relation_type
    """)
    return {"count": len(items), "items": items}


@app.get("/cmdb/asset/{asset_tag}")
def cmdb_asset(asset_tag: str):
    asset = fetch_one(
        "SELECT * FROM assets WHERE asset_tag=?",
        (asset_tag,)
    )

    relationships = fetch_all("""
        SELECT *
        FROM cmdb_relationships
        WHERE source_id=? OR target_id=?
        ORDER BY relation_type
    """, (asset_tag, asset_tag))

    tickets = fetch_all("""
        SELECT *
        FROM tickets
        WHERE asset_tag=?
        ORDER BY ticket_number
    """, (asset_tag,))

    return {
        "asset": asset,
        "relationships": relationships,
        "tickets": tickets
    }

@app.get("/iam/groups")
def iam_groups():
    items = fetch_all("""
        SELECT *
        FROM groups
        ORDER BY group_name
    """)
    return {"count": len(items), "items": items}


@app.get("/iam/group-memberships")
def iam_group_memberships():
    items = fetch_all("""
        SELECT *
        FROM group_memberships
        ORDER BY group_name, username
    """)
    return {"count": len(items), "items": items}


@app.get("/iam/rbac/roles")
def iam_rbac_roles():
    items = fetch_all("""
        SELECT *
        FROM rbac_roles
        ORDER BY role_name
    """)
    return {"count": len(items), "items": items}


@app.get("/iam/rbac/assignments")
def iam_rbac_assignments():
    items = fetch_all("""
        SELECT *
        FROM rbac_assignments
        ORDER BY principal_name, role_name
    """)
    return {"count": len(items), "items": items}


@app.get("/iam/user/{username}")
def iam_user(username: str):
    employee = fetch_one("""
        SELECT *
        FROM employees
        WHERE benutzername=?
    """, (username,))

    account = fetch_one("""
        SELECT *
        FROM user_accounts
        WHERE username=?
    """, (username,))

    memberships = fetch_all("""
        SELECT group_name
        FROM group_memberships
        WHERE username=?
        ORDER BY group_name
    """, (username,))

    assignments = fetch_all("""
        SELECT ra.*
        FROM rbac_assignments ra
        JOIN group_memberships gm
          ON gm.group_name = ra.principal_name
        WHERE gm.username=?
        ORDER BY ra.role_name
    """, (username,))

    return {
        "employee": employee,
        "account": account,
        "groups": memberships,
        "rbac_assignments": assignments
    }
