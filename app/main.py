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
        "groups": fetch_one("SELECT COUNT(*) AS count FROM groups")["count"],
        "rbac_assignments": fetch_one("SELECT COUNT(*) AS count FROM rbac_assignments")["count"],
        "azure_resources": fetch_one("SELECT COUNT(*) AS count FROM azure_resources")["count"],
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

@app.get("/azure/subscriptions")
def azure_subscriptions():
    items = fetch_all("""
        SELECT *
        FROM azure_subscriptions
        ORDER BY subscription_name
    """)
    return {"count": len(items), "items": items}


@app.get("/azure/resource-groups")
def azure_resource_groups():
    items = fetch_all("""
        SELECT *
        FROM azure_resource_groups
        ORDER BY resource_group_name
    """)
    return {"count": len(items), "items": items}


@app.get("/azure/resources")
def azure_resources():
    items = fetch_all("""
        SELECT *
        FROM azure_resources
        ORDER BY resource_group_name, resource_type, resource_name
    """)
    return {"count": len(items), "items": items}

@app.get("/compliance/checks")
def compliance_checks():
    items = fetch_all("""
        SELECT *
        FROM compliance_checks
        ORDER BY category, severity, check_id
    """)
    return {"count": len(items), "items": items}


@app.get("/compliance/results")
def compliance_results():
    items = fetch_all("""
        SELECT *
        FROM compliance_results
        ORDER BY status, check_id, affected_object
    """)
    return {"count": len(items), "items": items}


@app.get("/compliance/summary")
def compliance_summary():
    summary = fetch_all("""
        SELECT
            check_id,
            status,
            COUNT(*) AS count
        FROM compliance_results
        GROUP BY check_id, status
        ORDER BY check_id, status
    """)

    failed = fetch_all("""
        SELECT *
        FROM compliance_results
        WHERE status='FAIL'
        ORDER BY check_id, affected_object
    """)

    return {
        "summary": summary,
        "failed_count": len(failed),
        "failed_items": failed
    }

@app.get("/cost/policies")
def cost_policies():
    items = fetch_all("""
        SELECT *
        FROM cost_policies
        ORDER BY severity, category, policy_name
    """)
    return {"count": len(items), "items": items}


@app.get("/cost/items")
def cost_items():
    items = fetch_all("""
        SELECT *
        FROM cost_items
        ORDER BY estimated_monthly_eur DESC, resource_name
    """)
    return {"count": len(items), "items": items}


@app.get("/cost/summary")
def cost_summary():
    total = fetch_one("""
        SELECT SUM(estimated_monthly_eur) AS total
        FROM cost_items
    """)["total"]

    by_state = fetch_all("""
        SELECT cost_state, COUNT(*) AS resources, SUM(estimated_monthly_eur) AS monthly_eur
        FROM cost_items
        GROUP BY cost_state
        ORDER BY monthly_eur DESC
    """)

    return {
        "target_users": 50,
        "physical_vms_limit": "1-3",
        "mode": "trial-safe",
        "estimated_monthly_eur": total,
        "by_state": by_state
    }
