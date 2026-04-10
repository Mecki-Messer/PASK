import sqlite3
from model.objects import Business, Plot, Subplot, Fertilizer, Tillage, Sowing, FertilizerApplication, \
    PesticideApplication, Harvest, Pesticide, Culture, Crop

# TODO unify into a single method

def updateBusiness(business: Business):
    """
    TODO Docstring
    """
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE businesses SET name=?, address=?, telephone=?, mail=?, registry=? WHERE business_id=?;''',
                    (business.name, business.address, business.telephone, business.mail, business.registry, business.business_id))
        con.commit()

def updatePlot(plot: Plot):
    """
    TODO Docstring
    """
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE plots SET flik=?, plot_nr=?, size=?, business_id=? WHERE plot_id=?;''',
                    (plot.flik, plot.plot_nr, plot.size, plot.business_id, plot.plot_id))
        con.commit()

def updateSubplot(subplot: Subplot):
    """
    TODO Docstring
    TODO rest of the statement
    """
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE subplots SET plot_id=?, suffix=?, size=?, year=? WHERE subplot_id=?;''',
                    (subplot.plot_id, subplot.suffix, subplot.size, subplot.year, subplot.subplot_id))

def updateCulture(culture: Culture):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE cultures SET subplot_id=?, crop_id=? WHERE culture_id=?;''',
                    (culture.subplot_id, culture.crop_id, culture.culture_id))

def updateCrop(crop: Crop):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE crops SET name=?, variety=?, cost=? WHERE crop_id=?;''',
                    (crop.name, crop.variety, crop.cost, crop.crop_id))

def updateFertilizer(fertilizer: Fertilizer):
    """
    TODO Docstring
    """
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE fertilizers SET name=?, type=?, n=?, p=?, k=?, mg=?, ca=?, cost=? WHERE chemical_id=?;''',
                    (fertilizer.name, fertilizer.type, fertilizer.n, fertilizer.p, fertilizer.k, fertilizer.mg, fertilizer.ca, fertilizer.cost, fertilizer.chemical_id))
        con.commit()

def updatePesticide(pesticide: Pesticide):
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE pesticides SET name=?, type=?, identifier=?, cost=? WHERE chemical_id=?;''',
                    (pesticide.name, pesticide.type, pesticide.identifier, pesticide.cost, pesticide.chemical_id))

def updateTillage(action: Tillage):
    """
    TODO Docstring
    """
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE tillage SET subplot_id=?, date=?, type=?, tool=?, depth=? WHERE action_id=?;''',
                    (action.subplot_id, action.action_date, action.type, action.tool, action.depth, action.action_id))
        con.commit()

def updateSowing(action: Sowing):
    """
    TODO Docstring
    """
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE sowing SET subplot_id=?, date=?, seeding_rate=?, row_distance=? WHERE action_id=?;''',
                    (action.subplot_id, action.action_date, action.seeding_rate, action.row_distance, action.action_id))
        con.commit()

def updateFertilizerApplication(action: FertilizerApplication):
    """
    TODO Docstring
    """
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE fertilizer_applications SET subplot_id=?, date=?, chemical_id=?, amount=? WHERE action_id=?;''',
                    (action.subplot_id, action.action_date, action.chemical_id, action.amount, action.action_id))
        con.commit()

def updatePesticideApplication(action: PesticideApplication):
    """
    TODO Docstring
    """
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE pesticide_applications SET subplot_id=?, date=?, chemical_id=?, amount=? WHERE action_id=?;''',
                    (action.subplot_id, action.action_date, action.chemical_id, action.amount, action.action_id))
        con.commit()

def updateHarvest(action: Harvest):
    """
    TODO Docstring
    """
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE harvests SET subplot_id=?, date=?, amount=?, harvest_index=? WHERE action_id=?;''',
                    (action.subplot_id, action.action_date, action.amount, action.harvest_index, action.action_id))
        con.commit()