# Font used in calendar_classic
header_font = ('Helvetica', '13', 'bold')
dates_font = ('Helvetica', '10')
weekday_labels_font = ('Helvetica', '10')
# Buttons
calendar_button_conf = {'bg': '#DEE1DB',
                        'highlightthickness': 1,
                        'highlightbackground': '#E6D6E5',
                        'font': header_font}
# Label showing month and year displayed
month_year_conf = {'bg': '#DEE1DB',
                   'font': header_font,
                   'padx': 25}
# Frame containing buttons and month_year
header_conf = {'bg': '#DEE1DB',
               'padx': 7,
               'pady': 7}
# Weekday frame
weekdays_conf = {'bg': '#DEE1DB',
                 'padx': 7,
                 'pady': 7}
# Labels showing weekday names
weekday_labels_conf = {'bg': '#DEE1DB',
                       'font': weekday_labels_font}
# Frame containing table of data boxes
table_conf = {'bg': 'white',
              'highlightthickness': 3,
              'highlightbackground': '#F8EFF7'}
# Date boxes common configuration
date_box_conf = {'highlightbackground': '#F8EFF7',
                 'highlightthickness': 1,
                 'padx': 5,
                 'pady': 5,
                 'font': dates_font}
# Date box specific configurations
today_conf = {'fg': 'black', 'bg': '#F8EFF7'}
this_month_conf = {'fg': 'black',
                   'bg': table_conf['bg']}
other_month_conf = {'fg': '#D3D7CF',
                    'bg': table_conf['bg']}
