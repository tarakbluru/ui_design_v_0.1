import PySimpleGUI as sg

# Initialize the layout with a container for buttons
layout = [
    [sg.Text("Dynamic Buttons Example")],
    [sg.Button("Static Button 1"), sg.Button("Static Button 2")],
    [sg.Text("Dynamic Buttons:")],
    [sg.Button("Dynamic Button 1", key="-BUTTON1-"), sg.Button("Dynamic Button 2", key="-BUTTON2-")],  # Container for dynamic buttons
    [sg.Button("Toggle Dynamic Buttons"), sg.Exit()]
]

# Create the initial window
window = sg.Window("Dynamic Buttons Example", layout, finalize=True)

dynamic_buttons_visible = False  # Initial visibility state

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break
    elif event == "Toggle Dynamic Buttons":
        dynamic_buttons_visible = not dynamic_buttons_visible  # Toggle visibility state

        # Hide or unhide the dynamic buttons based on the condition
        window["-BUTTON1-"].update(visible=dynamic_buttons_visible)
        window["-BUTTON2-"].update(visible=dynamic_buttons_visible)

window.close()
