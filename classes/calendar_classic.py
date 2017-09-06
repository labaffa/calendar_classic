import calendar
from datetime import date, timedelta
from settings.config import (calendar_button_conf, header_conf,
                             this_month_conf, other_month_conf,
                             today_conf, weekdays_conf, month_year_conf,
                             table_conf, date_box_conf,
                             weekday_labels_conf)
from utils.checkers import (is_today, get_row, get_column,
                            proportion_to_screen_string,
                            proportion_to_screen_size)
try:
    import Tkinter as tk
    import tkFont
except ImportError: # python 3
    import tkinter as tk
    import tkinter.font as tkFont


class Left_arrow(tk.Label):
    """A tk.Label showing a left arrow to click on"""
    def __init__(self, master=None, **kw):
        self.action = kw.pop('action', self.default_action)
        kw['text'] = '<'
        tk.Label.__init__(self, master, **kw)
        self.bind('<Button-1>', self.callback)
        self.configure(calendar_button_conf)

    def callback(self, event):
        self.action()

    def default_action(self):
        """Action performed if 'action' attribute was not inserted"""
        print('Pass a function to this object to execute it')


class Right_arrow(tk.Label):
    """A tk.Label showing a right arrow to click on"""
    def __init__(self, master=None, **kw):
        self.action = kw.pop('action', self.default_action)
        kw['text'] = '>'
        tk.Label.__init__(self, master, **kw)
        self.bind('<Button-1>', self.callback)
        self.configure(calendar_button_conf)

    def callback(self, event):
        self.action()

    def default_action(self):
        print('Pass a function to this object to execute it')


class Month_and_year(tk.Label):
    """A tk.Label showing selected month and year"""
    def __init__(self, master=None, **kw):
        self.calendar = kw.pop('calendar', calendar.LocaleTextCalendar())
        # Set first day of the first-displayed month (def: today-month)
        self.reference_date = kw.pop('day', date.today())
        self.first_of_month = date(self.reference_date.year,
                                   self.reference_date.month, 1)
        # Year and month to visualize
        year, month = self.first_of_month.year, self.first_of_month.month
        # Fill and configure label
        header = self.calendar.formatmonthname(year, month, 0)
        kw['text'] = header.title()
        tk.Label.__init__(self, master, **kw)
        self.configure(month_year_conf)

    def update(self):
        year, month = self.first_of_month.year, self.first_of_month.month
        header = self.calendar.formatmonthname(year, month, 0)
        self.configure(text=header.title())


class Header(tk.Frame):
    """A tk.Frame with month, year and left, right buttons"""
    def __init__(self, master=None, **kw):
        self.calendar = kw.pop('calendar', calendar.LocaleTextCalendar())
        # Set first day of the first-displayed month (def: today-month)
        self.reference_date = kw.pop('day', date.today())
        self.first_of_month = date(self.reference_date.year,
                                   self.reference_date.month, 1)
        tk.Frame.__init__(self, master, **kw)
        # Create Header widgets
        self.left_button = Left_arrow(self)
        self.right_button = Right_arrow(self)
        self.header = Month_and_year(self,
                                     day=self.first_of_month,
                                     calendar=self.calendar)
        self.set_configure()
        self.build()

    def set_configure(self):
        """Configuration of inserted widgets"""
        self.configure(header_conf)
        self.left_button.configure(calendar_button_conf)
        self.right_button.configure(calendar_button_conf)
        self.header.configure(month_year_conf)

    def set_month_year_width(self):
        """Set Month_year width by the longest month-string"""
        # Frame and label to use as width testers
        frame = tk.Frame(self)
        label = tk.Label(frame)
        # Simulate appearence of the displayed month_year (important)
        label.configure(month_year_conf)
        label.grid(row=0)
        max_width = 0
        # Find the longest 'year and month' in the given locale
        for month in range(1, 13):
            # Different months
            header = self.calendar.formatmonthname(2000, month, 0)
            label.configure(text=header.title())
            # Retrieve widget width info
            label.update_idletasks()  # dont know why but it's crucial
            width = label.winfo_width()
            if width > max_width:
                max_width = width
        return max_width

    def build(self):
        # Fixed Month_year dimension
        month_year_width = self.set_month_year_width()
        # Dimensions of widgets
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, minsize=month_year_width, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.header.propagate(False)
        # Position of widgets
        self.left_button.grid(row=0, column=0, sticky='e')
        self.header.grid(row=0, column=1, sticky='news')
        self.right_button.grid(row=0, column=2, sticky='w')

    def update(self):
        self.header.first_of_month = self.first_of_month
        self.header.update()


class Weekday_names(tk.Frame):
    """A tk.Frame to display weekday names"""
    def __init__(self, master=None, **kw):
        self.calendar = kw.pop('calendar', calendar.LocaleTextCalendar())
        tk.Frame.__init__(self, master, **kw)
        # General frame config and build
        self.configure(weekdays_conf)
        self.build()

    def build(self):
        """Create, set size and place labels with weekday names in them"""
        weekdays = self.calendar.formatweekheader(3).split()
        # Loop over the seven weekdays
        for col, weekday in enumerate(weekdays):
            # Create and configure the label
            weekday_label = tk.Label(self, text=weekday)
            weekday_label.configure(weekday_labels_conf, anchor='center')
            # A column for every weekday
            weekday_label.grid(row=0, column=col, sticky='news')
            # Strechable, same-sized labels
            self.columnconfigure(col, weight=1)
            self.rowconfigure(0, weight=1)


class Dates_table(tk.Frame):
    """A matrix of tk.Labels displaying days of selected month"""
    def __init__(self, master=None, **kw):
        self.calendar = kw.pop('calendar', calendar.LocaleTextCalendar())
        # Set first day of the first-displayed month (def: today-month)
        self.reference_date = kw.pop('day', date.today())
        self.first_of_month = date(self.reference_date.year,
                                   self.reference_date.month, 1)
        tk.Frame.__init__(self, master, **kw)
        # Number of rows and columns of the table
        self.no_rows = 6
        self.no_cols = 7
        # Create boxes to fill with day numbers
        self.date_boxes = [tk.Label(self)
                           for _ in range(self.no_rows*self.no_cols)]
        # General frame configuration and display
        self.configure(table_conf)
        self.first_display()

    def this_month_date(self, date):
        """Return True if date.month is equal to the displayed one"""
        if date.month == self.first_of_month.month:
            return True
        return False

    def label_config(self, label, label_date):
        """Set the style of the label based on its associated date"""
        # Can be a day of the displayed month...
        if self.this_month_date(label_date):
            # (in particular today)
            if is_today(label_date):
                label.configure(today_conf)
                return
            label.configure(this_month_conf)
            return
        # ...or a day of the previous or next months of the displayed
        label.configure(other_month_conf)
        return

    def first_display(self):
        """Display month dates when a Dates_table instance is created"""
        # Define variables
        year = self.first_of_month.year
        month = self.first_of_month.month
        weekday_of_first, no_of_days = calendar.monthrange(year, month)
        # Fill boxes with day numbers and grid in 'self'
        for i, date_box in enumerate(self.date_boxes):
            # Shift: number of days from the first day of the month.
            # It is used to fill from the first day of the
            # week of the first month-day.
            shift = i - weekday_of_first
            current_date = self.first_of_month + timedelta(shift)
            # Assign number and style of the box
            date_box.configure(date_box_conf,
                               anchor='ne',
                               text=current_date.day)
            self.label_config(date_box, current_date)
            # Grid the box in the right row, column
            box_row = get_row(i, self.no_cols)
            box_column = get_column(i, self.no_cols)
            date_box.grid(row=box_row,
                          column=box_column,
                          sticky='news')
        # Equal space for each box
        for row in range(self.no_rows):
            self.rowconfigure(row, weight=1)
        for col in range(self.no_cols):
            self.columnconfigure(col, weight=1)

    def update(self):
        """Same of first_display but without placing labels"""
        # Define variables
        year = self.first_of_month.year
        month = self.first_of_month.month
        weekday_of_first, no_of_days = calendar.monthrange(year, month)
        # Overwrite dates and box colors
        for i, date_box in enumerate(self.date_boxes):
            shift = i - weekday_of_first
            current_date = self.first_of_month + timedelta(shift)
            date_box.configure(text=current_date.day)
            self.label_config(date_box, current_date)


class Calendar_classic(tk.Frame):
    """A classic calendar with arrows to change displayed month"""
    def __init__(self, master=None, **kw):
        self.calendar = kw.pop('calendar', calendar.LocaleTextCalendar())
        # Set first day of the first-displayed month (def: today-month)
        self.reference_date = kw.pop('day', date.today())
        self.first_of_month = date(self.reference_date.year,
                                   self.reference_date.month, 1)
        tk.Frame.__init__(self, master, **kw)
        # Create Calendar_classic widgets
        self.header = Header(self,
                             calendar=self.calendar,
                             day=self.first_of_month)
        self.weekdays = Weekday_names(self, calendar=self.calendar)
        self.table = Dates_table(self,
                                 calendar=self.calendar,
                                 day=self.first_of_month)
        # Build and bind action to buttons
        self.build()
        self.bind_widgets()

    def build(self):
        """Grid and set dimensions of widgets"""
        # Place widgets
        self.header.grid(row=0, column=0, sticky='news')
        self.weekdays.grid(row=1, column=0, sticky='news')
        self.table.grid(row=2, column=0, sticky='news')
        # Set dimension and behavior of children
        self.rowconfigure(0, weight=1)  # Strechable
        self.rowconfigure(1, weight=0)  # Fixed size
        self.rowconfigure(2, weight=5)  # Strechable and 5 times Header
        self.columnconfigure(0, weight=1)

    def update(self):
        """Update month, year and visualized dates"""
        self.header.update()
        self.table.update()

    def prev_month(self):
        """Set first_of_month of all widgets to the previous month's"""
        # Calculate date object of first day of the previous month
        self.last_of_previous = self.first_of_month - timedelta(1)
        self.first_of_month = date(self.last_of_previous.year,
                                   self.last_of_previous.month, 1)
        print(self.first_of_month)
        # Update first_of_month of children
        self.header.first_of_month = self.first_of_month
        self.table.first_of_month = self.first_of_month
        # Update displayed stuff
        self.update()

    def next_month(self):
        """Set first_of_month of all widgets to the next month's"""
        # Define variables
        year, month = self.first_of_month.year, self.first_of_month.month
        days_in_month = calendar.monthrange(year, month)[1]
        # Date object of the first day of the next month
        self.first_of_next = (self.first_of_month +
                              timedelta(days_in_month))
        self.first_of_month = self.first_of_next
        # Update first_of_month of children
        self.header.first_of_month = self.first_of_month
        self.table.first_of_month = self.first_of_month
        # Update displayed stuff
        self.update()

    def bind_widgets(self):
        """Bind commands to the widgets"""
        self.header.left_button.action = self.prev_month
        self.header.right_button.action = self.next_month


class Home_screen(tk.Tk):
    """The Home screen of the app"""
    def __init__(self, **kw):
        tk.Tk.__init__(self, **kw)
        # Place Calendar_classic in window
        screen = Calendar_classic(self)
        screen.grid(row=0, column=0, sticky='news')
        # Make the calendar strechable
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Set dimensions
        self.default_size()
        self.minimum_size()

    def default_size(self, w=3, h=2):
        """
        Set size of the window at launch proportioned to screen's size.
        w, h = 1,1 to launch in fullscreen mode
        """
        default_size = proportion_to_screen_string(self, w, h)
        self.geometry(default_size)

    def minimum_size(self, w=5, h=3):
        """
        Set minimum size of the window proportioned to screen's size
        """
        min_width, min_height = proportion_to_screen_size(self, w, h)
        self.minsize(min_width, min_height)
