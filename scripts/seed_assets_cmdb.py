import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/kmu_business.db")
conn.executescript(Path("app/database/schema.sql").read_text())

conn.execute("DELETE FROM assets")

ZONE_MAP = {
    "IT": ("IT-ZONE", 10, "10.0.10"),
    "Management": ("MGMT-ZONE", 11, "10.0.11"),
    "Personal": ("HR-ZONE", 12, "10.0.12"),
    "Buchhaltung": ("FINANCE-ZONE", 13, "10.0.13"),
    "Einkauf": ("PROCUREMENT-ZONE", 14, "10.0.14"),
    "Disposition": ("DISPATCH-ZONE", 15, "10.0.15"),
    "Engineering": ("ENG-ZONE", 20, "10.0.20"),
    "Lager": ("WAREHOUSE-ZONE", 30, "10.0.30"),
    "Produktion": ("PRODUCTION-ZONE", 40, "10.0.40"),
}

MODELS = [
    ("Notebook", "Lenovo", "ThinkPad T14", "Windows 11 Enterprise"),
    ("Notebook", "Dell", "Latitude 5440", "Windows 11 Enterprise"),
    ("Notebook", "HP", "EliteBook 840", "Windows 11 Enterprise"),
    ("Thin Client", "IGEL", "UD3", "IGEL OS"),
    ("Workstation", "Lenovo", "ThinkStation P3", "Windows 11 Enterprise"),
]

critical_high = {"IT", "Management", "Personal", "Buchhaltung"}

zone_counter = {}

rows = conn.execute("""
SELECT personalnummer, vorname, nachname, benutzername, abteilung
FROM employees
ORDER BY personalnummer
""").fetchall()

for idx, row in enumerate(rows, start=1):
    personalnummer, vorname, nachname, username, department = row
    zone, vlan, prefix = ZONE_MAP[department]
    zone_counter.setdefault(department, 0)
    zone_counter[department] += 1

    ip = f"{prefix}.{9 + zone_counter[department]}"
    mac = f"02:4B:4D:{idx:02X}:{(idx*3)%256:02X}:{(idx*7)%256:02X}"
    hostname = f"kmu-{department.lower().replace('ü','ue').replace('ä','ae').replace('ö','oe')}-{zone_counter[department]:03d}"
    asset_type, manufacturer, model, os_name = MODELS[idx % len(MODELS)]
    criticality = "high" if department in critical_high else "normal"

    conn.execute("""
    INSERT INTO assets (
        asset_tag, hostname, asset_type, manufacturer, model, os_name,
        assigned_to, owner_username, department, ip_address, mac_address,
        network_zone, vlan_id, criticality
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"KMU-ASSET-{idx:03d}", hostname, asset_type, manufacturer, model, os_name,
        f"{vorname} {nachname}", username, department, ip, mac, zone, vlan, criticality
    ))

conn.execute("INSERT INTO audit_logs(actor, action, target) VALUES (?, ?, ?)", ("system","seed_assets_cmdb","50_assets"))
conn.commit()

print("assets:", conn.execute("SELECT COUNT(*) FROM assets").fetchone()[0])
print("zones:", conn.execute("SELECT COUNT(DISTINCT network_zone) FROM assets").fetchone()[0])
print("with_ip:", conn.execute("SELECT COUNT(*) FROM assets WHERE ip_address IS NOT NULL").fetchone()[0])
print("with_mac:", conn.execute("SELECT COUNT(*) FROM assets WHERE mac_address IS NOT NULL").fetchone()[0])

conn.close()
