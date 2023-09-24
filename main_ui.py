import PySimpleGUI as sg
import datetime  # Added datetime module for timestamp

# Define the layout of your GUI
layout = [
    [sg.Text('Select Option 1:')],
    [sg.Combo(['NIFTY', 'BANKNIFTY'], key='-OPTION1-', enable_events=True, size=(20, 1))],
    [sg.Text('Select Option 2:')],
    [sg.Combo([], key='-OPTION2-', enable_events=True, size=(20, 1))],  # Initialize as empty
    [sg.Text('Selected Option 1:'), sg.Text('', size=(20, 1), key='-SELECTED-OPTION1-')],
    [sg.Text('Selected Option 2:'), sg.Text('', size=(20, 1), key='-SELECTED-OPTION2-')],
    [sg.Text('Select ATM:')],
    [sg.Combo(['ATM-5', 'ATM-4', 'ATM-3', 'ATM-2', 'ATM-1', 'ATM', 'ATM+1', 'ATM+2', 'ATM+3', 'ATM+4', 'ATM+5'], key='-ATM-', size=(20, 1), enable_events=True)],
    [sg.Text('Selected ATM:'), sg.Text('', size=(20, 1), key='-SELECTED-ATM-')],
    [sg.Text('Qty in Lots:')],
    [sg.InputText('', key='-QTY-')],
    [sg.Text('Max Loss:')],
    [sg.InputText('', key='-MAX-LOSS-')],
    [sg.Text('Max Profit:')],
    [sg.InputText('', key='-MAX-PROFIT-')],
    [sg.Button('CE BUY \u2191', button_color=('white', 'green')), sg.Button('CE SELL \u2193', button_color=('white', 'red'))],  # CE buttons with up and down arrows
    [sg.Button('PE BUY \u2193', button_color=('white', 'red')), sg.Button('PE SELL \u2191', button_color=('white', 'green'))],  # PE buttons with up and down arrows
    [sg.Text('Logger Window:')],
    [sg.Multiline('', key='-LOGGER-', size=(100, 10))],  # Logger window with a larger size
    [sg.Button('Exit', size=(10, 1))]  # Exit button at the lowest row
]

# Create the window
window = sg.Window('QuickTrade : ', layout, finalize=True)
window['-QTY-'].bind("<FocusIn>", "_FOCUS_IN_QTY")
window['-QTY-'].bind("<FocusOut>", "_FOCUS_OUT_QTY")
window['-QTY-'].bind("<Return>", "_Enter")

window['-MAX-LOSS-'].bind("<Return>", "_Enter")
window['-MAX-LOSS-'].bind("<FocusOut>", "_FOCUS_MAX_LOSS")

window['-MAX-PROFIT-'].bind("<Return>", "_Enter")
window['-MAX-PROFIT-'].bind("<FocusOut>", "_FOCUS_MAX_PROFIT")

# Options for the second dropdown based on Option 1
option2_options = {
    'NIFTY': ['NIFTY-I', 'NIFTY_INDEX'],
    'BANKNIFTY': ['BANKNIFTY-I', 'BANKNIFTY_INDEX']
}

# Initialize variables to store the previous values of the input fields
prev_qty = None  # Initialize as None
prev_max_loss = None  # Initialize as None
prev_max_profit = None  # Initialize as None

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
    elif event == '-OPTION1-':
        selected_option1 = values['-OPTION1-']
        log(f'Option 1 Selected: {selected_option1}')
        window['-SELECTED-OPTION1-'].update(selected_option1)
        
        # Update the options for the second dropdown based on the selection in the first dropdown
        if selected_option1 in option2_options:
            options = option2_options[selected_option1]
            
            # Calculate the maximum string length among all options
            max_option_length = max(len(option) for option in options)
            
            # Update the second dropdown with the options and set its width to fit the maximum option length
            window['-OPTION2-'].update(values=options, size=(max_option_length + 2, None))
        else:
            window['-OPTION2-'].update(values=[])
    
    elif event == '-OPTION2-':
        selected_option2 = values['-OPTION2-']
        log(f'Option 2 Selected: {selected_option2}')
        window['-SELECTED-OPTION2-'].update(selected_option2)
    
    elif event == '-ATM-':
        selected_atm = values['-ATM-']
        log(f'ATM Selected: {selected_atm}')
        window['-SELECTED-ATM-'].update(selected_atm)
    
    # Handle button clicks and log them
    elif 'CE BUY' in event:
        log('CE BUY button clicked')
    elif 'CE SELL' in event:
        log('CE SELL button clicked')
    elif 'PE BUY' in event:
        log('PE BUY button clicked')
    elif 'PE SELL' in event:
        log('PE SELL button clicked')
    
    # Check if the input fields have changed and log their values with a delay
    elif (event == '-QTY-' + "_Enter") or (event == '-QTY-' + "_FOCUS_OUT_QTY"):
        log(f"Qty changed: {values['-QTY-']}")
        if values['-QTY-'] == '':
            prev_qty = None
        elif (value:= integer(values["-QTY-"])) is not None:
            window["-QTY-"].update(value)  # Update the input field with the rounded value
            prev_qty = value
        else:
            # User entered a non-integer value, so blank the QTY input box
            window["-QTY-"].update('')
            prev_qty = None  # Reset prev_qty to None

    # Check if the input fields have changed and log their values when focus out event occurs
    elif (event == '-MAX-LOSS-' + "_Enter") or (event == '-MAX-LOSS-' + "_FOCUS_MAX_LOSS"):
        
        if values['-MAX-LOSS-'] == '':
            prev_max_loss = None
        elif number_with_2_decimal_places(values['-MAX-LOSS-']) is not None:
            tmp = prev_max_loss
            prev_max_loss = round(float(values['-MAX-LOSS-']), 2)
            if tmp != prev_max_loss:
                log(f"Max Loss changed: {prev_max_loss}")
            window['-MAX-LOSS-'].update(prev_max_loss)
        else:
            window['-MAX-LOSS-'].update('')
            prev_max_loss = None

    elif (event == '-MAX-PROFIT-' + "_Enter" or (event == '-MAX-PROFIT-' + "_FOCUS_MAX_PROFIT")):
        if values['-MAX-PROFIT-'] == '':
            prev_max_profit = None
        elif number_with_2_decimal_places(values['-MAX-PROFIT-']) is not None:
            tmp = prev_max_profit
            prev_max_profit = round(float(values['-MAX-PROFIT-']), 2)
            if tmp != prev_max_profit:
                log(f"Max Profit changed: {prev_max_profit}")
            window['-MAX-PROFIT-'].update(prev_max_profit)
        else:
            window['-MAX-PROFIT-'].update('')
            prev_max_profit = None

# Close the window
window.close()