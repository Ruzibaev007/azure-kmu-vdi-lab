import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/kmu_business.db")
conn.executescript(Path("app/database/schema.sql").read_text())

for t in ["azure_resources", "azure_resource_groups", "azure_subscriptions"]:
    conn.execute(f"DELETE FROM {t}")

subscription = (
    "Azure Trial Lab Subscription",
    "f15cdb2c-c782-4444-ad0e-c71c07c44f6a",
    "trial-lab"
)

conn.execute("""
INSERT INTO azure_subscriptions(subscription_name, subscription_id, environment)
VALUES (?, ?, ?)
""", subscription)

resource_groups = [
    ("fastapi-westeurope-rg", "westeurope", subscription[1], "Azure VDI and API lab resources"),
    ("rg-kmu-vdi-lab-modeled", "westeurope", subscription[1], "Modeled target architecture for GitHub portfolio"),
]

for rg in resource_groups:
    conn.execute("""
    INSERT INTO azure_resource_groups(resource_group_name, location, subscription_id, purpose)
    VALUES (?, ?, ?, ?)
    """, rg)

resources = [
    ("kmu-vdi-vnet", "Microsoft.Network/virtualNetworks", "fastapi-westeurope-rg", "westeurope", "high", "low", "Virtual network for segmented KMU lab"),
    ("kmu-infra-nsg", "Microsoft.Network/networkSecurityGroups", "fastapi-westeurope-rg", "westeurope", "high", "low", "NSG for infrastructure subnet"),
    ("kmu-desktop-vdi-nsg", "Microsoft.Network/networkSecurityGroups", "fastapi-westeurope-rg", "westeurope", "high", "low", "NSG for VDI desktop subnet"),
    ("kmu-vdi-vm01", "Microsoft.Compute/virtualMachines", "fastapi-westeurope-rg", "westeurope", "high", "cost-controlled", "Trial-safe AVD session host"),
    ("kmu-vdi-vm01-nic", "Microsoft.Network/networkInterfaces", "fastapi-westeurope-rg", "westeurope", "normal", "low", "Network interface for VM"),
    ("kmu-storage-private-endpoint", "Microsoft.Network/privateEndpoints", "fastapi-westeurope-rg", "westeurope", "high", "low", "Private endpoint for storage access"),
    ("fastapi-westeurope-3f2fnq2bil45y-function-app", "Microsoft.Web/sites", "fastapi-westeurope-rg", "westeurope", "normal", "low", "Function App API deployment experiment"),
    ("fastapi-westeurope-3f2fnq2bil45y-logworkspace", "Microsoft.OperationalInsights/workspaces", "fastapi-westeurope-rg", "westeurope", "normal", "low", "Log Analytics workspace"),
    ("fastapi-westeurope-3f2fnq2bil45y-appinsights", "Microsoft.Insights/components", "fastapi-westeurope-rg", "westeurope", "normal", "low", "Application Insights monitoring"),
]

for r in resources:
    conn.execute("""
    INSERT INTO azure_resources(resource_name, resource_type, resource_group_name, location, criticality, cost_model, purpose)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, r)

conn.execute("""
INSERT INTO audit_logs(actor, action, target)
VALUES ('system', 'seed_azure_resources', 'azure_resource_model')
""")

conn.commit()

for t in ["azure_subscriptions", "azure_resource_groups", "azure_resources"]:
    print(t + ":", conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])

conn.close()
