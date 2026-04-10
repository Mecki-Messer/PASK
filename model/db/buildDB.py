import sqlite3
import time

def build():
    _buildTables()
    _buildViews()
    _buildIndices()
    _buildTriggers()

def _buildTriggers():
    with sqlite3.connect("pask.db") as con:
        cursor = con.cursor()
        cursor.execute('''
                    CREATE TRIGGER IF NOT EXISTS tr_delete_plot_cascade
                    BEFORE DELETE ON plots
                    FOR EACH ROW
                    BEGIN
                        DELETE FROM subplots WHERE plot_id = OLD.plot_id;
                    END;
                ''')

        action_tables = [
            'tillage', 'sowing', 'fertilizer_applications',
            'pesticide_applications', 'harvests', 'cultures'
        ]
        for table in action_tables:
            cursor.execute(f'''
                        CREATE TRIGGER IF NOT EXISTS tr_delete_subplot_cascade_{table}
                        BEFORE DELETE ON subplots
                        FOR EACH ROW
                        BEGIN
                            DELETE FROM {table} WHERE subplot_id = OLD.subplot_id;
                        END;
                    ''')

        con.commit()

def _buildIndices():
    with sqlite3.connect("pask.db") as con:
        cursor = con.cursor()
        cursor.execute('''CREATE INDEX idx_subplot_plot_id ON subplots (subplot_id);''')
        cursor.execute('''CREATE INDEX idx_tillage_subplot_id ON tillage (subplot_id);''')
        cursor.execute('''CREATE INDEX idx_sowing_subplot_id ON sowing (subplot_id);''')
        cursor.execute('''CREATE INDEX idx_fertilizer_subplot_id ON fertilizer_applications (subplot_id);''')
        cursor.execute('''CREATE INDEX idx_pesticide_subplot_id ON pesticide_applications (subplot_id);''')
        cursor.execute('''CREATE INDEX idx_harvests_subplot_id ON harvests (subplot_id);''')
        con.commit()

def _buildViews():
    with sqlite3.connect("pask.db") as con:
        cursor = con.cursor()

        #cursor.execute('''
        #            CREATE VIEW vi_subplots_of_plots AS
        #            SELECT plots.business_id, plots.flik, plots.plot_nr, subplots.plot_suffix, plots.size AS plot_size, subplots.size AS
        #            subplot_size, subplots.year
        #            FROM plots
        #            INNER JOIN subplots ON subplots.plot_id = plots.plot_id;
        #        ''')

        cursor.execute('''
                    CREATE VIEW IF NOT EXISTS vi_subplots_by_business AS
                    SELECT s.*, p.business_id 
                    FROM subplots s
                    JOIN plots p ON s.plot_id = p.plot_id;
                ''')

        cursor.execute('''
                    CREATE VIEW IF NOT EXISTS vi_cultures_by_business AS
                    SELECT c.*, p.business_id
                    FROM cultures c
                    JOIN subplots s ON c.subplot_id = s.subplot_id
                    JOIN plots p ON s.plot_id = p.plot_id;
                ''')

        cursor.execute('''
                    CREATE VIEW IF NOT EXISTS vi_tillage_by_business AS
                    SELECT t.*, p.business_id 
                    FROM tillage t
                    JOIN subplots s ON t.subplot_id = s.subplot_id
                    JOIN plots p ON s.plot_id = p.plot_id;
                ''')

        cursor.execute('''
                    CREATE VIEW IF NOT EXISTS vi_sowing_by_business AS
                    SELECT sow.*, p.business_id 
                    FROM sowing sow
                    JOIN subplots s ON sow.subplot_id = s.subplot_id
                    JOIN plots p ON s.plot_id = p.plot_id;
                ''')

        cursor.execute('''
                    CREATE VIEW IF NOT EXISTS vi_fertilizer_applications_by_business AS
                    SELECT fa.*, p.business_id 
                    FROM fertilizer_applications fa
                    JOIN subplots s ON fa.subplot_id = s.subplot_id
                    JOIN plots p ON s.plot_id = p.plot_id;
                ''')

        cursor.execute('''
                    CREATE VIEW IF NOT EXISTS vi_pesticide_applications_by_business AS
                    SELECT pa.*, p.business_id 
                    FROM pesticide_applications pa
                    JOIN subplots s ON pa.subplot_id = s.subplot_id
                    JOIN plots p ON s.plot_id = p.plot_id;
                ''')

        cursor.execute('''
                    CREATE VIEW IF NOT EXISTS vi_harvests_by_business AS
                    SELECT h.*, p.business_id 
                    FROM harvests h
                    JOIN subplots s ON h.subplot_id = s.subplot_id
                    JOIN plots p ON s.plot_id = p.plot_id;
                ''')

        cursor.execute('''
                    CREATE VIEW IF NOT EXISTS vi_plot_chronology AS
                    SELECT 
                        p.business_id, s.plot_id, s.subplot_id, s.suffix, s.year AS subplot_year,
                        t.date, 'Bodenbearbeitung' AS action_type,
                        t.depth AS val_1, t.type AS val_2, t.tool AS info,
                        NULL AS ref_id
                    FROM tillage t
                    JOIN subplots s ON t.subplot_id = s.subplot_id
                    JOIN plots p ON s.plot_id = p.plot_id

                    UNION ALL

                    SELECT 
                        p.business_id, s.plot_id, s.subplot_id, s.suffix, s.year,
                        so.date, 'Aussaat',
                        so.seeding_rate, CAST(so.row_distance AS TEXT), 'kg/ha',
                        NULL
                    FROM sowing so
                    JOIN subplots s ON so.subplot_id = s.subplot_id
                    JOIN plots p ON s.plot_id = p.plot_id

                    UNION ALL

                    SELECT 
                        p.business_id, s.plot_id, s.subplot_id, s.suffix, s.year,
                        fa.date, 'Düngung',
                        fa.amount, 'dt/ha', NULL,
                        fa.chemical_id
                    FROM fertilizer_applications fa
                    JOIN subplots s ON fa.subplot_id = s.subplot_id
                    JOIN plots p ON s.plot_id = p.plot_id

                    UNION ALL

                    SELECT 
                        p.business_id, s.plot_id, s.subplot_id, s.suffix, s.year,
                        pa.date, 'Pflanzenschutz',
                        pa.amount, 'l/ha', NULL,
                        pa.chemical_id
                    FROM pesticide_applications pa
                    JOIN subplots s ON pa.subplot_id = s.subplot_id
                    JOIN plots p ON s.plot_id = p.plot_id

                    UNION ALL

                    SELECT 
                        p.business_id, s.plot_id, s.subplot_id, s.suffix, s.year,
                        h.date, 'Ernte',
                        h.amount, CAST(h.harvest_index AS TEXT), 'dt/ha',
                        NULL
                    FROM harvests h
                    JOIN subplots s ON h.subplot_id = s.subplot_id
                    JOIN plots p ON s.plot_id = p.plot_id;
                ''')

        con.commit()

        con.commit()

def _buildTables():
    t1 = time.time()
    connection = sqlite3.connect("pask.db")
    cursor = connection.cursor()

    cursor.execute('''PRAGMA foreign_keys = ON;''')

    #Betrieb, Stammdaten
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS businesses (
        business_id INTEGER PRIMARY KEY,
        name TEXT,
        address TEXT,
        telephone TEXT,
        mail TEXT,
        registry TEXT
    );
    ''')


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS plots (
        plot_id INTEGER PRIMARY KEY,
        business_id INTEGER NOT NULL,
        flik TEXT NOT NULL,
        plot_nr INTEGER,
        size REAL,
        FOREIGN KEY (business_id) REFERENCES businesses (business_id)
    );
    ''')

    # TODO add field for geodata
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subplots (
        subplot_id INTEGER PRIMARY KEY,
        plot_id INTEGER NOT NULL,
        suffix TEXT,
        size REAL,
        year INTEGER,
        FOREIGN KEY (plot_id) REFERENCES plots (plot_id)
    );
    ''')


    # This can be expanded to hold rules for crop rotations, im not gonna focus on that, maybe later. For now, it
    # stays as a basic implementation
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS crops (
        crop_id INTEGER PRIMARY KEY,
        name TEXT,
        variety TEXT,
        cost REAL
    );
    ''')

    #Kultur, nachverfolgung von Kulturen auf Schlag
    # TODO is that really everything? check it
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cultures (
        culture_id INTEGER PRIMARY KEY,
        subplot_id INTEGER NOT NULL,
        crop_id INTEGER NOT NULL,
        FOREIGN KEY (subplot_id) REFERENCES subplots (subplot_id),
        FOREIGN KEY (crop_id) REFERENCES crops (crop_id)
    );
    ''')

    #Dünger, register für sorten
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fertilizers (
        chemical_id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        n REAL,
        p REAL,
        k REAL,
        mg REAL,
        ca REAL,
        cost REAL,
        identifier TEXT
    );
    ''')

    # Pesticides
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pesticides (
        chemical_id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        cost REAL,
        identifier TEXT
    );
    ''')

    #Bodenbearbeitung, nachverfolgung
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tillage (
        action_id INTEGER PRIMARY KEY,
        subplot_id INTEGER NOT NULL,
        date TEXT,
        type TEXT,
        tool TEXT,
        depth REAL,
        FOREIGN KEY (subplot_id) REFERENCES subplots (subplot_id)
    );
    ''')

    #aussaat, nachverfolgung
    # TODO prüfe ob es sinn ergibt die kultur hier rein zu packen, emergentes verhalten bei join via datum?
    # dafuq was i talking about???
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sowing (
        action_id INTEGER PRIMARY KEY,
        subplot_id INTEGER NOT NULL,
        date TEXT,
        seeding_rate REAL,
        row_distance REAL,
        FOREIGN KEY (subplot_id) REFERENCES subplots (subplot_id)
    );
    ''')

    #Ernte, nachverfolgung
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS harvests (
        action_id INTEGER PRIMARY KEY,
        subplot_id INTEGER NOT NULL,
        date TEXT,
        amount REAL,
        harvest_index REAL,
        FOREIGN KEY (subplot_id) REFERENCES subplots (subplot_id)
    );
    ''')

    #Düngung, nachverfolgung
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fertilizer_applications (
        action_id INTEGER PRIMARY KEY,
        subplot_id INTEGER NOT NULL,
        date TEXT,
        chemical_id INTEGER NOT NULL,
        amount REAL,
        FOREIGN KEY (subplot_id) REFERENCES subplots (subplot_id),
        FOREIGN KEY (chemical_id) REFERENCES fertilizers (chemical_id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pesticide_applications (
        action_id INTEGER PRIMARY KEY,
        subplot_id INTEGER NOT NULL,
        date TEXT,
        chemical_id INTEGER NOT NULL,
        amount REAL,
        FOREIGN KEY (subplot_id) REFERENCES subplots (subplot_id),
        FOREIGN KEY (chemical_id) REFERENCES pesticides (chemical_id)
    );''')

    connection.commit()
    connection.close()

    tdiff = time.time() - t1
    # print("Built DB in {} seconds.".format(tdiff))
