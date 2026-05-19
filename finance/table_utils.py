from PySide6.QtCore import Qt


def fit_table_height_to_rows(table, min_rows=0, max_rows=14):
    table.resizeRowsToContents()

    row_count    = table.rowCount()
    visible_rows = max(min_rows, min(row_count, max_rows))
    default_row_height = table.verticalHeader().defaultSectionSize()

    row_height = 0
    for row in range(visible_rows):
        if row < row_count:
            row_height += table.rowHeight(row)
        else:
            row_height += default_row_height

    header_height = table.horizontalHeader().height()
    frame_height  = table.frameWidth() * 2
    padding       = 2
    table_height  = header_height + row_height + frame_height + padding

    table.setMinimumHeight(table_height)
    table.setMaximumHeight(table_height)

    if row_count > max_rows:
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    else:
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
