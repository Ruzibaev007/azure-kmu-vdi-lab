import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/kmu_business.db")
conn.executescript(Path("app/database/schema.sql").read_text())

for t in ["purchase_orders","inventory_items","work_orders"]:
    conn.execute(f"DELETE FROM {t}")

purchase_orders = [
("PO-2026-0001","Einkauf","p.vogel","approved",12500,"Neue Barcode-Scanner für Lagerprozesse"),
("PO-2026-0002","IT","t.becker","draft",7800,"AVD Monitoring und Backup-Komponenten"),
("PO-2026-0003","Engineering","s.lange","approved",15500,"CAD Workstation Zubehör"),
("PO-2026-0004","Produktion","r.meier.prod","in_review",9200,"Ersatzteile für Linie 2"),
("PO-2026-0005","Lager","a.schaefer","approved",4800,"Regal- und Kennzeichnungsmaterial"),
]

inventory = [
("INV-0001","Barcode Scanner Zebra DS2208","Scanner",18,"Lager A1","available"),
("INV-0002","Lenovo ThinkPad Dock","IT Zubehör",12,"IT Raum","available"),
("INV-0003","HP EliteDisplay 24 Zoll","Monitor",20,"Lager B2","available"),
("INV-0004","Sicherheitshelm Produktion","PSA",60,"Produktion P1","available"),
("INV-0005","Ersatzsensor Linie 2","Ersatzteil",8,"Techniklager","reserved"),
]

work_orders = [
("WO-2026-0001","Produktion","m.schulz.prod","open","high","Störung Linie 1 prüfen und dokumentieren"),
("WO-2026-0002","Lager","a.schaefer","open","normal","Inventurzone A vorbereiten"),
("WO-2026-0003","Engineering","n.richter","in_progress","normal","CAD Zeichnung Revision B prüfen"),
("WO-2026-0004","IT","l.hoffmann","open","high","AVD Benutzerzugriffe prüfen"),
("WO-2026-0005","Buchhaltung","d.wagner","open","normal","Monatsabschlussdaten validieren"),
]

for x in purchase_orders:
    conn.execute("INSERT INTO purchase_orders(order_number,department,requested_by,status,amount_eur,description) VALUES (?,?,?,?,?,?)", x)

for x in inventory:
    conn.execute("INSERT INTO inventory_items(item_number,name,category,quantity,location,status) VALUES (?,?,?,?,?,?)", x)

for x in work_orders:
    conn.execute("INSERT INTO work_orders(work_order_number,department,assigned_to,status,priority,description) VALUES (?,?,?,?,?,?)", x)

conn.execute("INSERT INTO audit_logs(actor, action, target) VALUES (?, ?, ?)", ("system","seed_operations","business_operations"))
conn.commit()

for t in ["purchase_orders","inventory_items","work_orders"]:
    print(t + ":", conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])

conn.close()
