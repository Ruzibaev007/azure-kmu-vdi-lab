import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/kmu_business.db")
conn.executescript(Path("app/database/schema.sql").read_text())

for t in ["ticket_comments","ticket_history","tickets"]:
    conn.execute(f"DELETE FROM {t}")

tickets = [
("INC-2026-0001","Incident","AVD","high","open","l.hartmann","t.becker","KMU-ASSET-008","AVD Anmeldung nicht möglich","Benutzerin kann sich nicht an AVD anmelden."),
("INC-2026-0002","Incident","Netzwerk","high","in_progress","a.schaefer","l.hoffmann","KMU-ASSET-024","Lagergerät verliert Netzwerk","WAREHOUSE-ZONE meldet Verbindungsabbrüche."),
("INC-2026-0003","Incident","Drucker","normal","open","m.koch","l.hoffmann","KMU-ASSET-012","Etikettendrucker nicht erreichbar","Drucker im Einkauf ist nicht erreichbar."),
("INC-2026-0004","Incident","Security","high","open","t.becker","t.becker","KMU-ASSET-003","Verdächtiger Login-Versuch","Mehrere fehlgeschlagene Admin-Logins erkannt."),
("INC-2026-0005","Incident","Application","normal","open","n.richter","l.hoffmann","KMU-ASSET-017","CAD startet langsam","CAD-Anwendung startet verzögert."),
("SR-2026-0001","Service Request","Hardware","normal","open","l.moreau","l.hoffmann","KMU-ASSET-035","Neuer Monitor","Zusätzlicher Monitor für Lagerverwaltung."),
("SR-2026-0002","Service Request","User Account","normal","open","a.fischer","l.hoffmann","KMU-ASSET-005","Neuen Benutzer vorbereiten","Onboarding Benutzerkonto vorbereiten."),
("SR-2026-0003","Service Request","Software","normal","approved","s.lange","t.becker","KMU-ASSET-016","Engineering Tool installieren","Tool für Engineering bereitstellen."),
("CHG-2026-0001","Change","Infrastructure","high","planned","t.becker","t.becker","KMU-ASSET-003","AVD Session Host vorbereiten","Bicep Deployment für zusätzlichen Session Host planen."),
("CHG-2026-0002","Change","Network","high","planned","l.hoffmann","t.becker","KMU-ASSET-004","Zero Trust Policy erweitern","Engineering zu Production Regel dokumentieren."),
]

for x in tickets:
    conn.execute("""
    INSERT INTO tickets(ticket_number,ticket_type,category,priority,status,created_by,assigned_to,asset_tag,title,description)
    VALUES (?,?,?,?,?,?,?,?,?,?)
    """, x)
    conn.execute("INSERT INTO ticket_history(ticket_number, action, actor) VALUES (?, 'created', 'system')", (x[0],))

conn.execute("INSERT INTO ticket_comments(ticket_number, author, comment) VALUES ('INC-2026-0001','t.becker','AVD Logs werden geprüft.')")
conn.execute("INSERT INTO audit_logs(actor, action, target) VALUES (?, ?, ?)", ("system","seed_tickets","itsm"))
conn.commit()

print("tickets:", conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0])
print("ticket_history:", conn.execute("SELECT COUNT(*) FROM ticket_history").fetchone()[0])
print("ticket_comments:", conn.execute("SELECT COUNT(*) FROM ticket_comments").fetchone()[0])
conn.close()
