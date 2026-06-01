import sqlite3

conn = sqlite3.connect("data/kmu_business.db")

print("=== KMU MANAGEMENT DASHBOARD ===")
print("Employees:", conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0])
print("User Accounts:", conn.execute("SELECT COUNT(*) FROM user_accounts").fetchone()[0])
print("Assets:", conn.execute("SELECT COUNT(*) FROM assets").fetchone()[0])
print("Tickets:", conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0])
print("Security Policies:", conn.execute("SELECT COUNT(*) FROM security_policies").fetchone()[0])
print("Backup Policies:", conn.execute("SELECT COUNT(*) FROM backup_policies").fetchone()[0])
print("Security Events:", conn.execute("SELECT COUNT(*) FROM security_events").fetchone()[0])

print("\n=== Employees per Department ===")
for row in conn.execute("SELECT abteilung, COUNT(*) FROM employees GROUP BY abteilung ORDER BY COUNT(*) DESC"):
    print(row)

print("\n=== Assets per Zone ===")
for row in conn.execute("SELECT network_zone, vlan_id, COUNT(*) FROM assets GROUP BY network_zone, vlan_id ORDER BY vlan_id"):
    print(row)

print("\n=== Payroll per Department ===")
for row in conn.execute("SELECT abteilung, SUM(gehalt_monat_eur) FROM employees GROUP BY abteilung ORDER BY SUM(gehalt_monat_eur) DESC"):
    print(row)

conn.close()
