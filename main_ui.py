try:
    import PySimpleGUI as sg
    import datetime  # Added datetime module for timestamp
    from dataclasses import dataclass, field 
except Exception as e:
    print (f'Exception occured {str(e)}')


# Function to validate if a string can be converted to an integer
def integer(value):
    try:
        rounded_qty = round(float(value))
        return rounded_qty
    except ValueError:
        return None

# Function to validate if a string can be converted to a number with 2 decimal places
def number_with_2_decimal_places(value):
    try:
        num = float(value)
        return round(num, 2)
    except ValueError:
        return None

@dataclass
class Level:
    text:str
    key:str
    msg:str
    value:float=None
    cmp_event:str = field(init=False)
    cmp_focus:str = field(init=False)
    focus_in: str = field(init=False)
    focus_out: str = field(init=False)

    def __post_init__(self):
        self.cmp_event = f'{self.key}_Enter'
        self.focus_in = f"{self.key}-FOCUS_IN"
        self.focus_out = f"{self.key}-FOCUS_OUT"

def main ():
    # Define the layout of your GUI
    ul_option = 'NIFTY-I'
    n_posn = 'INTRADAY'
    n_exp_date = ''
    n_alert = None
    n_b_entry = None
    n_s_entry = None

    al = Level (text='Alert Level:', key='-NIFTY-ALERT-LEVEL-',msg='Nifty Alert Level')

    layout = [
        [sg.TabGroup([
            [sg.Tab('NIFTY', [
                # Section 1: Configuration
                [sg.Text('Configuration', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE, size=(80,1))],
                [sg.Text('Instrument (for Level):', size=20),  sg.Text('Mode:', size=20, justification='left'), sg.Text('Option Expiry:', size=40, justification='left')],
                [sg.Combo(['NIFTY-I', 'NIFTY_INDEX'], key='-NIFTY-UNDERLYING-OPTION-', default_value = ul_option, enable_events=True, size=(20, 1)), sg.Combo(['INTRADAY', 'OVERNIGHT'], key='-NIFTY-INTRA-OVERNIGHT-', default_value=n_posn, enable_events=True, size=(20, 1)), sg.CalendarButton('Pick a Date', target='-NIFTY-EXPIRY-DATE-', format='%d/%m/%Y', pad=(10, 10)), sg.InputText('', key='-NIFTY-EXPIRY-DATE-', size=(20, 1), enable_events=True), sg.Text('Or', size=3), sg.Combo(['WEEK-I', 'WEEK-II', 'MONTH-I'], key='-NIFTY-EXPIRY-OPTION-', default_value='WEEK-I', enable_events=True, size=(20, 1))],
                [sg.Text('Moneyness (Ix Based):', size=20), sg.Text('~ Premium:',size=20), sg.Text('Select Broker:',size=20), sg.Text('Target Ratios:', size=20)],
                [sg.Combo(['ATM-5', 'ATM-4', 'ATM-3', 'ATM-2', 'ATM-1', 'ATM', 'ATM+1', 'ATM+2', 'ATM+3', 'ATM+4', 'ATM+5'], key='-NIFTY-MONEYNESS-', default_value='ATM', size=(20, 1), enable_events=True),
                sg.InputText('', key='-NIFTY-PREMIUM-',size=(20,1)),
                sg.Combo(['FINVASIA', 'ZERODHA'], key='-NIFTY-BROKER-OPTION-', default_value='FINVASIA', enable_events=True, size=(25, 1)), sg.Combo(['0:0:3', '0:3:0','3:0:0', '1:1:1', '1:2:0', '2:1:0', '0:1:2', '0:2:1'], key='-NIFTY-TARGET_RATIO-', default_value='1:1:1', enable_events=True, size=(10, 1)),
                sg.Text('Trade Mode'), sg.Combo(['Live', 'Paper'], key='-TRADE-LIVE-PAPER-', default_value='Live', enable_events=True, size=(5, 1)),
                ],
                
                # Section 2: Entry / Target / SL Levels
                [sg.Text('Levels', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE, size=(80,1))],
                [sg.Text('Alert Level', size=15), sg.Text('B Entry @:',size=12), sg.Text('S Entry @:',size=15)], 
                [sg.InputText('', key='-NIFTY-ALERT-LEVEL-',size=15), sg.InputText('', key='-NIFTY-BUY-LEVEL-', size=15), sg.InputText('', key='-NIFTY-SHORT-LEVEL-', size=15)],

                [sg.Text('B T1 Level:', justification="left"), sg.Text('B T2 Level:', justification="left"), sg.Text('B T3 Level:',justification="left"), sg.Text('B SL Level:'), sg.Text('', size=2), sg.Text('SL@Cost:'), sg.Text('Or', size=2), sg.Text('SL@Cost after :')], 
                [sg.InputText('', key='-NIFTY-LONG-T1-LEVEL-',size=9), sg.InputText('', key='-NIFTY-LONG-T2-LEVEL-',size=9), sg.InputText('', key='-NIFTY-LONG-T3-LEVEL-',size=9), sg.InputText('', key='-NIFTY-LONG-SL-LEVEL-',size=9), sg.Text('', size=2), sg.InputText('', key='-NIFTY-SL-AT-COST-LEVEL-',size=9), sg.Text('', size=2), sg.InputText('', key='-NIFTY-SL-AT-COST-AFTER-MINS-',size=9), sg.Text('Mins')],

                [sg.Text('S T1 Level:', justification="left"), sg.Text('S T2 Level:', justification="left"), sg.Text('S T3 Level:',justification="left"), sg.Text('S SL Level:'), sg.Text('', size=2), sg.Text('Trail After Level:'), sg.Text('', size=2), sg.Text('Trail By Pts:')], 
                [sg.InputText('', key='-NIFTY-SHORT-T1-LEVEL-',size=9), sg.InputText('', key='-NIFTY-SHORT-T2-LEVEL-',size=9),sg.InputText('', key='-NIFTY-SHORT-T3-LEVEL-',size=9), sg.InputText('', key='-NIFTY-SHORT-SL-LEVEL-',size=9), sg.Text('', size=2), sg.InputText('', key='-NIFTY-TRAIL-AFTER-LEVEL-',size=15), sg.Text('', size=2), sg.InputText('', key='-NIFTY-TRAIL-BY-PTS-',size=12)],

                # Section 3: Trading Info
                [sg.Text('Position Sizing', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE, size=(80,1))],
                [sg.Text('Qty(in Lots):',size=20), sg.Text('Or', size=3), sg.Text('Qty Amount:', size=20)],
                [sg.InputText('', key='-NIFTY-QTY-LOTS-', size=20), sg.Text('', size=3), sg.InputText('', key='-NIFTY-QTY-AMOUNT-',size=20)],
                [sg.Text('', size=(80, 1))],
                [sg.Button('NIFTY CE BUY  \u2191', button_color=('white', 'green'), size=(30,2), key='-NIFTY-CE-BUY-'),  sg.Text('',size=10), sg.Button('NIFTY CE SELL \u2193', button_color=('white', 'red'),size=(30,2),key='-NIFTY-CE-SELL-')],  # CE buttons with up and down arrows
                [sg.Text('', size=(80, 1))],
                [sg.Button('NIFTY PE SELL \u2193', button_color=('white', 'green'), size=(30,2), key='-NIFTY-PE-SELL-'),  sg.Text('',size=10), sg.Button('NIFTY PE BUY  \u2191', button_color=('white', 'red'),size=(30,2), key='-NIFTY-PE-SELL-') ],  # PE buttons with up and down arrows
                [sg.Text('', size=(80, 1))]
                ])
            ],
            [sg.Tab('Bank Nifty', [

                # Section 1: Configuration
                [sg.Text('Configuration', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE, size=(80,1))],
                [sg.Text('Instrument (for Level):', size=20),  sg.Text('Mode:', size=20, justification='left'), sg.Text('Option Expiry:', size=40, justification='left')],
                [sg.Combo(['BANKNIFTY-I', 'BANKNIFTY_INDEX'], key='-BANKNIFTY-OPTION-', default_value='BANKNIFTY-I', enable_events=True, size=(20, 1)), sg.Combo(['MIS', 'NRML'], key='-BANKNIFTY-MODE-', default_value='MIS', enable_events=True, size=(20, 1)), sg.CalendarButton('Pick a Date', target='-BANKNIFTY-DATE-', format='%d/%m/%Y', pad=(10, 10)), sg.InputText('', key='-BANKNIFTY-DATE-', size=(20, 1), enable_events=True), sg.Text('Or', size=3), sg.Combo(['WEEK-I', 'WEEK-II', 'MONTH-I'], key='-EXPIRY-OPTION-', default_value='WEEK-I', enable_events=True, size=(20, 1))],
                [sg.Text('Moneyness (Ix Based):', size=20), sg.Text('~ Premium:',size=20), sg.Text('Select Broker:',size=20), sg.Text('Target Ratios:', size=20)],
                [sg.Combo(['ATM-5', 'ATM-4', 'ATM-3', 'ATM-2', 'ATM-1', 'ATM', 'ATM+1', 'ATM+2', 'ATM+3', 'ATM+4', 'ATM+5'], key='-BANKNIFTY-ATM-', default_value='ATM', size=(20, 1), enable_events=True),
                sg.InputText('', key='-BANKNIFTY-PREMIUM-',size=(20,1)),
                sg.Combo(['FINVASIA', 'ZERODHA'], key='-BROKER-OPTION-', default_value='FINVASIA', enable_events=True, size=(25, 1)), sg.Combo(['0:0:3', '0:3:0','3:0:0', '1:1:1', '1:2:0', '2:1:0', '0:1:2', '0:2:1'], key='-BANKNIFTY-TARGET_RATIO-', default_value='1:1:1', enable_events=True, size=(10, 1)),
                sg.Text('Trade Mode'), sg.Combo(['Live', 'Paper'], key='-TRADE-LIVE-PAPER-', default_value='Live', enable_events=True, size=(5, 1)),
                ],
                
                # Section 2: Entry / Target / SL Levels
                [sg.Text('Levels', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE, size=(80,1))],

                [sg.Text('B Entry @:',size=12), sg.Text('S Entry @:',size=15), sg.Text('Alert Level:', size=15)], 
                [sg.InputText('', key='-BANKNIFTY-BUY-LEVEL-', size=15), sg.InputText('', key='-BANKNIFTY-SHORT-LEVEL-', size=15), sg.InputText('', key='-BANKNIFTY-ALERT-LEVEL-',size=15)],

                [sg.Text('B T1 Level:', justification="left"), sg.Text('B T2 Level:', justification="left"), sg.Text('B T3 Level:',justification="left"), sg.Text('B SL Level:'), sg.Text('', size=2), sg.Text('SL@Cost:'), sg.Text('Or', size=2), sg.Text('SL@Cost after :')], 
                [sg.InputText('', key='-BANKNIFTY-LONG-T1-LEVEL-',size=9), sg.InputText('', key='-BANKNIFTY-LONG-T2-LEVEL-',size=9), sg.InputText('', key='-BANKNIFTY-LONG-T3-LEVEL-',size=9), sg.InputText('', key='-BANKNIFTY-LONG-SL-LEVEL-',size=9), sg.Text('', size=2), sg.InputText('', key='-BANKNIFTY-SL-AT-COST-LEVEL-',size=9), sg.Text('', size=2), sg.InputText('', key='-BANKNIFTY-SL-AT-COST-AFTER-MINS-',size=9), sg.Text('Mins')],

                [sg.Text('S T1 Level:', justification="left"), sg.Text('S T2 Level:', justification="left"), sg.Text('S T3 Level:',justification="left"), sg.Text('S SL Level:'), sg.Text('', size=2), sg.Text('Trail After Level:'), sg.Text('', size=2), sg.Text('Trail By Pts:')], 
                [sg.InputText('', key='-BANKNIFTY-SHORT-T1-LEVEL-',size=9), sg.InputText('', key='-BANKNIFTY-SHORT-T2-LEVEL-',size=9),sg.InputText('', key='-BANKNIFTY-SHORT-T3-LEVEL-',size=9), sg.InputText('', key='-BANKNIFTY-SHORT-SL-LEVEL-',size=9), sg.Text('', size=2), sg.InputText('', key='-BANKNIFTY-TRAIL-AFTER-LEVEL-',size=9), sg.Text('', size=2), sg.InputText('', key='-BANKNIFTY-TRAIL-BY-PTS-',size=9)],

                # Section 3: Trading Info
                [sg.Text('Position Sizing', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE, size=(80,1))],
                [sg.Text('Qty(in Lots):',size=20), sg.Text('Or', size=3), sg.Text('Qty Amount:', size=20)],
                [sg.InputText('', key='-BANKNIFTY-QTY-LOTS-', size=20), sg.Text('', size=3), sg.InputText('', key='-BANKNIFTY-QTY-AMOUNT',size=20)],
                [sg.Text('', size=(80, 1))],
                [sg.Button('BANKNIFTY CE BUY  \u2191', button_color=('white', 'green'), size=(30,2), key='-BANKNIFTY-CE-BUY-'),  sg.Text('',size=10), sg.Button('BANKNIFTY CE SELL \u2193', button_color=('white', 'red'),size=(30,2), key='-BANKNIFTY-CE-SELL-')],  # CE buttons with up and down arrows
                [sg.Text('', size=(80, 1))],
                [sg.Button('BANKNIFTY PE SELL \u2193', button_color=('white', 'green'), size=(30,2), key='-BANKNIFTY-PE-SELL-'),  sg.Text('',size=10), sg.Button('BANKNIFTY PE BUY  \u2191', button_color=('white', 'red'),size=(30,2), key='-BANKNIFTY-PE-BUY-') ],  # PE buttons with up and down arrows
                [sg.Text('', size=(80, 1))]

                ]),
            ],
            [sg.Tab('System Config', [[sg.Text('Session ID Configuration', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE)],
                [sg.Text('Zerodha Session ID:')], 
                [sg.InputText('', key='-ZERODHA-SESSION-ID-')],
                [sg.Text('Finvasia Session ID:')], 
                [sg.InputText('', key='-FINVASIA-SESSION-ID-')],
                [sg.Text('Log Folder Path', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE)],
                [sg.Text('Log File:')], 
                [sg.InputText('', key='-SYSTEM-LOG-FILE-')],
                [sg.Text('Telegram Channel Info', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE)],
                [sg.Text('ID:')], 
                [sg.InputText('', key='-TELEGRAM-CHANNEL-ID-')],
                [sg.Text('Data Feed Info', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE)],
                [sg.Text('Primary DataFeed:')], 
                [sg.InputText('', key='-PRIMARY-DATA-FEED-')],
                [sg.Text('Secondary DataFeed:')], 
                [sg.InputText('', key='-SEC-DATA-FEED-')],
                [sg.Text('No Entry After Time', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE)],
                [sg.Text("(HH:MM:SS):"), sg.InputText(key='-NO-ENTRY-TIME-')],
                [sg.Text('SquareOFF Time', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE)],
                [sg.Text("(HH:MM:SS):"), sg.InputText(key='-SQ-OFF-TIME-')],
                [sg.Text('Max Trades', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE)],
                [sg.Text('Max Nifty Trades:'), sg.InputText('', key='-MAX-NIFTY-TRADES-')], 
                [sg.Text('Max Bank Nifty Trades:'), sg.InputText('', key='-MAX-BANK-NIFTY-TRADES-')], 
                ]),
            ],
            [sg.Tab('Disclaimer', [ ]),]
        ])],

        [sg.Text('', size=(80, 1))],
        [sg.Text('Overall Per Day Max PNL', font=('Helvetica', 14), relief=sg.RELIEF_RIDGE, size=(81,1))],
        [sg.Text('Max Loss:', size=20), sg.Text('Max Profit:', size=20)],
        [sg.InputText('', key='-MAX-LOSS-',size=20), sg.InputText('', key='-MAX-PROFIT-',size=20), sg.Button('Posn Sq Off', button_color=('white', 'grey'), size=(30,2)), sg.Text('Current Posn:', size=10), sg.Text('', size=9), sg.Text('PnL:', size=10), sg.Text('', size=9)],
        [sg.Text('', size=(80, 1))],
        [sg.Text('', size=(80, 1))],
        [sg.Button('App Exit', size=(10, 1))],  # Exit button at the lowest row
        [sg.Text('Logger Window:')],
        [sg.Multiline('', key='-LOGGER-', size=(120, 5))],  # Logger window with a larger size
    ]

    # Create the window
    window = sg.Window('::UI Ver 0.1::', layout, finalize=True)

    window['-NIFTY-PREMIUM-'].bind("<FocusIn>", "_NIFTY-FOCUS_IN_PREMIUM")
    window['-NIFTY-PREMIUM-'].bind("<FocusOut>", "_NIFTY-FOCUS_OUT_PREMIUM")
    window['-NIFTY-PREMIUM-'].bind("<Return>", "_Enter")


    window['-NIFTY-ALERT-LEVEL-'].bind("<FocusIn>", '_NIFTY-FOCUS_IN_ALERT')
    window['-NIFTY-ALERT-LEVEL-'].bind("<FocusOut>", '_NIFTY-FOCUS_OUT_ALERT')
    window['-NIFTY-ALERT-LEVEL-'].bind("<Return>", "_Enter")

    window['-NIFTY-BUY-LEVEL-'].bind("<FocusIn>", "_NIFTY-FOCUS_IN_B-ENTRY")
    window['-NIFTY-BUY-LEVEL-'].bind("<FocusOut>", "_NIFTY-FOCUS_OUT_B-ENTRY")
    window['-NIFTY-BUY-LEVEL-'].bind("<Return>", "_Enter")


    window['-NIFTY-SHORT-LEVEL-'].bind("<FocusIn>", "_NIFTY-FOCUS_IN_S-ENTRY")
    window['-NIFTY-SHORT-LEVEL-'].bind("<FocusOut>", "_NIFTY-FOCUS_OUT_S-ENTRY")
    window['-NIFTY-SHORT-LEVEL-'].bind("<Return>", "_Enter")









    window['-NIFTY-QTY-LOTS-'].bind("<FocusIn>", "_NIFTY-FOCUS_IN_QTY")
    window['-NIFTY-QTY-LOTS-'].bind("<FocusOut>", "_NIFTY-FOCUS_OUT_QTY")
    window['-NIFTY-QTY-LOTS-'].bind("<Return>", "_Enter")

















    window['-MAX-LOSS-'].bind("<Return>", "_Enter")
    window['-MAX-LOSS-'].bind("<FocusOut>", "_NIFTY-FOCUS_MAX_LOSS")

    window['-MAX-PROFIT-'].bind("<Return>", "_Enter")
    window['-MAX-PROFIT-'].bind("<FocusOut>", "_NIFTY-FOCUS_MAX_PROFIT")

    window['-BANKNIFTY-QTY-LOTS-'].bind("<FocusIn>", "_BANKNIFTY-FOCUS_IN_QTY")
    window['-BANKNIFTY-QTY-LOTS-'].bind("<FocusOut>", "_BANKNIFTY-FOCUS_OUT_QTY")
    window['-BANKNIFTY-QTY-LOTS-'].bind("<Return>", "_Enter")


    # Initialize variables to store the previous values of the input fields
    prev_nifty_premium = None
    prev_nifty_qty = None  # Initialize as None
    prev_nifty_max_loss = None  # Initialize as None
    prev_nifty_max_profit = None  # Initialize as None
    prev_banknifty_qty = None  # Initialize as None
    prev_banknifty_max_loss = None  # Initialize as None
    prev_banknifty_max_profit = None  # Initialize as None

    # Function to format a date with the day of the week
    def format_date_with_day(date_str):
        try:
            date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
            formatted_date = date.strftime('%A, %d/%b/%Y')
            return formatted_date
        
        except ValueError:
            return date_str
        
    # Logger function to append text to the Logger window with a timestamp
    def log(text):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        window['-LOGGER-'].print(f'[{timestamp}] {text}', end='\n', text_color='black')

    def handle_input_change(event, key, prev_value, log_text):
        new_value = values[key]
        if new_value != prev_value:
            log(log_text)
            return new_value
        return prev_value

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'App Exit':
            break
        
        else :
            match event:
                case '-NIFTY-UNDERLYING-OPTION-':
                    event = '-NIFTY-UNDERLYING-OPTION-'
                    ul_option = values[event]
                    log(f'NIFTY Underlying Selected: {ul_option}')
                    window[event].update(ul_option)

                case '-NIFTY-INTRA-OVERNIGHT-':
                    event = '-NIFTY-INTRA-OVERNIGHT-'
                    n_posn = values[event]
                    log(f'NIFTY Position : {n_posn}')
                    window[event].update(n_posn)
                
                case '-NIFTY-EXPIRY-DATE-':
                    event =  '-NIFTY-EXPIRY-DATE-'
                    n_exp_date = values[event]
                    n_exp_date = format_date_with_day(n_exp_date)
                    log(f'expiry date:{n_exp_date}')
                    window[event].update(n_exp_date)  # Update the input field with the selected date

                case '-NIFTY-EXPIRY-OPTION-':
                    event = '-NIFTY-EXPIRY-OPTION-'
                    selected_date = values[event]
                    formatted_date = format_date_with_day(selected_date)
                    log(f'Expiry choice:{formatted_date}')
                    window[event].update(formatted_date)  # Update the input field with the selected date

                case '-NIFTY-MONEYNESS-':
                    event = '-NIFTY-MONEYNESS-'
                    selected_atm = values[event]
                    log(f'NIFTY-MONEYNESS Selected: {selected_atm}')
                    window[event].update(selected_atm)

                case '-NIFTY-BROKER-OPTION-':
                    event = '-NIFTY-BROKER-OPTION-'
                    selected_nifty_broker = values[event]
                    log(f'NIFTY BROKER  Selected: {selected_nifty_broker}')
                    window[event].update(selected_nifty_broker)

                case '-NIFTY-TRADE-MODE-':
                    event = '-NIFTY-TRADE-MODE-'
                    tm = values[event]
                    log(f'NIFTY-TRADE-MODE Selected: {tm}')
                    window[event].update(tm)

                case '-NIFTY-TARGET_RATIO-':
                    event = '-NIFTY-TARGET_RATIO-'
                    n_target_ratio = values[event]
                    log(f'NIFTY-TRADE-MODE Selected: {n_target_ratio}')
                    window[event].update(n_target_ratio)

                case _:
                    ...

        if (event == '-NIFTY-PREMIUM-' + "_Enter") or (event == '-NIFTY-PREMIUM-' + "_NIFTY-FOCUS_OUT_PREMIUM"):
            if values['-NIFTY-PREMIUM-'] == '':
                prev_nifty_premium = None
            elif number_with_2_decimal_places(values['-NIFTY-PREMIUM-']) is not None:
                tmp = prev_nifty_premium
                prev_nifty_premium = round(float(values['-NIFTY-PREMIUM-']), 2)
                if tmp != prev_nifty_premium:
                    log(f"Nifty Premium changed: {prev_nifty_premium}")
                window['-NIFTY-PREMIUM-'].update(prev_nifty_premium)
            else:
                window['-NIFTY-PREMIUM-'].update('')
                prev_nifty_premium = None

        cmp_event = '-NIFTY-ALERT-LEVEL-'
        focus = '_NIFTY-FOCUS_OUT_ALERT'

        if (event == cmp_event + '_Enter') or (event == cmp_event+focus):
            if values[cmp_event] == '':
                n_alert = None
            elif number_with_2_decimal_places(values[cmp_event]) is not None:
                tmp = n_alert
                n_alert = round(float(values[cmp_event]), 2)
                if tmp != n_alert:
                    log(f"Nifty Alert Level {n_alert}")
                window[cmp_event].update(n_alert)
            else:
                window[cmp_event].update('')
                n_alert = None

        cmp_event = '-NIFTY-BUY-LEVEL-'
        focus = '_NIFTY-FOCUS_OUT_B-ENTRY'
        log_mesg = 'B Level'
        if (event == cmp_event + "_Enter") or (event == cmp_event + focus):
            if values[cmp_event] == '':
                n_b_entry = None
            elif number_with_2_decimal_places(values[cmp_event]) is not None:
                tmp = n_b_entry
                n_b_entry = round(float(values[cmp_event]), 2)
                if tmp != n_b_entry:
                    log(f"Nifty {log_mesg} changed: {n_b_entry}")
                window[cmp_event].update(n_b_entry)
            else:
                window[cmp_event].update('')
                n_b_entry = None


        cmp_event = '-NIFTY-SHORT-LEVEL-'
        focus = '_NIFTY-FOCUS_OUT_S-ENTRY'
        log_mesg = 'S Level'
        
        if (event == cmp_event + "_Enter") or (event == cmp_event + focus):
            if values[cmp_event] == '':
                n_s_entry = None
            elif number_with_2_decimal_places(values[cmp_event]) is not None:
                tmp = n_s_entry
                n_s_entry = round(float(values[cmp_event]), 2)
                if tmp != n_s_entry:
                    log(f"Nifty {log_mesg} changed: {n_s_entry}")
                window[cmp_event].update(n_s_entry)
            else:
                window[cmp_event].update('')
                n_s_entry = None

        cmp_event = '-NIFTY-LONG-T1-LEVEL-'
        focus = '_NIFTY-FOCUS_OUT_S-ENTRY'
        log_mesg = 'Long T1 Level'
        
        if (event == cmp_event + "_Enter") or (event == cmp_event + focus):
            if values[cmp_event] == '':
                n_s_entry = None
            elif number_with_2_decimal_places(values[cmp_event]) is not None:
                tmp = n_s_entry
                n_s_entry = round(float(values[cmp_event]), 2)
                if tmp != n_s_entry:
                    log(f"Nifty {log_mesg} changed: {n_s_entry}")
                window[cmp_event].update(n_s_entry)
            else:
                window[cmp_event].update('')
                n_s_entry = None


















        if event == '-BANKNIFTY-OPTION-':
            selected_option = values['-BANKNIFTY-OPTION-']
            log(f'Bank Nifty Option Selected: {selected_option}')
            window['-BANKNIFTY-OPTION-'].update(selected_option)
        
        elif event == '-NIFTY-ATM-':
            selected_atm = values['-NIFTY-ATM-']
            log(f'NIFTY ATM Selected: {selected_atm}')
            window['-NIFTY-ATM-'].update(selected_atm)
        
        elif event == '-BANKNIFTY-ATM-':
            selected_atm = values['-BANKNIFTY-ATM-']
            log(f'Bank Nifty ATM Selected: {selected_atm}')
            window['-BANKNIFTY-ATM-'].update(selected_atm)    

        elif event == '-NIFTY-CE-BUY-':
            log('NIFTY CE BUY Button Click')
        elif event == '-NIFTY-CE-SELL-':
            log('NIFTY CE SELL Button Click')
        elif event == '-NIFTY-PE-BUY-':
            log('NIFTY PE BUY Button Click')
        elif event == '-NIFTY-PE-SELL-':
            log('NIFTY PE SELL Button Click')

        elif event == '-BANKNIFTY-CE-BUY-':
            log('BANKNIFTY CE BUY Button Click')
        elif event == '-BANKNIFTY-CE-SELL-':
            log('BANKNIFTY CE SELL Button Click')
        elif event == '-BANKNIFTY-PE-BUY-':
            log('BANKNIFTY PE BUY Button Click')
        elif event == '-BANKNIFTY-PE-SELL-':
            log('BANKNIFTY PE SELL Button Click')

        # Check if the input fields have changed and log their values with a delay
        elif (event == '-NIFTY-QTY-LOTS-' + "_Enter") or (event == '-NIFTY-QTY-LOTS-' + "_NIFTY-FOCUS_OUT_QTY"):
            if values['-NIFTY-QTY-LOTS-'] == '':
                prev_nifty_qty = None
            elif (integer(values["-NIFTY-QTY-LOTS-"])) is not None:
                tmp  = prev_nifty_qty
                prev_nifty_qty = round(float(values['-NIFTY-QTY-LOTS-']))
                if tmp != prev_nifty_qty:
                    log(f"Nifty Qty changed: {prev_nifty_qty}")
                    window["-NIFTY-QTY-LOTS-"].update(prev_nifty_qty)  # Update the input field with the rounded value
            else:
                # User entered a non-integer value, so blank the QTY input box
                window["-NIFTY-QTY-LOTS-"].update('')
                prev_nifty_qty = None  # Reset prev_qty to None

        # Check if the input fields have changed and log their values when focus out event occurs
        elif (event == '-NIFTY-MAX-LOSS-' + "_Enter") or (event == '-NIFTY-MAX-LOSS-' + "_NIFTY-FOCUS_MAX_LOSS"):
            
            if values['-NIFTY-MAX-LOSS-'] == '':
                prev_nifty_max_loss = None
            elif number_with_2_decimal_places(values['-NIFTY-MAX-LOSS-']) is not None:
                tmp = prev_nifty_max_loss
                prev_nifty_max_loss = round(float(values['-NIFTY-MAX-LOSS-']), 2)
                if tmp != prev_nifty_max_loss:
                    log(f"Nifty Max Loss changed: {prev_nifty_max_loss}")
                window['-NIFTY-MAX-LOSS-'].update(prev_nifty_max_loss)
            else:
                window['-NIFTY-MAX-LOSS-'].update('')
                prev_nifty_max_loss = None

        elif (event == '-NIFTY-MAX-PROFIT-' + "_Enter" or (event == '-NIFTY-MAX-PROFIT-' + "_NIFTY-FOCUS_MAX_PROFIT")):
            if values['-NIFTY-MAX-PROFIT-'] == '':
                prev_nifty_max_profit = None
            elif number_with_2_decimal_places(values['-NIFTY-MAX-PROFIT-']) is not None:
                tmp = prev_nifty_max_profit
                prev_nifty_max_profit = round(float(values['-NIFTY-MAX-PROFIT-']), 2)
                if tmp != prev_nifty_max_profit:
                    log(f"Nifty Max Profit changed: {prev_nifty_max_profit}")
                window['-NIFTY-MAX-PROFIT-'].update(prev_nifty_max_profit)
            else:
                window['-NIFTY-MAX-PROFIT-'].update('')
                prev_nifty_max_profit = None

        # Check if the input fields have changed and log their values with a delay
        elif (event == '-BANKNIFTY-QTY-' + "_Enter") or (event == '-BANKNIFTY-QTY-' + "_BANKNIFTY-FOCUS_OUT_QTY"):
            if values['-BANKNIFTY-QTY-'] == '':
                prev_banknifty_qty = None
            elif (integer(values["-BANKNIFTY-QTY-"])) is not None:
                tmp  = prev_banknifty_qty
                prev_banknifty_qty = round(float(values['-BANKNIFTY-QTY-']))
                if tmp != prev_banknifty_qty:
                    log(f"Bank Qty changed: {prev_banknifty_qty}")
                    window["-BANKNIFTY-QTY-"].update(prev_banknifty_qty)  # Update the input field with the rounded value
            else:
                # User entered a non-integer value, so blank the QTY input box
                window["-BANKNIFTY-QTY-"].update('')
                prev_banknifty_qty = None  # Reset prev_qty to None

        # Check if the input fields have changed and log their values when focus out event occurs
        elif (event == '-BANKNIFTY-MAX-LOSS-' + "_Enter") or (event == '-BANKNIFTY-MAX-LOSS-' + "_BANKNIFTY-FOCUS_MAX_LOSS"):
            
            if values['-BANKNIFTY-MAX-LOSS-'] == '':
                prev_banknifty_max_loss = None
            elif number_with_2_decimal_places(values['-BANKNIFTY-MAX-LOSS-']) is not None:
                tmp = prev_banknifty_max_loss
                prev_banknifty_max_loss = round(float(values['-BANKNIFTY-MAX-LOSS-']), 2)
                if tmp != prev_banknifty_max_loss:
                    log(f"BANKNifty Max Loss changed: {prev_banknifty_max_loss}")
                window['-BANKNIFTY-MAX-LOSS-'].update(prev_banknifty_max_loss)
            else:
                window['-BANKNIFTY-MAX-LOSS-'].update('')
                prev_banknifty_max_loss = None

        elif (event == '-BANKNIFTY-MAX-PROFIT-' + "_Enter" or (event == '-BANKNIFTY-MAX-PROFIT-' + "_BANKNIFTY-FOCUS_MAX_PROFIT")):
            if values['-BANKNIFTY-MAX-PROFIT-'] == '':
                prev_banknifty_max_profit = None
            elif number_with_2_decimal_places(values['-BANKNIFTY-MAX-PROFIT-']) is not None:
                tmp = prev_banknifty_max_profit
                prev_banknifty_max_profit = round(float(values['-BANKNIFTY-MAX-PROFIT-']), 2)
                if tmp != prev_banknifty_max_profit:
                    log(f"Bank Nifty Max Profit changed: {prev_banknifty_max_profit}")
                window['-BANKNIFTY-MAX-PROFIT-'].update(prev_banknifty_max_profit)
            else:
                window['-BANKNIFTY-MAX-PROFIT-'].update('')
                prev_banknifty_max_profit = None

    # Close the window
    window.close()

if __name__ == '__main__':
    main ()

