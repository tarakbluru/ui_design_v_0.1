import PySimpleGUI as sg
import datetime  # Added datetime module for timestamp

# Define the layout of your GUI
layout = [
    [sg.TabGroup([
        [sg.Tab('NIFTY', [
            [sg.Text('Select Option:')],
            [sg.Combo(['NIFTY-I', 'NIFTY_INDEX'], key='-NIFTY-OPTION-', enable_events=True, size=(20, 1))],
            [sg.Text('Select ATM:')],
            [sg.Combo(['ATM-5', 'ATM-4', 'ATM-3', 'ATM-2', 'ATM-1', 'ATM', 'ATM+1', 'ATM+2', 'ATM+3', 'ATM+4', 'ATM+5'], key='-NIFTY-ATM-', size=(20, 1), enable_events=True)],
            [sg.Text('Qty in Lots:')],
            [sg.InputText('', key='-NIFTY-QTY-')],
            [sg.Text('Max Loss:')],
            [sg.InputText('', key='-NIFTY-MAX-LOSS-')],
            [sg.Text('Max Profit:')],
            [sg.InputText('', key='-NIFTY-MAX-PROFIT-')],
            [sg.Button('NIFTY CE BUY  \u2191', button_color=('white', 'green')),  sg.Button('NIFTY CE SELL \u2193', button_color=('white', 'red'))],  # CE buttons with up and down arrows
            [sg.Button('NIFTY PE SELL \u2191', button_color=('white', 'green')),  sg.Button('NIFTY PE BUY  \u2193', button_color=('white', 'red')) ],  # PE buttons with up and down arrows
        ])],
        [sg.Tab('Bank Nifty', [
            [sg.Text('Select Option:')],
            [sg.Combo(['BANKNIFTY-I', 'BANKNIFTY_INDEX'], key='-BANKNIFTY-OPTION-', enable_events=True, size=(20, 1))],
            [sg.Text('Select ATM:')],
            [sg.Combo(['ATM-5', 'ATM-4', 'ATM-3', 'ATM-2', 'ATM-1', 'ATM', 'ATM+1', 'ATM+2', 'ATM+3', 'ATM+4', 'ATM+5'], key='-BANKNIFTY-ATM-', size=(20, 1), enable_events=True)],
            [sg.Text('Qty in Lots:')],
            [sg.InputText('', key='-BANKNIFTY-QTY-')],
            [sg.Text('Max Loss:')],
            [sg.InputText('', key='-BANKNIFTY-MAX-LOSS-')],
            [sg.Text('Max Profit:')],
            [sg.InputText('', key='-BANKNIFTY-MAX-PROFIT-')],
            [sg.Button('BN_CE BUY  \u2191', button_color=('white', 'green')), sg.Button('BN_CE SELL \u2193', button_color=('white', 'red'))],  # CE buttons with up and down arrows
            [sg.Button('BN_PE SELL \u2191', button_color=('white', 'green')), sg.Button('BN_PE BUY  \u2193', button_color=('white', 'red')) ],  # PE buttons with up and down arrows
        ]),
        ]
        
    ])],
    [sg.Text('', size=(100, 1))],
    [sg.Text('Logger Window:')],
    [sg.Multiline('', key='-LOGGER-', size=(100, 10))],  # Logger window with a larger size
    [sg.Button('Exit', size=(10, 1))]  # Exit button at the lowest row
]

# Create the window
window = sg.Window('QuickTrade : ', layout, finalize=True)

window['-NIFTY-QTY-'].bind("<FocusIn>", "_NIFTY-FOCUS_IN_QTY")
window['-NIFTY-QTY-'].bind("<FocusOut>", "_NIFTY-FOCUS_OUT_QTY")
window['-NIFTY-QTY-'].bind("<Return>", "_Enter")

window['-NIFTY-MAX-LOSS-'].bind("<Return>", "_Enter")
window['-NIFTY-MAX-LOSS-'].bind("<FocusOut>", "_NIFTY-FOCUS_MAX_LOSS")

window['-NIFTY-MAX-PROFIT-'].bind("<Return>", "_Enter")
window['-NIFTY-MAX-PROFIT-'].bind("<FocusOut>", "_NIFTY-FOCUS_MAX_PROFIT")

window['-BANKNIFTY-QTY-'].bind("<FocusIn>", "_BANKNIFTY-FOCUS_IN_QTY")
window['-BANKNIFTY-QTY-'].bind("<FocusOut>", "_BANKNIFTY-FOCUS_OUT_QTY")
window['-BANKNIFTY-QTY-'].bind("<Return>", "_Enter")


window['-BANKNIFTY-MAX-LOSS-'].bind("<Return>", "_Enter")
window['-BANKNIFTY-MAX-LOSS-'].bind("<FocusOut>", "_BANKNIFTY-FOCUS_MAX_LOSS")

window['-BANKNIFTY-MAX-PROFIT-'].bind("<Return>", "_Enter")
window['-BANKNIFTY-MAX-PROFIT-'].bind("<FocusOut>", "_BANKNIFTY-FOCUS_MAX_PROFIT")


# Initialize variables to store the previous values of the input fields
prev_nifty_qty = None  # Initialize as None
prev_nifty_max_loss = None  # Initialize as None
prev_nifty_max_profit = None  # Initialize as None
prev_banknifty_qty = None  # Initialize as None
prev_banknifty_max_loss = None  # Initialize as None
prev_banknifty_max_profit = None  # Initialize as None

# Logger function to append text to the Logger window with a timestamp
def log(text):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    window['-LOGGER-'].print(f'[{timestamp}] {text}', end='\n', text_color='black')

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

def handle_input_change(event, key, prev_value, log_text):
    new_value = values[key]
    if new_value != prev_value:
        log(log_text)
        return new_value
    return prev_value

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    elif event == '-NIFTY-OPTION-':
        selected_option = values['-NIFTY-OPTION-']
        log(f'NIFTY Option Selected: {selected_option}')
        window['-NIFTY-OPTION-'].update(selected_option)
    
    elif event == '-BANKNIFTY-OPTION-':
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

    # Handle button clicks and log them
    elif 'NIFTY CE BUY' in event:
        log('NIFTY CE BUY button clicked')
    elif 'NIFTY CE SELL' in event:
        log('NIFTY CE SELL button clicked')
    elif 'NIFTY PE BUY' in event:
        log('NIFTY PE BUY button clicked')
    elif 'NIFTY PE SELL' in event:
        log('NIFTY PE SELL button clicked')

    elif 'BN_CE BUY' in event:
        log('BN CE BUY button clicked')
    elif 'BN_CE SELL' in event:
        log('BN CE SELL button clicked')
    elif 'BN_PE BUY' in event:
        log('BN_PE BUY button clicked')
    elif 'BN_PE SELL' in event:
        log('BN_PE SELL button clicked')


    # Check if the input fields have changed and log their values with a delay
    elif (event == '-NIFTY-QTY-' + "_Enter") or (event == '-NIFTY-QTY-' + "_NIFTY-FOCUS_OUT_QTY"):
        if values['-NIFTY-QTY-'] == '':
            prev_nifty_qty = None
        elif (integer(values["-NIFTY-QTY-"])) is not None:
            tmp  = prev_nifty_qty
            prev_nifty_qty = round(float(values['-NIFTY-QTY-']))
            if tmp != prev_nifty_qty:
                log(f"Nifty Qty changed: {prev_nifty_qty}")
                window["-NIFTY-QTY-"].update(prev_nifty_qty)  # Update the input field with the rounded value
        else:
            # User entered a non-integer value, so blank the QTY input box
            window["-NIFTY-QTY-"].update('')
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