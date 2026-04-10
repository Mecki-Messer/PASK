from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox, QFileDialog
from PyQt5.QtCore import QDate
import inspect

from view.forms.input_form_sidebar import Ui_input_form_sidebar
from view.forms.input_form_plot_ui import Ui_Form as Ui_form_plot
from view.forms.input_form_subplot_ui import Ui_Form as Ui_form_subplot
from view.forms.input_form_crop_ui import Ui_Form as Ui_form_crop
from view.forms.input_form_culture_ui import Ui_Form as Ui_form_culture
from view.forms.input_agrochemicals_base_ui import Ui_Form as Ui_form_agrochemicals
from view.forms.input_form_fertilizer_ui import Ui_Form as Ui_form_fertilizer
from view.forms.input_form_pesticdes_ui import Ui_Form as Ui_form_pesticide
from view.forms.input_action_base_ui import Ui_Form as Ui_form_action
from view.forms.input_form_tillage_ui import Ui_Form as Ui_form_tillage
from view.forms.input_form_sowing_ui import Ui_Form as Ui_form_sowing
from view.forms.input_form_fertilizerApplication_ui import Ui_Form as Ui_form_fertilizer_application
from view.forms.input_form_pesticideApplication_ui import Ui_Form as Ui_form_pesticide_application
from view.forms.input_form_harvest_ui import Ui_Form as Ui_form_harvest

import tests.test
from model import objects, export
from model.db import read, delete, create, update
from model.enums import ObjectType, IDPrefix, FertilizerType, PesticideType, TillageType
from view.main_view import MainView
from view.data_model import GenericTableModel

# TODO this code is a mess, clean up, shuffle some methods around, maybe switch entirely from match cases/elifs to generic handling
class MainController:
    def __init__(self, view: MainView):
        self.view = view
        #ID so we know which business we currently use
        self.business_id = None
        #ID of an object currently selected in the table
        self.current_id = None

        self.table_model = None

        self.current_form_widget = None
        self.sidebar_input_master_ui = None
        self.base_form = None
        self.active_form = None

        self.db_map = {
            ObjectType.BUSINESS: (objects.Business, create.insertBusiness, update.updateBusiness),
            ObjectType.PLOT: (objects.Plot, create.insertPlot, update.updatePlot),
            ObjectType.SUBPLOT: (objects.Subplot, create.insertSubplot, update.updateSubplot),
            ObjectType.CROP: (objects.Crop, create.insertCrop, update.updateCrop),
            ObjectType.CULTURE: (objects.Culture, create.insertCulture, update.updateCulture),
            ObjectType.FERTILIZER: (objects.Fertilizer, create.insertFertilizer, update.updateFertilizer),
            ObjectType.PESTICIDE: (objects.Pesticide, create.insertPesticide, update.updatePesticide),
            ObjectType.TILLAGE: (objects.Tillage, create.insertTillage, update.updateTillage),
            ObjectType.SOWING: (objects.Sowing, create.insertSowing, update.updateSowing),
            ObjectType.FERTILIZER_APPLICATION: (objects.FertilizerApplication, create.insertFertilizerApplication, update.updateFertilizerApplication),
            ObjectType.PESTICIDE_APPLICATION: (objects.PesticideApplication, create.insertPesticideApplication, update.updatePesticideApplication),
            ObjectType.HARVEST: (objects.Harvest, create.insertHarvest, update.updateHarvest)
        }

        self.view.ui.dropdown_select_betrieb.activated.connect(self.on_business_select)
        self.view.ui.dropdown_select_view.activated.connect(self.on_view_select)
        self.view.ui.tableView.clicked.connect(self.on_table_select)
        self.view.ui.actionPopulate_DB.triggered.connect(self.on_debug_populate)
        self.view.ui.actionClear_DB.triggered.connect(self.on_debug_clearAll)
        self.view.ui.actionExport.triggered.connect(self.on_menu_export_csv_clicked)

        self.refresh_form(ObjectType.PLOT.value)

        self.load_initial_data()

    def load_initial_data(self):
        self.view.display_message("Loading initial data")
        businesses = read.readAll(ObjectType.BUSINESS.table_name)
        for business in businesses:
            self.view.ui.dropdown_select_betrieb.addItem(business.name, business.business_id)

        for type_ in ObjectType:
            self.view.ui.dropdown_select_view.addItem(type_.table_name, type_.name)

    def on_debug_populate(self):
        tests.test.populateDB()
        #self.load_initial_data()
        self.view.display_message("Populated DB")


    def on_debug_clearAll(self):
        delete.deleteAll()
        self.view.display_message("Clearing DB")

    def on_business_select(self, index):
        business_id = self.view.ui.dropdown_select_betrieb.currentData()
        self.business_id = business_id
        self.view.display_message("Betrieb mit ID {} geladen".format(business_id))

    def on_view_select(self, index):
        table_name = self.view.ui.dropdown_select_view.currentText()

        raw_data = read.readFiltered(table_name, self.business_id)
        self.refresh_form(table_name)
        if not raw_data:
            self.view.display_message("Keine Daten gefunden.")
            return

        headers = list(raw_data[0].__dict__.keys())

        self.table_model = GenericTableModel(raw_data, headers)
        self.view.ui.tableView.setModel(self.table_model)
        self.view.ui.tableView.resizeColumnsToContents()

    def on_menu_export_csv_clicked(self):
        plot_id = getattr(self, 'current_id', None)
        if not plot_id:
            self.view.display_message("Nichts ausgewählt.")
            return

        filename, _ = QFileDialog.getSaveFileName(self.view, "Speichern", "", "CSV (*.csv)")

        if filename:
            try:
                export.export_plot_report_to_csv(plot_id, self.business_id, filename)
                self.view.display_message("Export abgeschlossen.")
            except Exception as e:
                self.view.display_message(f"Kritischer Export-Fehler: {str(e)}")

    def on_input_form_update_save(self):
        #Dispatcher method to decide create or update
        if hasattr(self, 'current_id') and self.current_id is not None:
            self._handle_update()
        else:
            self._handle_create()

    def _handle_create(self):
        table_name = self.view.ui.dropdown_select_view.currentText()
        obj_type = ObjectType.from_table_name(table_name)

        if not obj_type:
            self.view.display_message(f"Fehler: Typ {table_name} unbekannt.")
            return

        data = self._collect_form_data()

        if "business_id" in data or obj_type == ObjectType.PLOT:
            data["business_id"] = self.business_id

        try:
            obj_class, insert_func, _ = self.db_map[obj_type]

            new_obj = obj_class(**data)
            insert_func(new_obj)

            self.view.display_message(f"{table_name} erfolgreich erstellt.")
            self.on_view_select(None)
        except Exception as e:
            raise e

    def _handle_update(self):
        table_name = self.view.ui.dropdown_select_view.currentText()
        obj_type = ObjectType.from_table_name(table_name)

        if not obj_type:
            return

        data = self._collect_form_data()

        try:
            obj_class, _, update_func = self.db_map[obj_type]

            id_attr_name = getattr(IDPrefix, obj_type.prefix).value
            data[id_attr_name] = self.current_id

            updated_obj = obj_class(**data)
            update_func(updated_obj)

            self.view.display_message(f"ID {self.current_id} in {table_name} erfolgreich aktualisiert.")
            self.current_id = None
            self.on_view_select(None)
        except Exception as e:
            self.view.display_message(f"Update-Fehler: {e}")
            raise e

    def on_input_form_delete(self):
        if not hasattr(self, 'current_id') or self.current_id is None:
            self.view.display_message("Nichts ausgewählt!")
            return

        table_name = self.view.ui.dropdown_select_view.currentText()
        obj_type = ObjectType.from_table_name(table_name)
        if not obj_type:
            return

        try:
            obj_class, _, _ = self.db_map[obj_type]
            id_attr_name = getattr(IDPrefix, obj_type.prefix).value

            full_data = self._collect_form_data()
            full_data[id_attr_name] = self.current_id

            sig = inspect.signature(obj_class.__init__)
            if 'business_id' in sig.parameters and 'business_id' not in full_data:
                full_data['business_id'] = self.business_id

            obj_to_delete = obj_class(**full_data)
            status = delete.delete(obj_to_delete)

            if status == 0:
                self.view.display_message(f"Eintrag {self.current_id} gelöscht.")
                self.current_id = None
                # UI Refresh
                self.on_view_select(None)

        except Exception as e:
            self.view.display_message(f"Lösch-Fehler: {e}")
            raise e

    def on_table_select(self, index):
        table_name = self.view.ui.dropdown_select_view.currentText()
        obj_type = ObjectType.from_table_name(table_name)

        if not obj_type:
            return

        id_attr_name = getattr(IDPrefix, obj_type.prefix).value
        obj_class, _, _ = self.db_map[obj_type]

        row = index.row()
        selected_item = self.table_model._data[row]
        self.current_id = getattr(selected_item, id_attr_name)
        try:
            obj_type = ObjectType.from_table_name(table_name)
            id_attr_name = getattr(IDPrefix, obj_type.prefix).value
            self.current_id = getattr(selected_item, id_attr_name)

            self.sidebar_input_master_ui.btn_insert_update.setText("Aktualisieren")
            self.view.display_message(f"Bearbeite {table_name} ID: {self.current_id}")

            for attr_name, value in vars(selected_item).items():
                widget = self._find_widget_by_attribute(attr_name)
                if widget:
                    self._write_to_widget(widget, value)

        except Exception as e:
            self.view.display_message(f"Fehler bei der Auswahl: {e}")

    def _find_widget_by_attribute(self, attr_name):
        for prefix in ["db_", "cb_"]:
            target_name = "{}{}".format(prefix, attr_name)
            for form in [self.active_form, self.base_form]:
                if form and hasattr(form, target_name):
                    return getattr(form, target_name)
        return None

    def _collect_form_data(self):
        data = {}
        for form in [self.base_form, self.active_form]:
            if not form:
                continue

            for attr_name in dir(form):
                if attr_name.startswith(("cb_", "db_")):
                    widget = getattr(form, attr_name)

                    field_name = attr_name[3:]
                    data[field_name] = self._read_from_widget(widget)

        return data

    @staticmethod
    def _write_to_widget(widget, value):
        if isinstance(widget, QLineEdit):
            widget.setText(str(value) if value is not None else "")

        elif isinstance(widget, QComboBox):
            idx = widget.findData(value)
            widget.setCurrentIndex(idx)

        elif isinstance(widget, QDateEdit) and value:
            if isinstance(value, str):
                q_date = QDate.fromString(value, "yyyy-MM-dd")
                if q_date.isValid():
                    widget.setDate(q_date)
                else:
                    print(f"WARNUNG: Ungültiges Datumsformat in DB: {value}")
            else:
                widget.setDate(QDate(value.year, value.month, value.day))

        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            pass

    @staticmethod
    def _read_from_widget(widget):
        if isinstance(widget, QLineEdit):
            return widget.text()
        elif isinstance(widget, QComboBox):
            return widget.currentData()
        elif isinstance(widget, QDateEdit):
            return widget.date().toPyDate().isoformat()
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            return widget.value()
        return None

    @staticmethod
    def assemble_form(container_widget, ui_class):
        ui_instance = ui_class()

        if container_widget.layout():
            QWidget().setLayout(container_widget.layout())

        ui_instance.setupUi(container_widget)
        return ui_instance

    def _populate_dropdowns(self, combobox, type_enum, id_enum):
        if combobox is None:
            print(f"no cb, returning. {type}")
            return

        combobox.clear()
        datalist = read.readFiltered(type_enum.table_name, self.business_id)
        #print(f"DEBUG: Suche Daten für {type_enum}, gefunden: {len(datalist)} Einträge")

        for item in datalist:
            item_id = getattr(item, id_enum)

            if hasattr(item, 'name'):
                display_name = item.name
            elif hasattr(item, 'plot_nr'):
                display_name = f"Schlag {item.plot_nr} (FLIK: {item.flik})"
            elif hasattr(item, 'suffix'):
                display_name = f"Teilschlag {item.suffix}"
            else:
                display_name = "{} ID: {}".format(item.__class__.__name__, item_id)

            combobox.addItem(display_name, item_id)

    def refresh_form(self, type_name):
        self.base_form = None
        self.active_form = None

        sidebar_area = self.view.ui.container_widget_sidebar
        if sidebar_area.layout():
            while sidebar_area.layout().count():
                item = sidebar_area.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        self.current_form_widget = QWidget()
        self.sidebar_input_master_ui = self.assemble_form(self.current_form_widget, Ui_input_form_sidebar)

        match type_name:
            case "plots":
                self.active_form = self.assemble_form(self.sidebar_input_master_ui.container_widget_input_form, Ui_form_plot)

            case "subplots":
                self.active_form = self.assemble_form(self.sidebar_input_master_ui.container_widget_input_form, Ui_form_subplot)
                self._populate_dropdowns(self.active_form.cb_plot_id, ObjectType.PLOT, IDPrefix.PLOT.value)

            case "crops":
                self.active_form = self.assemble_form(self.sidebar_input_master_ui.container_widget_input_form, Ui_form_crop)

            case "cultures":
                self.active_form = self.assemble_form(self.sidebar_input_master_ui.container_widget_input_form, Ui_form_culture)

                self._populate_dropdowns(self.active_form.cb_subplot_id, ObjectType.SUBPLOT, IDPrefix.SUBPLOT.value)
                self._populate_dropdowns(self.active_form.cb_crop_id, ObjectType.CROP, IDPrefix.CROP.value)

            case "fertilizers":
                self.base_form = self.assemble_form(self.sidebar_input_master_ui.container_widget_input_form, Ui_form_agrochemicals)
                self.active_form = self.assemble_form(self.base_form.subform_widget, Ui_form_fertilizer)

                for type_ in FertilizerType:
                    self.active_form.cb_type.addItem(type_.value, type_.name)

            case "pesticides":
                self.base_form = self.assemble_form(self.sidebar_input_master_ui.container_widget_input_form, Ui_form_agrochemicals)
                self.active_form = self.assemble_form(self.base_form.subform_widget, Ui_form_pesticide)

                for type_ in PesticideType:
                    self.active_form.cb_type.addItem(type_.value, type_.name)

            case "tillage":
                self.base_form = self.assemble_form(self.sidebar_input_master_ui.container_widget_input_form, Ui_form_action)
                self.active_form = self.assemble_form(self.base_form.subform_widget, Ui_form_tillage)

                self._populate_dropdowns(self.base_form.cb_subplot_id, ObjectType.SUBPLOT, IDPrefix.SUBPLOT.value)

                for type_ in TillageType:
                    self.active_form.cb_type.addItem(type_.value, type_.name)

            case "sowing":
                self.base_form = self.assemble_form(self.sidebar_input_master_ui.container_widget_input_form, Ui_form_action)
                self.active_form = self.assemble_form(self.base_form.subform_widget, Ui_form_sowing)

                self._populate_dropdowns(self.base_form.cb_subplot_id, ObjectType.SUBPLOT, IDPrefix.SUBPLOT.value)

            case "fertilizer_applications":
                self.base_form = self.assemble_form(self.sidebar_input_master_ui.container_widget_input_form, Ui_form_action)
                self.active_form = self.assemble_form(self.base_form.subform_widget, Ui_form_fertilizer_application)

                self._populate_dropdowns(self.base_form.cb_subplot_id, ObjectType.SUBPLOT, IDPrefix.SUBPLOT.value)
                self._populate_dropdowns(self.active_form.cb_chemical_id, ObjectType.FERTILIZER, IDPrefix.CHEMICAL.value)

            case "pesticide_applications":
                self.base_form = self.assemble_form(self.sidebar_input_master_ui.container_widget_input_form, Ui_form_action)
                self.active_form = self.assemble_form(self.base_form.subform_widget, Ui_form_pesticide_application)

                self._populate_dropdowns(self.base_form.cb_subplot_id, ObjectType.SUBPLOT, IDPrefix.SUBPLOT.value)
                self._populate_dropdowns(self.active_form.cb_chemical_id, ObjectType.PESTICIDE, IDPrefix.CHEMICAL.value)

            case "harvests":
                self.base_form = self.assemble_form(self.sidebar_input_master_ui.container_widget_input_form, Ui_form_action)
                self.active_form = self.assemble_form(self.base_form.subform_widget, Ui_form_harvest)

                self._populate_dropdowns(self.base_form.cb_subplot_id, ObjectType.SUBPLOT, IDPrefix.SUBPLOT.value)

            case _:
                self.view.display_message("Not yet implemented")

        sidebar_area = self.view.ui.container_widget_sidebar
        sidebar_layout = sidebar_area.layout()

        if sidebar_layout is None:
            from PyQt5.QtWidgets import QVBoxLayout
            sidebar_layout = QVBoxLayout(sidebar_area)
            sidebar_layout.setContentsMargins(0, 0, 0, 0)
            sidebar_area.setLayout(sidebar_layout)

        self.current_id = None
        sidebar_layout.addWidget(self.current_form_widget)

        # Connecting Slots and Signals
        self.sidebar_input_master_ui.btn_insert_update.clicked.connect(self.on_input_form_update_save)
        self.sidebar_input_master_ui.btn_delete.clicked.connect(self.on_input_form_delete)



