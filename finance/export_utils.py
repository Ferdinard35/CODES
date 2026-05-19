import csv
from datetime import datetime
import database


def export_transactions_to_csv():

    data = database.get_all_transactions_for_export()
    filename = f"finance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Description", "Amount (GHS)", "Type"])

        for row in data:
            date        = row[0]
            category    = row[1]
            description = row[2]
            amount      = (row[3] if row[3] is not None else 0) / 100
            trans_type  = row[4]

            writer.writerow([date, category, description, f"{amount:,.2f}", trans_type])

    return filename
