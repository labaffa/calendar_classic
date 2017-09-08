from __future__ import division
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
    index = linear_index
    columns = matrix_columns
    return int(index/columns)


def get_column(linear_index, matrix_columns):
    """
    From a matrix of given columns return the column index
    corresponding to a given linear index
    """
    index = linear_index
    columns = matrix_columns
    return int(index - int((index/columns))*columns)


def proportion_to_screen_size(master, width_parts, height_parts):
    """
    Given 'w' and 'h' integers and the width, height of the screen ->
    -> tuple((1/w)*screen_width, (1/h)*screen_height)
    """
    # Get screen size
    master.update_idletasks()
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    # Calculate proportioned size
    proportioned_width = int((1/width_parts)*screen_width)
    proportioned_height = int((1/height_parts)*screen_height)
    proportioned_size = (proportioned_width, proportioned_height)
    return proportioned_size


def pixel_size_string_format(pixels_width, pixels_height):
    """(width, height) -> str('width'x'height')"""
    pixels_string = str(pixels_width) + 'x' + str(pixels_height)
    return pixels_string


def proportion_to_screen_string(master, width_parts, height_parts):
    """Same of proportion_to_screen_size() but return a 'w x h' string"""
    width, height = proportion_to_screen_size(master,
                                              width_parts, height_parts)
    size_string = pixel_size_string_format(width, height)
    return size_string
