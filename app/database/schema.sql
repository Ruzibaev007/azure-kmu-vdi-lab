CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    user_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    personalnummer TEXT NOT NULL UNIQUE,
    vorname TEXT NOT NULL,
    nachname TEXT NOT NULL,
    geburtsjahr INTEGER NOT NULL,
    geburtsort TEXT NOT NULL,
    staatsangehoerigkeit TEXT NOT NULL,
    eintrittsdatum TEXT NOT NULL,
    abteilung TEXT NOT NULL,
    rolle TEXT NOT NULL,
    gehalt_monat_eur INTEGER NOT NULL,
    arbeitszeitmodell TEXT NOT NULL,
    aufgabenbericht TEXT NOT NULL,
    benutzername TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS user_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    employee_number TEXT NOT NULL,
    department TEXT NOT NULL,
    role TEXT NOT NULL,
    account_status TEXT NOT NULL DEFAULT 'enabled',
    mfa_enabled INTEGER NOT NULL DEFAULT 1,
    privileged INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_tag TEXT NOT NULL UNIQUE,
    hostname TEXT NOT NULL UNIQUE,
    asset_type TEXT NOT NULL,
    manufacturer TEXT NOT NULL,
    model TEXT NOT NULL,
    os_name TEXT NOT NULL,
    assigned_to TEXT NOT NULL,
    owner_username TEXT NOT NULL,
    department TEXT NOT NULL,
    ip_address TEXT NOT NULL UNIQUE,
    mac_address TEXT NOT NULL UNIQUE,
    network_zone TEXT NOT NULL,
    vlan_id INTEGER NOT NULL,
    criticality TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
