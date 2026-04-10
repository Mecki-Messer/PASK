import sqlite3
from builtins import object

from model import objects, enums


def delete(obj: object) -> int:
    """
    deletes an arbitrary item from the database

    :return an integer that servers as a status code, 0 = execution without failure
    """

    if isinstance(obj, objects.Business):
            query = "DELETE FROM businesses WHERE business_id = ?;"
            id_ = obj.business_id
    elif isinstance(obj, objects.Plot):
            query = "DELETE FROM plots WHERE plot_id = ?;"
            id_ = obj.plot_id
    elif isinstance(obj, objects.Subplot):
            query = "DELETE FROM subplots WHERE subplot_id = ?;"
            id_ = obj.subplot_id
    elif isinstance(obj, objects.Crop):
            query = "DELETE FROM crops WHERE crop_id = ?;"
            id_ = obj.crop_id
    elif isinstance(obj, objects.Culture):
        query = "DELETE FROM cultures WHERE culture_id = ?;"
        id_ = obj.culture_id
    elif isinstance(obj, objects.Fertilizer):
            query = "DELETE FROM fertilizers WHERE chemical_id = ?;"
            id_ = obj.chemical_id
    elif isinstance(obj, objects.Pesticide):
            query = "DELETE FROM pesticides WHERE chemical_id = ?;"
            id_ = obj.chemical_id
    elif isinstance(obj, objects.Tillage):
            query = "DELETE FROM tillage WHERE action_id = ?;"
            id_ = obj.action_id
    elif isinstance(obj, objects.Sowing):
            query = "DELETE FROM sowing WHERE action_id = ?;"
            id_ = obj.action_id
    elif isinstance(obj, objects.FertilizerApplication):
            query = "DELETE FROM fertilizer_applications WHERE action_id = ?;"
            id_ = obj.action_id
    elif isinstance(obj, objects.PesticideApplication):
            query = "DELETE FROM pesticide_applications WHERE action_id = ?;"
            id_ = obj.action_id
    elif isinstance(obj, objects.Harvest):
            query = "DELETE FROM harvests WHERE action_id = ?;"
            id_ = obj.action_id
    else:
        raise TypeError("Not a supported Data Type")

    try:
        with sqlite3.connect('pask.db') as con:
            cur = con.cursor()
            cur.execute('''PRAGMA foreign_keys = ON;''')
            cur.execute(query, (id_,))
            con.commit()
            # print("deleted item with ID {}".format(id_))
            return 0

    except sqlite3.OperationalError as e:
        con.rollback()
        raise e
    except sqlite3.IntegrityError as e:
        con.rollback()
        raise e
    except sqlite3.ProgrammingError as e:
        con.rollback()
        raise e

    finally:
        con.close()

def deleteAll():
    with sqlite3.connect('pask.db') as con:
        cur = con.cursor()
        cur.execute('''DELETE FROM businesses;''')
        cur.execute('''DELETE FROM plots;''')
        cur.execute('''DELETE FROM subplots;''')
        cur.execute('''DELETE FROM crops;''')
        cur.execute('''DELETE FROM cultures''')
        cur.execute('''DELETE FROM pesticides;''')
        cur.execute('''DELETE FROM fertilizers;''')
        cur.execute('''DELETE FROM fertilizer_applications;''')
        cur.execute('''DELETE FROM pesticide_applications;''')
        cur.execute('''DELETE FROM harvests;''')
        cur.execute('''DELETE FROM sowing;''')
        cur.execute('''DELETE FROM tillage;''')
        con.commit()
        cur.execute('''VACUUM;''')
        con.commit()