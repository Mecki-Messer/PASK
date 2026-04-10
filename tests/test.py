import datetime
import time
import sqlite3
import unittest
import random
from typing import override

from model.db import buildDB, create, delete, read
from model import objects
from model.enums import FertilizerType, PesticideType, TillageType, ObjectType, IDPrefix


def populateDB():
    test_fertilizer = objects.Fertilizer(name="test_fertilizer", type=FertilizerType.MINERAL, n=random.random(),
                                         p=random.random(), k=random.random(), mg=random.random(), ca=random.random(),
                                         cost=random.randint(20, 100), identifier="test")
    test_pesticide = objects.Pesticide(name="test_pesticide", type=PesticideType.PESTICIDE, identifier="test",
                                       cost=random.randint(20, 100))
    test_crop = objects.Crop(name="test_crop", variety="test_variety", cost=random.randint(10, 50))
    test_fertilizer = create.insertFertilizer(test_fertilizer)
    test_pesticide = create.insertPesticide(test_pesticide)
    test_crop = create.insertCrop(test_crop)

    for i in range(10):
        test_business = objects.Business("business" + str(i), "test", "1", "test", "test")
        test_business = create.insertBusiness(test_business)
        for j in range(random.randint(1, 5)):
            plot_size = random.randint(10, 20)
            test_plot = objects.Plot(business_id=test_business.business_id, flik="testflik", plot_nr=j,size=plot_size)
            test_plot = create.insertPlot(test_plot)
            subplot_count = random.randint(1, 4)
            for k in range(subplot_count):
                test_subplot = objects.Subplot(test_plot.plot_id, str(k), plot_size / subplot_count, 2026)
                test_subplot = create.insertSubplot(test_subplot)

                test_tilling = objects.Tillage(subplot_id=test_subplot.subplot_id, action_date=datetime.date(2025, random.randint(6, 9), random.randint(1, 29)), type=TillageType.BASE, tool="plow", depth=30)
                test_sowing = objects.Sowing(subplot_id=test_subplot.subplot_id, action_date=datetime.date(2025, 8, random.randint(1, 29)), seeding_rate=2.5, row_distance=20)
                test_fertilizer_application = objects.FertilizerApplication(subplot_id=test_subplot.subplot_id, action_date=datetime.date(2026, random.randint(3, 5), random.randint(1, 29)), chemical_id=test_fertilizer.chemical_id, amount=random.randint(1, 100))
                test_pesticide_application = objects.PesticideApplication(subplot_id=test_subplot.subplot_id, action_date=datetime.date(2026, random.randint(3, 5), random.randint(1, 29)), chemical_id=test_pesticide.chemical_id, amount=100)
                test_harvest = objects.Harvest(subplot_id=test_subplot.subplot_id, action_date=datetime.date(2026, random.randint(4, 7), random.randint(1, 29)), amount=120, harvest_index=0.7)

                create.insertTillage(test_tilling)
                create.insertSowing(test_sowing)
                create.insertFertilizerApplication(test_fertilizer_application)
                create.insertPesticideApplication(test_pesticide_application)
                create.insertHarvest(test_harvest)


class TestInsertion(unittest.TestCase):
    # basically what we are testing for is whether the inserted object is returned with an ID
    # this is indicative of a successful insertion
    # no logic is tested here directly
    # TODO add tests that check for foreign key constraints (plot, subplot and some more)

    @override
    def setUp(self):
        buildDB.buildTables()

    @override
    def tearDown(self):
        delete.deleteAll()

    def test_business(self):
        business = objects.Business("Oma Ducks Hof", "Am Hügel 1, 47110 Entenhausen", "123456789",
                                    "omaduck@dagomail.ent",
                                    "ENT313")
        business = create.insertBusiness(business)
        self.assertTrue(business.business_id is not None)

    def test_plot(self):
        business = objects.Business("test", "test", "test", "test", "test")
        business = create.insertBusiness(business)

        plot = objects.Plot(flik="test", plot_nr=1, size=20, business_id=business.business_id)
        plot = create.insertPlot(plot)
        self.assertTrue(plot.plot_nr is not None)

    def test_subplot(self):
        business = objects.Business("test", "test", "test", "test", "test")
        business = create.insertBusiness(business)
        plot = objects.Plot(flik="ENTHA420131269", plot_nr=1, size=20.7, business_id=business.business_id)
        plot = create.insertPlot(plot)

        subplot = objects.Subplot(plot.plot_id, "a", 20.7, 2026)
        subplot = create.insertSubplot(subplot)
        self.assertTrue(subplot.subplot_id is not None)

    def test_crop(self):
        crop = objects.Crop("testcrop", "test variety", 20)
        crop = create.insertCrop(crop)
        self.assertTrue(crop.crop_id is not None)

    def test_culture(self):
        business = objects.Business("test", "test", "test", "test", "test")
        business = create.insertBusiness(business)
        plot = objects.Plot(flik="ENTHA420131269", plot_nr=1, size=20.7, business_id=business.business_id)
        plot = create.insertPlot(plot)
        subplot = objects.Subplot(plot.plot_id, "a", 20.7, 2026)
        subplot = create.insertSubplot(subplot)
        crop = objects.Crop("testcrop", "test variety", 20)
        crop = create.insertCrop(crop)

        culture = objects.Culture(subplot.subplot_id, crop.crop_id)
        culture = create.insertCulture(culture)
        self.assertTrue(culture.culture_id is not None)

    def test_fertilizer(self):
        fertilizer = objects.Fertilizer(name="Dagogrow Ultra", type=FertilizerType.MINERAL, n=1, p=1, k=1,
                                        mg=1, ca=1, cost=99.9, identifier="test")
        fertilizer = create.insertFertilizer(fertilizer)
        self.assertTrue(fertilizer.chemical_id is not None)

    def test_pesticide(self):
        pesticide = objects.Pesticide(name="Totgiftikai", cost=42, identifier="test", type=PesticideType.PESTICIDE)
        pesticide = create.insertPesticide(pesticide)
        self.assertTrue(pesticide.chemical_id is not None)

    def test_tillage(self):
        business = objects.Business("test", "test", "test", "test", "test")
        business = create.insertBusiness(business)
        plot = objects.Plot(flik="ENTHA420131269", plot_nr=1, size=20.7, business_id=business.business_id)
        plot = create.insertPlot(plot)
        subplot = objects.Subplot(plot.plot_id, "a", 20.7, 2026)
        subplot = create.insertSubplot(subplot)

        action1 = objects.Tillage(subplot_id=subplot.subplot_id, action_date=datetime.date(2025, 8, 7), work_type=TillageType.BASE, tool="plow", depth=30)
        action1 = create.insertTillage(action1)
        self.assertTrue(action1.action_id is not None)

    def test_sowing(self):
        business = objects.Business("test", "test", "test", "test", "test")
        business = create.insertBusiness(business)
        plot = objects.Plot(flik="ENTHA420131269", plot_nr=1, size=20.7, business_id=business.business_id)
        plot = create.insertPlot(plot)
        subplot = objects.Subplot(plot.plot_id, "a", 20.7, 2026)
        subplot = create.insertSubplot(subplot)

        action2 = objects.Sowing(subplot_id=subplot.subplot_id, action_date=datetime.date(2025, 10, 16), seeding_rate=2.5, row_distance=20)
        action2 = create.insertSowing(action2)
        self.assertTrue(action2.action_id is not None)

    def test_fertilizerApplication(self):
        business = objects.Business("test", "test", "test", "test", "test")
        business = create.insertBusiness(business)
        plot = objects.Plot(flik="ENTHA420131269", plot_nr=1, size=20.7, business_id=business.business_id)
        plot = create.insertPlot(plot)
        subplot = objects.Subplot(plot.plot_id, "a", 20.7, 2026)
        subplot = create.insertSubplot(subplot)
        fertilizer = objects.Fertilizer(name="Dagogrow Ultra", type=FertilizerType.MINERAL, n=1, p=1, k=1,
                                        mg=1, ca=1, cost=99.9, identifier="test")
        fertilizer = create.insertFertilizer(fertilizer)

        action3 = objects.FertilizerApplication(subplot_id=subplot.subplot_id, action_date=datetime.date(2026, 3, 5), chemical_id=fertilizer.chemical_id, amount=100)
        action3 = create.insertFertilizerApplication(action3)
        self.assertTrue(action3.action_id is not None)

    def test_pesticideApplication(self):
        business = objects.Business("test", "test", "test", "test", "test")
        business = create.insertBusiness(business)
        plot = objects.Plot(flik="ENTHA420131269", plot_nr=1, size=20.7, business_id=business.business_id)
        plot = create.insertPlot(plot)
        subplot = objects.Subplot(plot.plot_id, "a", 20.7, 2026)
        subplot = create.insertSubplot(subplot)
        pesticide = objects.Pesticide(name="Totgiftikai", cost=42, identifier="test", type=PesticideType.PESTICIDE)
        pesticide = create.insertPesticide(pesticide)

        action4 = objects.PesticideApplication(subplot_id=subplot.subplot_id, action_date=datetime.date(2026, 4, 1), chemical_id=pesticide.chemical_id, amount=100)
        action4 = create.insertPesticideApplication(action4)
        self.assertTrue(action4.action_id is not None)

    def test_harvest(self):
        business = objects.Business("test", "test", "test", "test", "test")
        business = create.insertBusiness(business)
        plot = objects.Plot(flik="ENTHA420131269", plot_nr=1, size=20.7, business_id=business.business_id)
        plot = create.insertPlot(plot)
        subplot = objects.Subplot(plot.plot_id, "a", 20.7, 2026)
        subplot = create.insertSubplot(subplot)

        action5 = objects.Harvest(subplot_id=subplot.subplot_id, action_date=datetime.date(2026, 6, 19), amount=120, harvest_index=0.7)
        action5 = create.insertHarvest(action5)
        self.assertTrue(action5.action_id is not None)

    def test_missing_fk(self):
        no_good_plot = objects.Plot(99999, "", 1, 1)
        self.assertRaises(sqlite3.IntegrityError, create.insertPlot, no_good_plot)


class TestRead(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        populateDB()
        super(TestRead, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        delete.deleteAll()
        super(TestRead, cls).tearDownClass()


    def test_readAllBusinesses(self):
        results = read.readAll(ObjectType.BUSINESS)
        self.assertEqual(len(results), 10)

    def test_readOneBusiness(self):
        self.assertTrue(isinstance(read.readOne(ObjectType.BUSINESS, IDPrefix.BUSINESS, 1), objects.Business) == True)

    def test_readAllPlots(self):
        self.assertTrue(len(read.readAll(ObjectType.PLOT)) >= 1)

    def test_readOnePlot(self):
        self.assertTrue(isinstance(read.readOne(ObjectType.PLOT, IDPrefix.PLOT, 1), objects.Plot) == True)

    def test_readAllSubplots(self):
        self.assertTrue(len(read.readAll(ObjectType.SUBPLOT)) >= 1)

    def test_readOneSubplot(self):
        self.assertTrue(isinstance(read.readOne(ObjectType.SUBPLOT, IDPrefix.SUBPLOT, 1), objects.Subplot) == True)

    def test_readAllFertilizers(self):
        self.assertTrue(len(read.readAll(ObjectType.FERTILIZER)) >= 1)

    def test_readAllPesticides(self):
        self.assertTrue(len(read.readAll(ObjectType.PESTICIDE)) >= 1)

    def test_readAllSowing(self):
        self.assertTrue(len(read.readAll(ObjectType.SOWING)) >= 1)

    def test_readAllTillage(self):
        self.assertTrue(len(read.readAll(ObjectType.TILLAGE)) >= 1)

    def test_readAllFertilizerApplications(self):
        self.assertTrue(len(read.readAll(ObjectType.FERTILIZER_APPLICATION)) >= 1)

    def test_readAllPesticideApplications(self):
        self.assertTrue(len(read.readAll(ObjectType.PESTICIDE_APPLICATION)) >= 1)

    def test_readAllHarvests(self):
        self.assertTrue(len(read.readAll(ObjectType.HARVEST)) >= 1)

    # will also raise with a syntax error in the query TODO make its own test
    def test_readAll_raise_OperationalError(self):
        self.assertRaises(sqlite3.OperationalError, read.readAll, "thisTableDoesntExist")

    # test for insertion^^
    def test_readAll_raise_ProgrammingError(self):
        self.assertRaises(sqlite3.ProgrammingError, read.readAll, "businesses;SELECT * FROM plots;")


class TestUpdate(unittest.TestCase):

    @override
    def setUp(self):
        buildDB.buildTables()

    @override
    def tearDown(self):
        delete.deleteAll()


class TestDelete(unittest.TestCase):

    @override
    def setUp(self):
        buildDB.buildTables()

    @override
    def tearDown(self):
        delete.deleteAll()

    def test_delete_1_raiseTypeError_str(self):
        # basic raise test representative of types not supported by the delete method
        self.assertRaises(TypeError, delete.delete, "this should raise a TypeError")

    def test_delete_2_raiseTypeError_int(self):
        # again this should raise a TypeError, this test checks for raw id input but is honestly redundant
        self.assertRaises(TypeError, delete.delete, 1)

    def test_delete_3_FKConstraints(self):
        business = objects.Business("test", "test", 1, "test", "test")
        business = create.insertBusiness(business)
        plot = objects.Plot(plot_nr=1, flik="ENTHA420131269", size=20.7, plot_id=1, business_id=business.business_id)
        plot = create.insertPlot(plot)
        # in this case deletion should fail because of foreign key constraints
        self.assertRaises(sqlite3.IntegrityError, delete.delete, business)

    def test_delete_4(self):
        business = objects.Business("test", "test", 1, "test", "test")
        business = create.insertBusiness(business)
        plot = objects.Plot(plot_nr=1, flik="ENTHA420131269", size=20.7, plot_id=1, business_id=business.business_id)
        plot = create.insertPlot(plot)

        delete.delete(plot)
        # This deletion should succeed and return with 0
        self.assertEqual(delete.delete(business), 0)



if __name__ == "__main__":
    random.seed(time.time())
    unittest.main()
