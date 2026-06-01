import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/kmu_business.db")
conn.executescript(Path("app/database/schema.sql").read_text())

for table in ["rbac_assignments", "rbac_roles", "group_memberships", "groups"]:
    conn.execute(f"DELETE FROM {table}")

groups = [
    ("GG_All_Employees", "All active employees"),
    ("GG_MFA_Required", "Users required to use MFA"),
    ("GG_AVD_Users", "Users allowed to access virtual desktops"),
    ("GG_IT_Admins", "IT administrators"),
    ("GG_Helpdesk", "Helpdesk operators"),
    ("GG_Security_Operators", "Security monitoring operators"),
    ("GG_Backup_Operators", "Backup and recovery operators"),
    ("GG_Management_Users", "Management users"),
    ("GG_HR_Users", "Human resources users"),
    ("GG_Finance_Users", "Accounting and finance users"),
    ("GG_Procurement_Users", "Purchasing users"),
    ("GG_Dispatch_Users", "Dispatching users"),
    ("GG_Engineering_Users", "Engineering users"),
    ("GG_Warehouse_Users", "Warehouse users"),
    ("GG_Production_Users", "Production users"),
]

roles = [
    ("Global Administrator", "Full tenant administration; break-glass only"),
    ("User Administrator", "Manage users and groups"),
    ("Security Administrator", "Manage security settings and incidents"),
    ("Helpdesk Administrator", "Password reset and user support"),
    ("VM Operator", "Start, stop and inspect virtual machines"),
    ("Backup Operator", "Manage backup and restore operations"),
    ("Monitoring Reader", "Read logs, alerts and dashboards"),
    ("Reader", "Read-only access to Azure resources"),
    ("Contributor", "Manage resources without access control delegation"),
    ("Owner", "Full resource control including access assignments"),
]

for g in groups:
    conn.execute("INSERT INTO groups(group_name, description) VALUES (?, ?)", g)

for r in roles:
    conn.execute("INSERT INTO rbac_roles(role_name, description) VALUES (?, ?)", r)

dept_group = {
    "Management": "GG_Management_Users",
    "IT": "GG_IT_Admins",
    "Personal": "GG_HR_Users",
    "Buchhaltung": "GG_Finance_Users",
    "Einkauf": "GG_Procurement_Users",
    "Disposition": "GG_Dispatch_Users",
    "Engineering": "GG_Engineering_Users",
    "Lager": "GG_Warehouse_Users",
    "Produktion": "GG_Production_Users",
}

users = conn.execute("""
SELECT benutzername, abteilung, rolle
FROM employees
ORDER BY personalnummer
""").fetchall()

for username, department, role in users:
    base_groups = ["GG_All_Employees", "GG_MFA_Required", "GG_AVD_Users", dept_group[department]]

    if department == "IT":
        base_groups.extend(["GG_Helpdesk", "GG_Security_Operators", "GG_Backup_Operators"])

    for group_name in sorted(set(base_groups)):
        conn.execute(
            "INSERT INTO group_memberships(username, group_name) VALUES (?, ?)",
            (username, group_name)
        )

assignments = [
    ("GG_IT_Admins", "Contributor", "/subscriptions/demo/resourceGroups/rg-kmu-vdi-lab"),
    ("GG_IT_Admins", "VM Operator", "/subscriptions/demo/resourceGroups/rg-kmu-vdi-lab/providers/Microsoft.Compute"),
    ("GG_Helpdesk", "Helpdesk Administrator", "/tenants/demo"),
    ("GG_Security_Operators", "Security Administrator", "/subscriptions/demo/resourceGroups/rg-kmu-vdi-lab/security"),
    ("GG_Backup_Operators", "Backup Operator", "/subscriptions/demo/resourceGroups/rg-kmu-vdi-lab/recovery"),
    ("GG_Management_Users", "Reader", "/subscriptions/demo/resourceGroups/rg-kmu-vdi-lab"),
    ("GG_Finance_Users", "Reader", "/subscriptions/demo/resourceGroups/rg-kmu-vdi-lab/reports/finance"),
    ("GG_HR_Users", "Reader", "/subscriptions/demo/resourceGroups/rg-kmu-vdi-lab/reports/hr"),
    ("GG_Engineering_Users", "Reader", "/subscriptions/demo/resourceGroups/rg-kmu-vdi-lab/engineering"),
    ("GG_Warehouse_Users", "Reader", "/subscriptions/demo/resourceGroups/rg-kmu-vdi-lab/warehouse"),
    ("GG_Production_Users", "Reader", "/subscriptions/demo/resourceGroups/rg-kmu-vdi-lab/production"),
]

for a in assignments:
    conn.execute(
        "INSERT INTO rbac_assignments(principal_name, role_name, scope) VALUES (?, ?, ?)",
        a
    )

conn.execute("""
INSERT INTO audit_logs(actor, action, target)
VALUES ('system', 'seed_iam_rbac', 'entra_id_rbac_model')
""")

conn.commit()

for table in ["groups", "group_memberships", "rbac_roles", "rbac_assignments"]:
    print(table + ":", conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])

conn.close()
