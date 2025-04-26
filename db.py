import sqlite3

conn = sqlite3.connect('MEC.db')
cursor = conn.cursor()

cursor.executescript('''
CREATE TABLE IF NOT EXISTS Bus (
    bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_number TEXT UNIQUE NOT NULL,
    bus_route TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS CollegeBus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_id INTEGER,
    bus_number TEXT,
    bus_route TEXT,
    date TEXT NOT NULL,
    intime TEXT DEFAULT '-',
    outtime TEXT DEFAULT '-',
    FOREIGN KEY (bus_id) REFERENCES Bus(bus_id)
);

CREATE TABLE IF NOT EXISTS Visitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    purpose TEXT NOT NULL,
    vehicle TEXT NOT NULL CHECK(vehicle IN ('Yes', 'No')),
    vehicle_type TEXT,
    vehicle_number TEXT,
    intime TEXT NOT NULL,
    outtime TEXT,
    date TEXT NOT NULL DEFAULT (DATE('now'))
);
                     
CREATE TABLE IF NOT EXISTS Outpass (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    hostel TEXT NOT NULL,
    room_number TEXT,
    reason TEXT NOT NULL,
    outtime TEXT NOT NULL,
    date TEXT NOT NULL DEFAULT (DATE('now'))
);

    CREATE TABLE IF NOT EXISTS Latecomers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    intime TEXT NOT NULL,
    reason TEXT NOT NULL,
    date TEXT NOT NULL DEFAULT (DATE('now'))
);

ALTER TABLE Outpass ADD COLUMN hostel_type TEXT CHECK(hostel_type IN ('Girls', 'Boys'));
 ''')              

# insert data
cursor.executescript('''
INSERT OR IGNORE INTO Bus(bus_number,bus_route) VALUES
('TN39 N0748','Madhakovil'),
('TN38 A1234','Old Bus Stand'),
('TN38 N1297','Koliyanur'),
('TN27 G8711','Pondy'),
('TN32 F0866','Thirukanur'),
('TN23 B0845','Kalamaruthur');
     ''')       

print("Database created and Data Inserted succesfully")         
conn.commit()
conn.close()