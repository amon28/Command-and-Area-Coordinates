import PySimpleGUI as Gui
import pyperclip
import math

# First the window layout in 2 columns

file_directory = ""
file_str = []

window = Gui.Window("Commands and Coordinates")
menu_def = [
    ['Help', 'Command'],
    ['Command Template',['execute',['execute setblock','execute loot','execute summon'],
                        ['execute if/else',['execute if block']]]]
    ]


def gui_initialization():
    coordinate1_layout = [
        [
            Gui.Text(text="Command:", size=(20, 1))
            
        ],
        [
            Gui.Input("", size=(90, 1), key="command")
        ],
        [
            Gui.Text(text="AREA X:", size=(20, 1)),
            Gui.Text(text="AREA Y:", size=(19, 1)),
            Gui.Text(text="AREA Z:", size=(18, 1))
        ],
        [
            Gui.Input("0", size=(22, 1), key="area1"),
            Gui.Input("0", size=(22, 1), key="area2"),
            Gui.Input("0", size=(22, 1), key="area3"),
            Gui.Button(button_text="Submit!", enable_events=True, key="submit_button")
        ],
        [   
            Gui.Text(text="Fixed X Offset:"),    
            Gui.Input("0", size=(5, 1), disabled=True, key="fixx_input"),
            Gui.Checkbox("", enable_events=True, key="fixx_checkbox"),
            Gui.Text(text="Fixed Y Offset:"),
            Gui.Input("0", size=(5, 1), disabled=True, key="fixy_input"),
            Gui.Checkbox("", enable_events=True, key="fixy_checkbox"),
            Gui.Text(text="Fixed Z Offset:"),
            Gui.Input("0", size=(5, 1), disabled=True, key="fixz_input"),
            Gui.Checkbox("", enable_events=True, key="fixz_checkbox"),           
        ]
    ]

    multi_line = [
        [
            Gui.Multiline("", size=(90, 20), disabled=True, key="multiline1")
        ]
    ]

    layout2 = [
        [
            Gui.FileSaveAs(button_text="Save As", file_types=(('Text', '.txt'), ('Jason', '.json'),('Mcfunction','.mcfunction')), enable_events=True, size=(20, 1), key="print_button")
        ],
        [
            Gui.Button("Copy to Clipboard", key="copy"),
            Gui.Button("Clear", key="clear")
        ]
    ]

    final_layout = [
        [
            Gui.Menu(menu_def),
            Gui.Column(layout=coordinate1_layout)
        ],
        [
            Gui.Column(justification="center", layout=multi_line)
        ],
        [
            Gui.Column(justification="center", element_justification="center", layout=layout2)
        ]
    ]

    global window
    window = Gui.Window("Command and Area Coordinates", layout=final_layout)


def event_listener():
    while True:
        event, values = window.read()
        # print("Event:", event, " - Value:", values)

        match event:
            case "Command":
                newLayout = [
                    [
                        Gui.Text("Any command with the keywords in it will be replace by the inputs.")
                    ],
                    [
                        Gui.Text("Keywords: Area X:#coordx, Area Y:#coordy, Area Z:#coordz, Offset: #offset",text_color = "#00FF00")
                    ]
                ]
                newWindow = Gui.Window("Help Command", force_toplevel=True, keep_on_top=True, layout=newLayout)
                while True:
                    event, values = newWindow.read()
                    if event in ("NONE", Gui.WIN_CLOSED):
                        break
                    newWindow.close()

            case "fixx_checkbox":
                if values["fixx_checkbox"]:
                    window["fixx_input"].update(disabled=False)
                else:
                    window["fixx_input"].update(disabled=True)

            case "fixy_checkbox":
                if values["fixy_checkbox"]:
                    window["fixy_input"].update(disabled=False)
                else:
                    window["fixy_input"].update(disabled=True)

            case "fixz_checkbox":
                if values["fixz_checkbox"]:
                    window["fixz_input"].update(disabled=False)
                else:
                    window["fixz_input"].update(disabled=True)

            case "submit_button":
                command = values["command"]
                area1 = values["area1"]
                area2 = values["area2"]
                area3 = values["area3"]       
                if area1 and area2 and area3 and command:
                    if area1.isnumeric() and area2.isnumeric() and area3.isnumeric():
                        offsetX = "0"
                        offsetY = "0"
                        offsetZ = "0"

                        if values["fixx_checkbox"]:
                            if values["fixx_input"]:                      
                                offsetX = values["fixx_input"]
                        else:
                            offsetX = "-" + str(math.floor(int(area1)/2))

                        if values["fixy_checkbox"]:
                            if values["fixy_input"]:                      
                                offsetY = values["fixy_input"]
                        else:
                            offsetY = "-" + str(math.floor(int(area2)/2))

                        if values["fixz_checkbox"]:
                            if values["fixz_input"]:                      
                                offsetZ = values["fixz_input"]
                        else:
                            offsetZ = "-" + str(math.floor(int(area3)/2))
                        
                        offset = "~" + offsetX + " ~" + offsetY + " ~" + offsetZ
                        output = ""
                        for areaY in range (0, int(area2)+1):
                            for areaX in range (0, int(area1)+1):
                                for areaZ in range (0, int(area3)+1):
                                    output= output + command.replace("#coordx", str(areaX)).replace("#coordy", str(areaY)).replace("#coordz", str(areaZ)).replace("#offset", offset) + "\n"
                        window["multiline1"].update(value=output, text_color = "#000000")
                    else:
                        window["multiline1"].update(value="Area Inputs must be numbers!", text_color = "#FF0000", justification="center")
                else:
                        window["multiline1"].update(value="Fill out all the inputs!", text_color = "#FF0000", justification="center")

            case "print_button":
                if values["multiline1"] == "":
                    pass
                with open(values["print_button"], 'w') as file:
                    file.write(values["multiline1"])
                file.close()

            case "clear":
                window["multiline1"].update(value="")

            case "copy":
                pyperclip.copy(values["multiline1"])
                #Gui.popup("Successfully Copied to Clipboard!", text_color="#6cf065")

            case "execute":
                window["command"].update(value="execute positioned #offset run ")
            case "execute setblock":
                window["command"].update(value="execute positioned #offset run setblock #coordx #coordy #coordz planks")
            case "execute summon":
                window["command"].update(value="execute positioned #offset run summon #coordx #coordy #coordz")
            case "execute loot":
                window["command"].update(value="execute positioned #offset run loot spawn #coordx #coordy #coordz loot \"entities/blaze\"")

            case "execute if block":
                window["command"].update(value="execute if block ~#coordx ~#coordy ~#coordz planks run say Plank Found!")    
            case _:
                if event in ("None", Gui.WIN_CLOSED):
                    break
    window.close()


gui_initialization()
event_listener()
