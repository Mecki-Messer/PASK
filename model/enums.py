from enum import Enum, StrEnum


class FertilizerType(StrEnum):
    ORGANIC = 'ORGANIC'
    MINERAL = 'MINERAL'

class TillageType(StrEnum):
    BASE = 'BASE'
    SECONDARY = 'SECONDARY'

class PesticideType(StrEnum):
    HERBICIDE = 'HERBICIDE'
    PESTICIDE = 'PESTICIDE'
    FUNGICIDE = 'FUNGICIDE'


class ObjectType(Enum):

    #Format: (Dropdown_Name, ID_Prefix_Key)
    BUSINESS = ("businesses", "BUSINESS")
    PLOT = ("plots", "PLOT")
    SUBPLOT = ("subplots", "SUBPLOT")
    CROP = ("crops", "CROP")
    CULTURE = ("cultures", "CULTURE")
    FERTILIZER = ("fertilizers", "CHEMICAL")
    PESTICIDE = ("pesticides", "CHEMICAL")
    TILLAGE = ("tillage", "ACTION")
    SOWING = ("sowing", "ACTION")
    FERTILIZER_APPLICATION = ("fertilizer_applications", "ACTION")
    PESTICIDE_APPLICATION = ("pesticide_applications", "ACTION")
    HARVEST = ("harvests", "ACTION")

    @property
    def table_name(self):
        return self.value[0]

    @property
    def prefix(self):
        return self.value[1]

    @classmethod
    def from_table_name(cls, name):
        for member in cls:
            if member.table_name == name:
                return member
        return None

class IDPrefix(StrEnum):
    BUSINESS = "business_id"
    PLOT = "plot_id"
    SUBPLOT = "subplot_id"
    CROP = "crop_id"
    CULTURE = "culture_id"
    CHEMICAL = "chemical_id"
    ACTION = "action_id"


