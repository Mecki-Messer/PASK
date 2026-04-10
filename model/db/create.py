import sqlite3
from model.objects import Business, Plot, Subplot, Fertilizer, Pesticide, Tillage, Sowing, FertilizerApplication, PesticideApplication, Harvest, Crop, Culture

# TODO unify into a single method

def insertBusiness(business: Business):
    """

    :param business: a Business object
    :return business: a Business object inlcuding its database ID
    """
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''PRAGMA foreign_keys = ON;''')
        res = cur.execute('''INSERT INTO businesses (name, address, telephone, mail, registry) VALUES (?, ?, ?, ?, ?);''',
                          (business.name, business.address, business.telephone, business.mail, business.registry))
        business.business_id = res.lastrowid
        con.commit()
        return business

def insertPlot(plot: Plot):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''PRAGMA foreign_keys = ON;''')
        res = cur.execute('''INSERT INTO plots (business_id, flik, plot_nr, size) VALUES (?, ?, ?, ?);''',
                          (plot.business_id, plot.flik, plot.plot_nr, plot.size))
        plot.plot_id = res.lastrowid
        con.commit()
        return plot

def insertSubplot(subplot: Subplot):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''PRAGMA foreign_keys = ON;''')
        res = cur.execute('''INSERT INTO subplots (plot_id, suffix, size, year) VALUES (?, ?, ?, ?);''',
                          (subplot.plot_id, subplot.suffix, subplot.size, subplot.year))
        subplot.subplot_id = res.lastrowid
        con.commit()
        return subplot

def insertCulture(culture: Culture):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''PRAGMA foreign_keys = ON;''')
        res = cur.execute('''INSERT INTO cultures (subplot_id, crop_id) VALUES (?, ?)''',
                          (culture.subplot_id, culture.crop_id))
        culture.culture_id = res.lastrowid
        con.commit()
        return culture

def insertCrop(crop: Crop):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''PRAGMA foreign_keys = ON;''')
        res = cur.execute('''INSERT INTO crops (name, variety, cost) VALUES (?, ?, ?)''',
                          (crop.name, crop.variety, crop.cost))
        crop.crop_id = res.lastrowid
        con.commit()
        return crop

def insertFertilizer(fertilizer: Fertilizer):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''PRAGMA foreign_keys = ON;''')
        res = cur.execute('''INSERT INTO fertilizers (name, type, n, p, k, mg, ca, cost, identifier) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                          (fertilizer.name, fertilizer.type, fertilizer.n, fertilizer.p, fertilizer.k, fertilizer.mg, fertilizer.ca, fertilizer.cost, fertilizer.identifier))
        fertilizer.chemical_id = res.lastrowid
        con.commit()
        return fertilizer

def insertPesticide(pesticide: Pesticide):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''PRAGMA foreign_keys = ON;''')
        res = cur.execute('''INSERT INTO pesticides (name, type, identifier, cost) VALUES (?, ?, ?, ?);''',
                          (pesticide.name, pesticide.type, pesticide.identifier, pesticide.cost))
        pesticide.chemical_id = res.lastrowid
        con.commit()
        return pesticide

def insertTillage(action: Tillage):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''PRAGMA foreign_keys = ON;''')
        res = cur.execute('''INSERT INTO tillage (subplot_id, date, type, tool, depth) VALUES (?, ?, ?, ?, ?);''',
                          (action.subplot_id, action.action_date, action.type, action.tool, action.depth))
        action.action_id = res.lastrowid
        con.commit()
        return action

def insertSowing(action: Sowing):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''PRAGMA foreign_keys = ON;''')
        res = cur.execute('''INSERT INTO sowing (subplot_id, date, seeding_rate, row_distance) VALUES (?, ?, ?, ?);''',
                          (action.subplot_id, action.action_date, action.seeding_rate, action.row_distance))
        action.action_id = res.lastrowid
        con.commit()
        return action

def insertFertilizerApplication(action: FertilizerApplication):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''PRAGMA foreign_keys = ON;''')
        res = cur.execute('''INSERT INTO fertilizer_applications (subplot_id, date, chemical_id, amount) VALUES (?, ?, ?, ?)''',
                          (action.subplot_id, action.action_date, action.chemical_id, action.amount))
        action.action_id = res.lastrowid
        con.commit()
        return action

def insertPesticideApplication(action: PesticideApplication):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''PRAGMA foreign_keys = ON;''')
        res = cur.execute('''INSERT INTO pesticide_applications (subplot_id, date, chemical_id, amount) VALUES (?, ?, ?, ?)''',
                          (action.subplot_id, action.action_date, action.chemical_id, action.amount))
        action.action_id = res.lastrowid
        con.commit()
        return action

def insertHarvest(action: Harvest):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''PRAGMA foreign_keys = ON;''')
        res = cur.execute('''INSERT INTO harvests (subplot_id, date, amount, harvest_index) VALUES (?, ?, ?, ?)''',
                          (action.subplot_id, action.action_date, action.amount, action.harvest_index))
        action.action_id = res.lastrowid
        con.commit()
        return action