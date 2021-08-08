import PySimpleGUI as sg
import polymer_chains as pc

# chain options available in the GUI
chain_options = ["Random Walk", "Freely Rotating", "Rotational Isomeric", "None"]

# Function to get the help_text file
def get_helptext():
	helptext = "alkdsfhaksf\nadkfhl\n\t\taskjdga\n\tasdfhasf"
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
def calculate_chain_properties(values, cprint=True, round=True):
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

# Function to get the index of a chain when provided an event string
def get_chain_index(event):
    chain_index_start = event.index("-chain") + 6
    chain_index_end = event.index("_")
    chain_index = int(event[chain_index_start:chain_index_end]) -1
    return chain_index
