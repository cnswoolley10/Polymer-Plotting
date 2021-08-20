import PySimpleGUI as sg
import polymer_chains as pc
import os

# chain options available in the GUI
chain_options = ["Random Walk", "Freely Rotating", "Rotational Isomeric", "None"]
calculator_checkboxes = ["N", "l", "E2E", "CoM", "RoG"]
calculator_checkbox_tooltips = ["Number of segments", "Length of each segment", "End to end distance", "Centre of mass", "Radius of gyration"]
calculator_checkbox_keys = ["-check_{}-".format(label) for label in calculator_checkboxes]

# Build the main layout of the GUI
# set number of chains to create frames for
chain_number = 5
top_row_height = 100
bottom_row_height = 500
left_col_width = 300
right_col_width = 650
element_justification = "center"
pad = (0,0)
canvas_size = (600,400)
calculator_checkboxes_per_line = 5
chains_column_height = 500

# create a chain frame for each chain and put it in the chains column
chain_objects = []
chains_column_layout = []
chain_frame_RC = ["confirm-", "print_coords-"]
chain_combos = []#######################################################################################################################################
for i in range(1, chain_number+1):
    new_chain_frame_layout = [
        [sg.T("Chain type:"), sg.Combo(chain_options, key="-chain{}_type-".format(i), default_value="Random Walk")],
        [sg.T("Chain length:"), sg.Input(key="-chain{}_length-".format(i), enable_events=True, default_text="100", size=(6,1))]
    ]
    new_chain_frame_column = sg.Column(new_chain_frame_layout, pad=pad)
    new_chain_frame = sg.Frame("Chain {}:".format(i), [[new_chain_frame_column]], right_click_menu=["", [("-chain{}_".format(i) + option) for option in chain_frame_RC]])
    chains_column_layout.append([new_chain_frame])
    chain_objects.append(pc.Random_Walk_Chain(100))
chains_column = sg.Column(layout=chains_column_layout, size=(left_col_width-20, chains_column_height), pad=(0,0))

# precalculate chain coords for initial chains
for chain in chain_objects:
    chain.calculate_coords()
    chain.calculate_CoM()
    chain.calculate_RoG()
    chain.calculate_end2end()

# create calulator frame
calculator_frame_layout = []
calculator_frame_layout_line = []
for i, label in enumerate(calculator_checkboxes):
    new_checkbox = sg.Checkbox(label, key=calculator_checkbox_keys[i], tooltip=calculator_checkbox_tooltips[i])
    calculator_frame_layout_line.append(new_checkbox)
    if ((i+1) % calculator_checkboxes_per_line == 0) or i == len(calculator_checkboxes)-1:
        calculator_frame_layout.append(calculator_frame_layout_line)
        calculator_frame_layout_line = []
calculator_frame_layout.append([sg.B("Calculate", key="-calculate_chain_properties-"), sg.B("Save", key="-save_chain_properties-")])
calculator_frame = sg.Frame("Properties Calculator", layout = calculator_frame_layout)

# new layout method
chain_options_frame_column = sg.Column([[calculator_frame], [sg.B("Confirm all", key="-confirm_all_chains-"), sg.B("Clear all", key="-clear_all_chains-")], [chains_column]], size=(left_col_width,bottom_row_height), scrollable=True, vertical_scroll_only=True)
chain_options_frame = sg.Frame("Chain Options", layout=[[chain_options_frame_column]])
plotting_frame_column = sg.Column(layout = [
    [sg.T('Controls:')],
    [sg.Canvas(key='controls_cv', size = (100,30), pad=(0,0))],
    [sg.T('Figure:')],
    [sg.Column(
        layout=[
            [sg.Canvas(key='fig_cv',
                       # it's important that you set this size
                       size=canvas_size
                       )]
        ],
        background_color='#DAE0E6',
        pad=(0, 0)
        )]], size=(right_col_width,bottom_row_height))
plotting_frame = sg.Frame("Plotting", key="-plotting_frame-", layout = [[plotting_frame_column]])
output_multiline = sg.Multiline("This is the text output\n", key="-output_textbox-", size=(80,5), write_only=True, reroute_cprint=True)
output_frame_column = sg.Column([[output_multiline, sg.Column([[sg.B("Popout", key="-output_popout-")], [sg.B("Clear", key="-output_clear-")]])]], size=(right_col_width,top_row_height))
output_frame = sg.Frame("Info", layout = [[output_frame_column]])
main_options_frame_column = sg.Column(layout = [
    [sg.T('Demo')],
    [sg.B('Plot'), sg.B('Exit'), sg.B("Help", key="-help-")]], size=(left_col_width,top_row_height))
main_options_frame = sg.Frame("Main", layout = [[main_options_frame_column]])

# Function to get the help_text file
def get_helptext():
    with open("help_text.txt") as helptext_file:
	       helptext = helptext_file.read()
    return helptext

# This is to include a matplotlib figure in a Tkinter canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)
class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

# Function to open a second window to display text
def open_text_window(text, key, size=(100,30), title="Output Text"):
    layout = [[sg.Multiline(text, key=key, size=size, write_only=True)], [sg.B("Save All", key="-save_all_output-")]]
    window = sg.Window(layout=layout, title=title, modal=True)
    choice = None
    while True:
        event, values = window.read()
        print(event)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "-save_all_output-":
            save_location = sg.popup_get_file("Select a save location", save_as=True, initial_folder=os.getcwd(), default_extension=".txt")
            pass


    window.close()

# Function to output the selected chain properties to the output box
def calculate_chain_properties(chain_objects, values, cprint=True, round=True):
    keys_to_output = ["Chain_name"]
    for key in calculator_checkbox_keys:
        if values[key]:
            keys_to_output.append(key)
    output_properties_lines = []
    output_properties_header = ""
    for key in keys_to_output:
        if key in calculator_checkbox_keys:
            if key == calculator_checkbox_keys[3]:
                output_properties_label = calculator_checkboxes[calculator_checkbox_keys.index(key)]
                output_properties_header += "{}_x,{}_y,{}_z,".format(output_properties_label,output_properties_label,output_properties_label)
            else:
                output_properties_header += calculator_checkboxes[calculator_checkbox_keys.index(key)] + ","
        else:
            output_properties_header += key + ","
    output_properties_lines.append(output_properties_header)
    for chain in chain_objects:
        output_properties_chain_line = ""
        if chain:
            if round:
                for key in keys_to_output:
                    if key == "Chain_name":
                        output_properties_chain_line += chain.name + ","
                    elif key == calculator_checkbox_keys[0]:
                        output_properties_chain_line += "{:.2e},".format(chain.length)
                    elif key == calculator_checkbox_keys[1]:
                        output_properties_chain_line += "{},".format(1)
                    elif key == calculator_checkbox_keys[2]:
                        output_properties_chain_line += "{:.2e},".format(chain.end2end)
                    elif key == calculator_checkbox_keys[3]:
                        output_properties_chain_line += "{:.2e},{:.2e},{:.2e},".format(chain.CoM[0],chain.CoM[1],chain.CoM[2])
                    elif key == calculator_checkbox_keys[4]:
                        output_properties_chain_line += "{:.2e},".format(chain.RoG)
                output_properties_lines.append(output_properties_chain_line)
            else:
                for key in keys_to_output:
                    if key == "Chain_name":
                        output_properties_chain_line += chain.name + ","
                    elif key == calculator_checkbox_keys[0]:
                        output_properties_chain_line += "{},".format(chain.length)
                    elif key == calculator_checkbox_keys[1]:
                        output_properties_chain_line += "{},".format(1)
                    elif key == calculator_checkbox_keys[2]:
                        output_properties_chain_line += "{},".format(chain.end2end)
                    elif key == calculator_checkbox_keys[3]:
                        output_properties_chain_line += "{},{},{},".format(chain.CoM[0],chain.CoM[1],chain.CoM[2])
                    elif key == calculator_checkbox_keys[4]:
                        output_properties_chain_line += "{},".format(chain.RoG)
                output_properties_lines.append(output_properties_chain_line)
    if cprint:
        sg.cprint("\nCalculated Properties:")
        for line in output_properties_lines:
            sg.cprint(line)
    return output_properties_lines

# Function to save the calculated chain properties
def save_chain_properties(chain_objects, values):
            chain_properties_to_save = calculate_chain_properties(chain_objects, values, cprint=False, round=False)
            chain_properties_to_save = [line + "\n" for line in chain_properties_to_save]
            #print(chain_properties_to_save)
            save_location = sg.popup_get_file("Select a save location", save_as=True, initial_folder=os.getcwd(), default_extension=".csv", file_types=(("Comma separated values", ".csv"),))
            if save_location:
                with open(save_location,"w") as save_properties_file:
                    save_properties_file.writelines(chain_properties_to_save)

# Function for confirm chain button
def confirm_chain(chain_objects, chain_index, values):
    chain_int = chain_index + 1
    calculate_coords_ = True
    if values["-chain{}_type-".format(chain_int)] == chain_options[0]:
        chain_objects[chain_index] = pc.Random_Walk_Chain(int(values["-chain{}_length-".format(chain_int)]))
    elif values["-chain{}_type-".format(chain_int)] == chain_options[1]:
        chain_objects[chain_index] = pc.Freely_Rotating_Chain(int(values["-chain{}_length-".format(chain_int)]))
    elif values["-chain{}_type-".format(chain_int)] == chain_options[2]:
        chain_objects[chain_index] = pc.Rotational_Isomeric_Chain(int(values["-chain{}_length-".format(chain_int)]))
    else:
        chain_objects[chain_index] = None
        calculate_coords_ = False
    if calculate_coords_:
        chain_objects[chain_index].calculate_coords()
        chain_objects[chain_index].calculate_CoM()
        chain_objects[chain_index].calculate_RoG()
        chain_objects[chain_index].calculate_end2end()

# Function for clear chain button
def clear_chain(chain_objects, chain_index): ###########################################################################################################################################
    chain_objects[chain_index] = None
    sg.update(value)
# Function to get the index of a chain when provided an event string
def get_chain_index(event):
    chain_index_start = event.index("-chain") + 6
    chain_index_end = event.index("_")
    chain_index = int(event[chain_index_start:chain_index_end]) -1
    return chain_index
