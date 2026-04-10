import sqlite3
from model.objects import Business, Plot, Subplot, Fertilizer, Tillage, Sowing, FertilizerApplication, \
    PesticideApplication, Harvest, Pesticide, Crop, Culture

from model.enums import ObjectType, IDPrefix

def _map_row_to_object(obj_type, data):
    if obj_type == ObjectType.BUSINESS:
        obj = Business(business_id=data[0], name=data[1], address=data[2], telephone=data[3], mail=data[4],
                       registry=data[5])
    elif obj_type == ObjectType.PLOT:
        obj = Plot(plot_id=data[0], business_id=data[1], flik=data[2], plot_nr=data[3], size=data[4])
    elif obj_type == ObjectType.SUBPLOT:
        obj = Subplot(subplot_id=data[0], plot_id=data[1], suffix=data[2], size=data[3], year=data[4])
    elif obj_type == ObjectType.CROP:
        obj = Crop(crop_id=data[0], name=data[1], variety=data[2], cost=data[3])
    elif obj_type == ObjectType.CULTURE:
        obj = Culture(culture_id=data[0], subplot_id=data[1], crop_id=data[2])
    elif obj_type == ObjectType.FERTILIZER:
        obj = Fertilizer(chemical_id=data[0], name=data[1], type=data[2], n=data[3], p=data[4], k=data[5],
                         mg=data[6], ca=data[7], cost=data[8], identifier=data[9])
    elif obj_type == ObjectType.PESTICIDE:
        obj = Pesticide(chemical_id=data[0], name=data[1], type=data[2], cost=data[3], identifier=data[4])
    elif obj_type == ObjectType.TILLAGE:
        obj = Tillage(action_id=data[0], subplot_id=data[1], action_date=data[2], type=data[3], tool=data[4],
                      depth=data[5])
    elif obj_type == ObjectType.SOWING:
        obj = Sowing(action_id=data[0], subplot_id=data[1], action_date=data[2], seeding_rate=data[3],
                     row_distance=data[4])
    elif obj_type == ObjectType.FERTILIZER_APPLICATION:
        obj = FertilizerApplication(action_id=data[0], subplot_id=data[1], action_date=data[2],
                                    chemical_id=data[3], amount=data[4])
    elif obj_type == ObjectType.PESTICIDE_APPLICATION:
        obj = PesticideApplication(action_id=data[0], subplot_id=data[1], action_date=data[2],
                                   chemical_id=data[3], amount=data[4])
    elif obj_type == ObjectType.HARVEST:
        obj = Harvest(action_id=data[0], subplot_id=data[1], action_date=data[2], amount=data[3],
                      harvest_index=data[4])
    else:
        raise TypeError("Kein valider ObjectType")

    return obj


# im trying to write a single method for all reads
def readAll(target) -> list[object]:
    if isinstance(target, str):
        type_enum = ObjectType.from_table_name(target)
    else:
        type_enum = target

    if type_enum is None:
        raise TypeError(f"Ungültiger Typ oder Tabellenname: {target}")

    table_name = type_enum.table_name
    result_list = []

    try:
        with sqlite3.connect("pask.db") as con:
            cur = con.cursor()
            cur.execute("""SELECT * FROM {}""".format(table_name))
            rows = cur.fetchall()

            for row in rows:
                obj = _map_row_to_object(type_enum, row)
                result_list.append(obj)

    except sqlite3.Error as e:
        raise e

    return result_list

def readOne(type_enum: ObjectType, id_enum: IDPrefix, id_: int) -> object:
    try:
        with sqlite3.connect("pask.db") as con:
            cur = con.cursor()
            cur.execute("""SELECT * FROM {} where {} = ?;""".format(type_enum, id_enum), (id_,))
            row = cur.fetchone()
    except sqlite3.OperationalError as e:
        raise e
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.ProgrammingError as e:
        raise e

    if type_enum == ObjectType.BUSINESS:
        data = Business(business_id=row[0], name=row[1], address=row[2], telephone=row[3], mail=row[4], registry=row[5])
    elif type_enum == ObjectType.PLOT:
        data = Plot(plot_id=row[0], business_id=row[1], flik=row[2], plot_nr=row[3], size=row[4])
    elif type_enum == ObjectType.SUBPLOT:
        data = Subplot(subplot_id=row[0], plot_id=row[1], suffix=row[2], size=row[3], year=row[4])
    elif type_enum == ObjectType.CROP:
        data = Crop(crop_id=row[0], name=row[1], variety=row[2], cost=row[3])
    elif type_enum == ObjectType.CULTURE:
        data = Culture(culture_id=row[0], subplot_id=row[1], crop_id=row[2])
    elif type_enum == ObjectType.FERTILIZER:
        data = Fertilizer(chemical_id=row[0], name=row[1], type=row[2], n=row[3], p=row[4], k=row[5], mg=row[6], ca=row[7], cost=row[8], identifier=row[9])
    elif type_enum == ObjectType.PESTICIDE:
        data = Pesticide(chemical_id=row[0], name=row[1], type=row[2], cost=row[3], identifier=row[4])
    elif type_enum == ObjectType.TILLAGE:
        data = Tillage(action_id=row[0], subplot_id=row[1], action_date=row[2], type=row[3], tool=row[4], depth=row[5])
    elif type_enum == ObjectType.SOWING:
        data = Sowing(action_id=row[0], subplot_id=row[1], action_date=row[2], seeding_rate=row[3], row_distance=row[4])
    elif type_enum == ObjectType.FERTILIZER_APPLICATION:
        data = FertilizerApplication(action_id=row[0], subplot_id=row[1], action_date=row[2], chemical_id=row[3], amount=row[4])
    elif type_enum == ObjectType.PESTICIDE_APPLICATION:
        data = PesticideApplication(action_id=row[0], subplot_id=row[1], action_date=row[2], chemical_id=row[3], amount=row[4])
    elif type_enum == ObjectType.HARVEST:
        data = Harvest(action_id=row[0], subplot_id=row[1], action_date=row[2], amount=row[3], harvest_index=row[4])
    else:
        raise TypeError("not a valid type")

    return data


def readFiltered(type_name: str, business_id: int):
    obj_type = ObjectType.from_table_name(type_name)
    nonspecific_data = [ObjectType.CROP, ObjectType.FERTILIZER, ObjectType.PESTICIDE]

    if obj_type in nonspecific_data:
        target = obj_type.table_name
        use_filter = False
    elif obj_type == ObjectType.PLOT:
        target = obj_type.table_name
        use_filter = True
    else:
        target = f"vi_{obj_type.table_name}_by_business"
        use_filter = True

    class_map = {
        ObjectType.PLOT: Plot,
        ObjectType.SUBPLOT: Subplot,
        ObjectType.TILLAGE: Tillage,
        ObjectType.SOWING: Sowing,
        ObjectType.FERTILIZER_APPLICATION: FertilizerApplication,
        ObjectType.PESTICIDE_APPLICATION: PesticideApplication,
        ObjectType.HARVEST: Harvest,
        ObjectType.CULTURE: Culture,
        ObjectType.CROP: Crop,
        ObjectType.FERTILIZER: Fertilizer,
        ObjectType.PESTICIDE: Pesticide
    }

    obj_class = class_map.get(obj_type)
    results = []

    try:
        with sqlite3.connect('pask.db') as con:
            cur = con.cursor()

            if use_filter:
                cur.execute(f"SELECT * FROM {target} WHERE business_id = ?", (business_id,))
            else:
                cur.execute(f"SELECT * FROM {target}")

            rows = cur.fetchall()

            for row in rows:
                data_row = row[:-1] if "vi_" in target else row
                obj = _map_row_to_object(obj_type, data_row)
                results.append(obj)

    except Exception as e:
        raise e

    return results


def get_plot_report(plot_id, business_id):
    with sqlite3.connect("pask.db") as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        query = """
            SELECT * FROM vi_plot_chronology 
            WHERE plot_id = ? AND business_id = ?
            ORDER BY subplot_year DESC, suffix ASC, date ASC
        """
        cursor.execute(query, (plot_id, business_id))
        return [dict(row) for row in cursor.fetchall()]