import sqlite3
from pathlib import Path

DB = Path("data/kmu_business.db")
SCHEMA = Path("app/database/schema.sql")

conn = sqlite3.connect(DB)
conn.executescript(SCHEMA.read_text())

conn.execute("DELETE FROM roles")
conn.execute("DELETE FROM departments")

departments = [
    ("Management", "Geschäftsführung, Strategie und Reporting", 2),
    ("IT", "Systemadministration, Azure, Support und Security", 2),
    ("Personal", "HR, Mitarbeiterverwaltung und Onboarding", 2),
    ("Buchhaltung", "Finanzen, Rechnungen und Monatsabschlüsse", 2),
    ("Einkauf", "Lieferanten, Bestellungen und Beschaffung", 4),
    ("Disposition", "Planung, Versand und operative Steuerung", 3),
    ("Engineering", "Technische Planung, CAD und Dokumentation", 8),
    ("Lager", "Wareneingang, Bestand und Kommissionierung", 14),
    ("Produktion", "Fertigung, Maschinenbedienung und Qualitätskontrolle", 13),
]

roles = [
    ("Geschäftsführer", "Management", "Strategische Leitung"),
    ("Operations Manager", "Management", "Operative Steuerung"),

    ("Systemadministrator", "IT", "Azure, Netzwerk, Backup, Security"),
    ("IT-Administrator", "IT", "Benutzer, Endgeräte, Support"),

    ("HR-Manager", "Personal", "Personalverwaltung"),
    ("HR-Sachbearbeiter", "Personal", "Onboarding und Dokumente"),

    ("Finanzbuchhalter", "Buchhaltung", "Buchungen und Rechnungen"),
    ("Controller", "Buchhaltung", "Kostenstellen und Reporting"),

    ("Einkaufsleiter", "Einkauf", "Einkaufsplanung"),
    ("Einkäufer", "Einkauf", "Bestellungen und Lieferanten"),
    ("Junior Einkäufer", "Einkauf", "Operative Beschaffung"),
    ("Supplier Manager", "Einkauf", "Lieferantenmanagement"),

    ("Disponent", "Disposition", "Touren und Einsatzplanung"),
    ("Leitstand Koordinator", "Disposition", "Operativer Leitstand"),
    ("Versandkoordinator", "Disposition", "Versandsteuerung"),

    ("Engineering Lead", "Engineering", "Technische Leitung"),
    ("CAD Konstrukteur", "Engineering", "CAD und Zeichnungen"),
    ("Projektingenieur", "Engineering", "Projektplanung"),
    ("Technischer Zeichner", "Engineering", "Technische Dokumentation"),

    ("Lagerleiter", "Lager", "Lagersteuerung"),
    ("Fachkraft Lagerlogistik", "Lager", "Wareneingang und Kommissionierung"),
    ("Staplerfahrer", "Lager", "Innerbetrieblicher Transport"),
    ("Wareneingangsprüfer", "Lager", "Prüfung und Buchung"),

    ("Produktionsleiter", "Produktion", "Produktionssteuerung"),
    ("Maschinenführer", "Produktion", "Maschinenbedienung"),
    ("Schichtleiter", "Produktion", "Schichtkoordination"),
    ("Qualitätsprüfer", "Produktion", "Qualitätssicherung"),
]

for d in departments:
    conn.execute(
        "INSERT INTO departments(name, description, user_count) VALUES (?, ?, ?)",
        d
    )

for r in roles:
    conn.execute(
        "INSERT INTO roles(name, department, description) VALUES (?, ?, ?)",
        r
    )

conn.execute(
    "INSERT INTO audit_logs(actor, action, target) VALUES (?, ?, ?)",
    ("system", "seed_departments_roles", "departments_roles")
)

conn.commit()

print("departments:", conn.execute("SELECT COUNT(*) FROM departments").fetchone()[0])
print("roles:", conn.execute("SELECT COUNT(*) FROM roles").fetchone()[0])

conn.close()
