import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/kmu_business.db")
conn.executescript(Path("app/database/schema.sql").read_text())

conn.execute("DELETE FROM compliance_results")
conn.execute("DELETE FROM compliance_checks")

checks = [
    ("CIS-001", "MFA enabled for all users", "Identity", "high", "All active user accounts must have MFA enabled."),
    ("CIS-002", "Privileged users limited to IT", "Identity", "critical", "Only IT users may have privileged accounts."),
    ("CMDB-001", "Every asset has owner", "CMDB", "high", "Every asset must be assigned to a user."),
    ("CMDB-002", "Every asset has IP and MAC", "CMDB", "high", "Every asset must have IP and MAC address."),
    ("SEC-001", "High criticality assets protected", "Security", "high", "High criticality assets must have MFA and BitLocker relationship."),
    ("ITSM-001", "High priority tickets tracked", "ITSM", "medium", "Open high priority tickets must be visible."),
    ("AZ-001", "Azure resources classified", "Azure", "medium", "Azure resources must have criticality and cost model."),
]

for c in checks:
    conn.execute("""
    INSERT INTO compliance_checks(check_id, check_name, category, severity, description)
    VALUES (?, ?, ?, ?, ?)
    """, c)

def result(check_id, status, obj, evidence):
    conn.execute("""
    INSERT INTO compliance_results(check_id, status, affected_object, evidence)
    VALUES (?, ?, ?, ?)
    """, (check_id, status, obj, evidence))

# CIS-001
for username, mfa in conn.execute("SELECT username, mfa_enabled FROM user_accounts"):
    result("CIS-001", "PASS" if mfa == 1 else "FAIL", username, f"mfa_enabled={mfa}")

# CIS-002
for username, department, privileged in conn.execute("SELECT username, department, privileged FROM user_accounts"):
    status = "PASS" if privileged == 0 or department == "IT" else "FAIL"
    result("CIS-002", status, username, f"department={department}, privileged={privileged}")

# CMDB-001
for asset_tag, owner in conn.execute("SELECT asset_tag, owner_username FROM assets"):
    result("CMDB-001", "PASS" if owner else "FAIL", asset_tag, f"owner_username={owner}")

# CMDB-002
for asset_tag, ip, mac in conn.execute("SELECT asset_tag, ip_address, mac_address FROM assets"):
    status = "PASS" if ip and mac else "FAIL"
    result("CMDB-002", status, asset_tag, f"ip={ip}, mac={mac}")

# SEC-001
for (asset_tag,) in conn.execute("SELECT asset_tag FROM assets WHERE criticality='high'"):
    rels = [r[0] for r in conn.execute("""
        SELECT target_id
        FROM cmdb_relationships
        WHERE source_id=? AND relation_type='protected_by'
    """, (asset_tag,))]
    ok = "MFA-Required-All" in rels and "BitLocker-All" in rels
    result("SEC-001", "PASS" if ok else "FAIL", asset_tag, f"policies={','.join(rels)}")

# ITSM-001
high_open = conn.execute("""
SELECT COUNT(*)
FROM tickets
WHERE priority='high' AND status!='Closed'
""").fetchone()[0]
result("ITSM-001", "PASS" if high_open > 0 else "FAIL", "tickets", f"open_high_priority={high_open}")

# AZ-001
for name, criticality, cost_model in conn.execute("SELECT resource_name, criticality, cost_model FROM azure_resources"):
    status = "PASS" if criticality and cost_model else "FAIL"
    result("AZ-001", status, name, f"criticality={criticality}, cost_model={cost_model}")

conn.execute("""
INSERT INTO audit_logs(actor, action, target)
VALUES ('system', 'run_compliance_checks', 'compliance_engine')
""")

conn.commit()

print("compliance_checks:", conn.execute("SELECT COUNT(*) FROM compliance_checks").fetchone()[0])
print("compliance_results:", conn.execute("SELECT COUNT(*) FROM compliance_results").fetchone()[0])
print("failed:", conn.execute("SELECT COUNT(*) FROM compliance_results WHERE status='FAIL'").fetchone()[0])

conn.close()
