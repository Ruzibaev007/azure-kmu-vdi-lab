import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/kmu_business.db")
conn.executescript(Path("app/database/schema.sql").read_text())

conn.execute("DELETE FROM cost_items")
conn.execute("DELETE FROM cost_policies")

policies = [
    ("Trial-Safe-VM-Limit", "Compute", "Run maximum 1-3 physical VMs during trial phase; model 50 users logically.", "critical"),
    ("Deallocate-Idle-VMs", "Compute", "All lab VMs must be deallocated when not actively used.", "critical"),
    ("Avoid-Premium-Always-On", "Platform", "Avoid always-on premium services unless required for testing.", "high"),
    ("Use-Modeled-Architecture", "Architecture", "Use database-modeled users/assets instead of physically deploying 50 machines.", "high"),
    ("Document-Quota-Limits", "Governance", "Document quota limitations and failed deployments as real Azure troubleshooting evidence.", "medium"),
]

items = [
    ("kmu-vdi-vm01", "Azure VM", 0.00, "deallocated", "VM should stay deallocated when not testing."),
    ("kmu-vdi-vnet", "Virtual Network", 0.00, "active", "VNet has no direct compute cost."),
    ("kmu-desktop-vdi-nsg", "Network Security Group", 0.00, "active", "NSG has no direct cost."),
    ("kmu-infra-nsg", "Network Security Group", 0.00, "active", "NSG has no direct cost."),
    ("kmu-storage-private-endpoint", "Private Endpoint", 7.00, "active", "Keep only if required for private storage testing."),
    ("Log Analytics", "Monitoring", 3.00, "limited", "Keep data ingestion low."),
    ("Application Insights", "Monitoring", 2.00, "limited", "Use only for API monitoring tests."),
    ("Modeled 50 Users", "Logical Model", 0.00, "modeled", "50 users represented in CMDB without deploying 50 VMs."),
]

for p in policies:
    conn.execute("""
    INSERT INTO cost_policies(policy_name, category, rule_text, severity)
    VALUES (?, ?, ?, ?)
    """, p)

for i in items:
    conn.execute("""
    INSERT INTO cost_items(resource_name, resource_type, estimated_monthly_eur, cost_state, optimization_note)
    VALUES (?, ?, ?, ?, ?)
    """, i)

conn.execute("""
INSERT INTO audit_logs(actor, action, target)
VALUES ('system', 'seed_cost_management', 'trial_cost_model')
""")

conn.commit()

print("cost_policies:", conn.execute("SELECT COUNT(*) FROM cost_policies").fetchone()[0])
print("cost_items:", conn.execute("SELECT COUNT(*) FROM cost_items").fetchone()[0])
print("estimated_monthly_eur:", conn.execute("SELECT SUM(estimated_monthly_eur) FROM cost_items").fetchone()[0])

conn.close()
