from PySide6.QtCore import Qt


def fit_table_height_to_rows(table, min_rows=0, max_rows=14):
    """
    Resize the table so it shows exactly its rows with no blank space,
    and the rounded border-radius looks correct on all four corners.
    """
    table.resizeRowsToContents()

    row_count    = table.rowCount()
    visible_rows = max(min_rows, min(row_count, max_rows))

    row_height = 0
    for i in range(visible_rows):
        if i < row_count:
            row_height += table.rowHeight(i)
        else:
            row_height += table.verticalHeader().defaultSectionSize()

    header_h = table.horizontalHeader().height()
    total_h  = header_h + row_height + 2   # +2 for frame border pixels

    table.setMinimumHeight(total_h)
    table.setMaximumHeight(total_h)

    if row_count > max_rows:
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    else:
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


def apply_table_style(table):
    """
    Call after populating a table to ensure last row has no bottom border
    so it doesn't fight the rounded bottom corners.
    """
    row_count = table.rowCount()
    if row_count == 0:
        return
    last_row = row_count - 1
    for col in range(table.columnCount()):
        item = table.item(last_row, col)
        if item:
            # Mark last row so CSS :last child works
            item.setData(Qt.UserRole, "last")
