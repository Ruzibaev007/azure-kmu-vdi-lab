import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/kmu_business.db")
conn.executescript(Path("app/database/schema.sql").read_text())

conn.execute("DELETE FROM cmdb_relationships")

assets = conn.execute("""
SELECT asset_tag, owner_username, assigned_to, department, network_zone
FROM assets
ORDER BY asset_tag
""").fetchall()

for asset_tag, username, assigned_to, department, network_zone in assets:
    employee = conn.execute("""
    SELECT personalnummer
    FROM employees
    WHERE benutzername=?
    """, (username,)).fetchone()

    if employee:
        conn.execute("""
        INSERT INTO cmdb_relationships(source_type, source_id, relation_type, target_type, target_id)
        VALUES ('employee', ?, 'owns', 'asset', ?)
        """, (employee[0], asset_tag))

    conn.execute("""
    INSERT INTO cmdb_relationships(source_type, source_id, relation_type, target_type, target_id)
    VALUES ('user_account', ?, 'uses', 'asset', ?)
    """, (username, asset_tag))

    conn.execute("""
    INSERT INTO cmdb_relationships(source_type, source_id, relation_type, target_type, target_id)
    VALUES ('asset', ?, 'belongs_to', 'network_zone', ?)
    """, (asset_tag, network_zone))

tickets = conn.execute("""
SELECT ticket_number, asset_tag
FROM tickets
WHERE asset_tag IS NOT NULL
""").fetchall()

for ticket_number, asset_tag in tickets:
    conn.execute("""
    INSERT INTO cmdb_relationships(source_type, source_id, relation_type, target_type, target_id)
    VALUES ('asset', ?, 'has_ticket', 'ticket', ?)
    """, (asset_tag, ticket_number))

high_assets = conn.execute("""
SELECT asset_tag
FROM assets
WHERE criticality='high'
""").fetchall()

for (asset_tag,) in high_assets:
    conn.execute("""
    INSERT INTO cmdb_relationships(source_type, source_id, relation_type, target_type, target_id)
    VALUES ('asset', ?, 'protected_by', 'security_policy', 'MFA-Required-All')
    """, (asset_tag,))
    conn.execute("""
    INSERT INTO cmdb_relationships(source_type, source_id, relation_type, target_type, target_id)
    VALUES ('asset', ?, 'protected_by', 'security_policy', 'BitLocker-All')
    """, (asset_tag,))

conn.execute("""
INSERT INTO audit_logs(actor, action, target)
VALUES ('system', 'seed_cmdb_relationships', 'cmdb_graph')
""")

conn.commit()

print("cmdb_relationships:", conn.execute("SELECT COUNT(*) FROM cmdb_relationships").fetchone()[0])

conn.close()
