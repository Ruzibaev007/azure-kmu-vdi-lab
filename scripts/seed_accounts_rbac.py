import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/kmu_business.db")
conn.executescript(Path("app/database/schema.sql").read_text())

conn.execute("DELETE FROM user_accounts")

admin_roles = {"Systemadministrator", "IT-Administrator"}

for row in conn.execute("""
SELECT personalnummer, benutzername, abteilung, rolle
FROM employees
ORDER BY personalnummer
""").fetchall():
    personalnummer, username, department, role = row
    privileged = 1 if role in admin_roles else 0
    conn.execute("""
    INSERT INTO user_accounts (
        username, employee_number, department, role,
        account_status, mfa_enabled, privileged
    )
    VALUES (?, ?, ?, ?, 'enabled', 1, ?)
    """, (username, personalnummer, department, role, privileged))

conn.execute("INSERT INTO audit_logs(actor, action, target) VALUES (?, ?, ?)", ("system","seed_accounts_rbac","50_user_accounts"))
conn.commit()

print("user_accounts:", conn.execute("SELECT COUNT(*) FROM user_accounts").fetchone()[0])
print("mfa_enabled:", conn.execute("SELECT COUNT(*) FROM user_accounts WHERE mfa_enabled=1").fetchone()[0])
print("privileged:", conn.execute("SELECT COUNT(*) FROM user_accounts WHERE privileged=1").fetchone()[0])

conn.close()
