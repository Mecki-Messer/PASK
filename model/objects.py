import datetime

from typing import override
from dataclasses import dataclass
from model.enums import FertilizerType, PesticideType, TillageType


# TODO prüfe ob db anschluss innerhalb der klassen sinn macht, gerade bei schlag und subschlag, möglicherweise update/delete statements insgesamt !DONE!
# Nope, nope the fuck right out of there, you will enter the land of circular imports and other weird shit, im leaving this here as a warning


@dataclass
class DatabaseEntry:
    id_: int = None

@dataclass
class Business:
    """Provides an abstract Data type that mirrors the scheme of the "Business" table"""
    name: str
    address: str
    telephone: str
    mail: str
    registry: str
    business_id: int = None

    @override
    def __str__(self):
        return "Betrieb(id={}, name={}, address={}, telephone={}, mail={}, registry={})".format(self.business_id, self.name, self.address, self.telephone, self.mail, self.registry)


@dataclass
class Subplot:
    """
    TODO Docstring
    """
    plot_id: int
    suffix: str
    size: float
    year: int
    subplot_id: int = None

    @override
    def __str__(self):
        return "Subschlag(subschlag_id={}, plot_id={}, suffix={}, year={}, size={})".format(self.subplot_id, self.plot_id, self.suffix, self.year, self.size)


@dataclass
class Plot:
    """
    TODO Docstring
    """
    business_id: int
    flik: str
    plot_nr: int
    size: float
    plot_id: int = None

    @override
    def __str__(self):
        return "Schlag(plot_id={}, business_id={}, flik={}, size={})".format(self.plot_id, self.business_id, self.flik, self.size)


@dataclass
class Crop:
    name: str
    variety: str
    cost: float
    crop_id: int = None

    @override
    def __str__(self):
        return "Crop(crop_id={}, name={}, variety={}, cost={})".format(self.crop_id, self.name, self.variety, self.cost)


@dataclass
class Culture:
    subplot_id: int
    crop_id: int
    culture_id: int = None

    @override
    def __str__(self):
        return "Culture(culture_id={}, subplot_id={}, crop_id={})".format(self.culture_id, self.subplot_id, self.crop_id)


@dataclass(kw_only=True)
class Agrochemicals:
    """
    TODO Docstring
    """
    name: str
    cost: float
    identifier: str
    chemical_id: int = None


@dataclass(kw_only=True)
class Pesticide(Agrochemicals):
    """
    TODO Docstring
    """
    type: PesticideType

    @override
    def __str__(self):
        return "Pesticide(chemical_id={}, name={}, cost={}, identifier={}, pesticide_type={})".format(
            self.chemical_id, self.name, self.cost, self.identifier, self.type)


@dataclass(kw_only=True)
class Fertilizer(Agrochemicals):
    """
    TODO Docstring
    """
    type: FertilizerType
    n: float
    p: float
    k: float
    mg: float
    ca: float

    @override
    def __str__(self):
        return "Duenger(id={}, name={}, duengertype={}, n={}, p={}, k={}, mg={}, ca={}, preis={})".format(
            self.chemical_id, self.name, self.type, self.n, self.p, self.k, self.mg, self.ca, self.cost)



@dataclass(kw_only=True)
class Action:
    """
    TODO Docstring
    """
    subplot_id: int
    action_date: datetime.date
    action_id: int = None

    @override
    def __str__(self):
        return "Massnahme(massnahme_id={}, subschlag_id={}, massnahme_date={})".format(self.action_id, self.subplot_id, self.action_date)


@dataclass(kw_only=True)
class Sowing(Action):
    """
    TODO Docstring
    TODO add override for __str__ method
    TODO maybe add a field for crop id, but this might be redundant, maybe this could also set a culture?
    """
    seeding_rate: float
    row_distance: float


@dataclass(kw_only=True)
class Harvest(Action):
    """
    TODO Docstring
    TODO add override for __str__ method
    """
    amount: float
    harvest_index: float


@dataclass(kw_only=True)
class FertilizerApplication(Action):
    """
    TODO Docstring
    TODO add override for __str__ method
    """
    chemical_id: int
    amount: float


@dataclass(kw_only=True)
class PesticideApplication(Action):
    """
    TODO Docstring
    TODO add override for __str__ method
    """
    chemical_id: int
    amount: float

@dataclass(kw_only=True)
class Tillage(Action):
    """
    TODO Docstring
    TODO add override for __str__ method
    """
    type: TillageType
    tool: str
    depth: float

