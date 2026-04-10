import csv
from model.db.read import get_plot_report


def export_plot_report_to_csv(plot_id, business_id, filename):
    data = get_plot_report(plot_id, business_id)

    if not data:
        return False
    keys = data[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys, delimiter=';')
        writer.writeheader()
        writer.writerows(data)

    return True