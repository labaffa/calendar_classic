from datetime import date


def is_today(test_date):
    """Return True if a given date is today"""
    if test_date == date.today():
        return True
    return False


def get_row(linear_index, matrix_columns):
    """
    From a matrix of given columns return the row index
    corresponding to a given linear index
    """
    index = int(linear_index)
    columns = int(matrix_columns)
    return index/columns


def get_column(linear_index, matrix_columns):
    """
    From a matrix of given columns return the column index
    corresponding to a given linear index
    """
    index = int(linear_index)
    columns = int(matrix_columns)
    return index - (index/columns)*columns
