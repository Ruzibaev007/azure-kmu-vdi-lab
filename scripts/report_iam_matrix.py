import sqlite3

conn = sqlite3.connect("data/kmu_business.db")

print("=== IAM / RBAC MATRIX ===")

print("\n[Groups]")
for row in conn.execute("""
SELECT group_name, description
FROM groups
ORDER BY group_name
"""):
    print(row)

print("\n[Members per Group]")
for row in conn.execute("""
SELECT group_name, COUNT(*) AS members
FROM group_memberships
GROUP BY group_name
ORDER BY members DESC, group_name
"""):
    print(row)

print("\n[RBAC Assignments]")
for row in conn.execute("""
SELECT principal_name, role_name, scope
FROM rbac_assignments
ORDER BY principal_name, role_name
"""):
    print(row)

print("\n[Privileged Users]")
for row in conn.execute("""
SELECT e.personalnummer, e.vorname, e.nachname, ua.username, ua.role
FROM user_accounts ua
JOIN employees e ON e.personalnummer = ua.employee_number
WHERE ua.privileged=1
ORDER BY ua.username
"""):
    print(row)

conn.close()
