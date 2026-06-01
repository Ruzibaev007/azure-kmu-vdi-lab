import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/kmu_business.db")
conn.executescript(Path("app/database/schema.sql").read_text())
conn.execute("DELETE FROM security_policies")

policies = [
("Password-Min-Length-All","GG_All_Employees","Identity","14","Minimum password length"),
("Password-Max-Age-All","GG_All_Employees","Identity","90","Password rotation"),
("MFA-Required-All","GG_MFA_Required","Identity","Enabled","Mandatory MFA"),
("BitLocker-All","GG_All_Employees","Endpoint","Enabled","Disk encryption"),
("Windows-Firewall-All","GG_All_Employees","Endpoint","Enabled","Local firewall"),
("USB-Storage-Production","GG_Production","Endpoint","Disabled","Block removable storage"),
("USB-Storage-Warehouse","GG_Warehouse","Endpoint","Disabled","Block removable storage"),
("Windows-Update-All","GG_All_Employees","PatchManagement","Automatic","Automatic updates"),
("Defender-All","GG_All_Employees","Endpoint","Enabled","Microsoft Defender"),
("RDP-Access-IT-Admins","GG_IT_Admins","RemoteAccess","Allowed","Only IT administrators"),
("RDP-Access-All-Employees","GG_All_Employees","RemoteAccess","Denied","No direct RDP"),
("AVD-Access-All","GG_AVD_Users","AVD","Allowed","Access via Azure Virtual Desktop"),
("Admin-Rights-IT-Admins","GG_IT_Admins","Privilege","Allowed","Local admin rights"),
("Admin-Rights-All-Employees","GG_All_Employees","Privilege","Denied","No local admin rights"),
("Audit-Logging-All","GG_All_Employees","Monitoring","Enabled","Security auditing"),
("PowerShell-Execution-IT-Admins","GG_IT_Admins","Security","Restricted","Signed scripts only"),
]

for p in policies:
    conn.execute("INSERT INTO security_policies(policy_name,target_group,category,setting_value,description) VALUES (?,?,?,?,?)", p)

conn.execute("INSERT INTO audit_logs(actor, action, target) VALUES (?, ?, ?)", ("system","seed_security_policies","security_baseline"))
conn.commit()
print("security_policies:", conn.execute("SELECT COUNT(*) FROM security_policies").fetchone()[0])
conn.close()
