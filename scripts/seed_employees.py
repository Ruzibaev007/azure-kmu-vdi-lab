import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/kmu_business.db")
conn.executescript(Path("app/database/schema.sql").read_text())

conn.execute("DELETE FROM employees")

employees = [
("MA001","Markus","Schneider",1978,"Hamburg","Deutsch","2016-03-01","Management","Geschäftsführer",8200,"Vollzeit","Strategische Leitung, Budgetfreigaben, Management-Reporting.","m.schneider"),
("MA002","Julia","Weber",1983,"Bremen","Deutsch","2018-07-15","Management","Operations Manager",6500,"Vollzeit","Operative Steuerung, KPI-Auswertung, Prozesskoordination.","j.weber"),

("MA003","Thomas","Becker",1985,"Hannover","Deutsch","2019-01-10","IT","Systemadministrator",5200,"Vollzeit","Azure, Netzwerk, Backup, Security und Infrastrukturpflege.","t.becker"),
("MA004","Leon","Hoffmann",1992,"Kiel","Deutsch","2021-05-01","IT","IT-Administrator",4300,"Vollzeit","User Support, Endgeräte, AVD-Zugriffe und Tickets.","l.hoffmann"),

("MA005","Anna","Fischer",1988,"Lübeck","Deutsch","2020-02-01","Personal","HR-Manager",4700,"Vollzeit","Personalakten, Onboarding und HR-Prozesse.","a.fischer"),
("MA006","Sophie","Klein",1995,"Rostock","Deutsch","2022-09-01","Personal","HR-Sachbearbeiter",3600,"Teilzeit 30h","Dokumentenpflege, Arbeitsverträge und Zeiterfassung.","s.klein"),

("MA007","Daniel","Wagner",1981,"Dortmund","Deutsch","2017-04-01","Buchhaltung","Finanzbuchhalter",4800,"Vollzeit","Rechnungsprüfung, Monatsabschluss und Zahlungsfreigaben.","d.wagner"),
("MA008","Lisa","Hartmann",1990,"Leipzig","Deutsch","2021-11-01","Buchhaltung","Controller",4600,"Vollzeit","Kostenstellen, Controlling und Finanzberichte.","l.hartmann"),

("MA009","Patrick","Vogel",1987,"Köln","Deutsch","2019-08-01","Einkauf","Einkaufsleiter",5100,"Vollzeit","Lieferantenstrategie und Beschaffungsfreigaben.","p.vogel"),
("MA010","Laura","Zimmer",1993,"Berlin","Deutsch","2020-10-01","Einkauf","Einkäufer",3900,"Vollzeit","Bestellungen, Angebote und Liefertermine.","l.zimmer"),
("MA011","Niklas","Braun",1998,"Münster","Deutsch","2023-01-15","Einkauf","Junior Einkäufer",3200,"Vollzeit","Operative Beschaffung und Stammdatenpflege.","n.braun"),
("MA012","Maria","Koch",1984,"Nürnberg","Deutsch","2018-06-01","Einkauf","Supplier Manager",4400,"Vollzeit","Lieferantenbewertung und Vertragsdokumentation.","m.koch"),

("MA013","Oliver","Neumann",1982,"Frankfurt am Main","Deutsch","2016-09-01","Disposition","Disponent",4300,"Vollzeit","Tourenplanung und Kapazitätssteuerung.","o.neumann"),
("MA014","Elena","Schwarz",1991,"Dresden","Deutsch","2020-03-01","Disposition","Leitstand Koordinator",4100,"Schichtmodell","Leitstand, Eskalationen und Schichtübergaben.","e.schwarz"),
("MA015","Fabian","Krüger",1994,"Bielefeld","Deutsch","2022-02-01","Disposition","Versandkoordinator",3700,"Vollzeit","Versandplanung und Statusverfolgung.","f.krueger"),

("MA016","Stefan","Lange",1979,"Stuttgart","Deutsch","2015-05-01","Engineering","Engineering Lead",5900,"Vollzeit","Technische Leitung und Projektfreigaben.","s.lange"),
("MA017","Nina","Richter",1989,"Mannheim","Deutsch","2019-10-01","Engineering","CAD Konstrukteur",4700,"Vollzeit","CAD-Konstruktion und Zeichnungsprüfung.","n.richter"),
("MA018","Mehmet","Demir",1990,"Hamburg","Türkisch","2020-01-15","Engineering","Projektingenieur",4800,"Vollzeit","Projektplanung und technische Abstimmung.","m.demir"),
("MA019","Kateryna","Melnyk",1992,"Kyjiw","Ukrainisch","2022-07-01","Engineering","Technischer Zeichner",3900,"Vollzeit","Technische Dokumentation und Zeichnungsverwaltung.","k.melnyk"),
("MA020","Ahmed","Hassan",1986,"Kairo","Ägyptisch","2021-04-01","Engineering","Projektingenieur",4700,"Vollzeit","Produktionsnahe technische Analyse.","a.hassan"),
("MA021","Marta","Nowak",1991,"Warschau","Polnisch","2019-09-01","Engineering","CAD Konstrukteur",4500,"Vollzeit","CAD-Modelle und Änderungsdokumentation.","m.nowak"),
("MA022","Kevin","Mayer",1997,"Augsburg","Deutsch","2023-03-01","Engineering","Technischer Zeichner",3500,"Vollzeit","Zeichnungsableitung und Dokumentenpflege.","k.mayer"),
("MA023","Sara","Conti",1988,"Mailand","Italienisch","2020-08-01","Engineering","Projektingenieur",4650,"Vollzeit","Technische Projektkoordination.","s.conti"),

("MA024","Andreas","Schäfer",1977,"Essen","Deutsch","2014-02-01","Lager","Lagerleiter",4600,"Vollzeit","Lagersteuerung und Bestandsverantwortung.","a.schaefer"),
("MA025","Robert","Meier",1984,"Bochum","Deutsch","2017-06-01","Lager","Fachkraft Lagerlogistik",3400,"Schichtmodell","Wareneingang und Kommissionierung.","r.meier"),
("MA026","Ivan","Petrov",1989,"Sofia","Bulgarisch","2020-05-01","Lager","Staplerfahrer",3200,"Schichtmodell","Innerbetrieblicher Transport.","i.petrov"),
("MA027","Piotr","Kowalski",1982,"Krakau","Polnisch","2018-09-01","Lager","Wareneingangsprüfer",3300,"Vollzeit","Wareneingangsprüfung und Buchung.","p.kowalski"),
("MA028","Ali","Yilmaz",1993,"Izmir","Türkisch","2021-01-01","Lager","Fachkraft Lagerlogistik",3150,"Schichtmodell","Kommissionierung und Lagerbuchungen.","a.yilmaz"),
("MA029","Jonas","Schulz",1996,"Hamburg","Deutsch","2022-04-01","Lager","Staplerfahrer",3050,"Schichtmodell","Materialbewegung und Nachschub.","j.schulz"),
("MA030","Erik","Petersen",1985,"Flensburg","Deutsch","2019-03-01","Lager","Fachkraft Lagerlogistik",3350,"Vollzeit","Bestandsführung und Inventur.","e.petersen"),
("MA031","Milan","Horvat",1990,"Zagreb","Kroatisch","2020-11-01","Lager","Staplerfahrer",3150,"Schichtmodell","Transport und Ladezonensteuerung.","m.horvat"),
("MA032","Irina","Sokolova",1987,"Riga","Lettisch","2021-06-01","Lager","Wareneingangsprüfer",3350,"Vollzeit","Qualitätsprüfung Wareneingang.","i.sokolova"),
("MA033","Tobias","Frank",1999,"Kassel","Deutsch","2023-08-01","Lager","Fachkraft Lagerlogistik",3000,"Vollzeit","Kommissionierung und Verpackung.","t.frank"),
("MA034","Yusuf","Aydin",1994,"Ankara","Türkisch","2022-01-01","Lager","Staplerfahrer",3100,"Schichtmodell","Staplerbetrieb und Sicherheitskontrollen.","y.aydin"),
("MA035","Luc","Moreau",1986,"Lyon","Französisch","2019-12-01","Lager","Fachkraft Lagerlogistik",3400,"Vollzeit","Lagerbewegungen und Inventurpflege.","l.moreau"),
("MA036","Petra","Hansen",1980,"Hamburg","Deutsch","2016-05-01","Lager","Wareneingangsprüfer",3500,"Vollzeit","Wareneingang und Reklamationen.","p.hansen"),
("MA037","Dmytro","Shevchenko",1991,"Lwiw","Ukrainisch","2022-10-01","Lager","Fachkraft Lagerlogistik",3150,"Schichtmodell","Kommissionierung und Scannerbuchungen.","d.shevchenko"),

("MA038","Ralf","Meier",1976,"Bremen","Deutsch","2013-01-01","Produktion","Produktionsleiter",5400,"Vollzeit","Produktionssteuerung und Tagesplanung.","r.meier.prod"),
("MA039","Selin","Demir",1992,"Hamburg","Türkisch","2020-06-01","Produktion","Schichtleiter",4200,"Schichtmodell","Schichtkoordination und Übergaben.","s.demir"),
("MA040","Martin","Schulz",1984,"Celle","Deutsch","2018-02-01","Produktion","Maschinenführer",3600,"Schichtmodell","Maschinenbedienung Linie 1.","m.schulz.prod"),
("MA041","Oksana","Koval",1990,"Odessa","Ukrainisch","2022-05-01","Produktion","Qualitätsprüfer",3700,"Vollzeit","Qualitätsprüfung und Prüfprotokolle.","o.koval"),
("MA042","Jan","Bauer",1988,"Ulm","Deutsch","2019-07-01","Produktion","Maschinenführer",3550,"Schichtmodell","Maschinenbedienung Linie 2.","j.bauer"),
("MA043","Miguel","Garcia",1985,"Madrid","Spanisch","2020-09-01","Produktion","Maschinenführer",3600,"Schichtmodell","Fertigungsbetrieb und Störungsmeldungen.","m.garcia"),
("MA044","Hanna","Wolf",1995,"Erfurt","Deutsch","2021-03-01","Produktion","Qualitätsprüfer",3450,"Vollzeit","Endkontrolle und Dokumentation.","h.wolf"),
("MA045","Tom","Lehmann",1998,"Potsdam","Deutsch","2023-02-01","Produktion","Maschinenführer",3200,"Schichtmodell","Bedienung und Reinigung der Anlage.","t.lehmann"),
("MA046","Nikolai","Ivanov",1987,"Plowdiw","Bulgarisch","2019-11-01","Produktion","Maschinenführer",3500,"Schichtmodell","Anlagenbetrieb und Materialzufuhr.","n.ivanov"),
("MA047","Fatima","El Amrani",1991,"Casablanca","Marokkanisch","2021-08-01","Produktion","Qualitätsprüfer",3500,"Vollzeit","Qualitätsprüfung und Abweichungsberichte.","f.elamrani"),
("MA048","Ben","Keller",1983,"Mainz","Deutsch","2017-10-01","Produktion","Schichtleiter",4300,"Schichtmodell","Schichtleitung und Produktionsfreigabe.","b.keller"),
("MA049","Radu","Popescu",1989,"Bukarest","Rumänisch","2020-12-01","Produktion","Maschinenführer",3450,"Schichtmodell","Maschinenbedienung Linie 3.","r.popescu"),
("MA050","Lea","Sommer",1996,"Würzburg","Deutsch","2022-06-01","Produktion","Qualitätsprüfer",3400,"Vollzeit","Prüfberichte und Fertigungsfreigabe.","l.sommer"),
]

for e in employees:
    conn.execute("""
    INSERT INTO employees (
        personalnummer, vorname, nachname, geburtsjahr, geburtsort,
        staatsangehoerigkeit, eintrittsdatum, abteilung, rolle,
        gehalt_monat_eur, arbeitszeitmodell, aufgabenbericht,
        benutzername
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, e)

conn.execute("INSERT INTO audit_logs(actor, action, target) VALUES (?, ?, ?)", ("system","seed_employees","50_employees"))
conn.commit()
print("employees:", conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0])
conn.close()
