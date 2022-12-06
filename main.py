import PySimpleGUI as sg
from PySimpleGUI import TABLE_SELECT_MODE_BROWSE
import os
import stat
import winshell
import sys

apps_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
files_list = os.listdir(apps_path)
files = []

for file in files_list:
    if os.path.isfile(fr"{apps_path}\{file}") and file.endswith(".lnk"):
        files.append([".", file])
    elif os.path.isdir(fr"{apps_path}\{file}"):
        for r_file in os.listdir(fr"{apps_path}\{file}"):
            if r_file.endswith(".lnk"):
                files.append([file, r_file.split('.lnk')[0]])

layout = [
    [
        sg.Col([[sg.Table(files, ["Path", "App Name"], size=(100, 400), col_widths=[14, 20], key="app_list",
                          auto_size_columns=False, select_mode=TABLE_SELECT_MODE_BROWSE, enable_events=True)]]),
        sg.Col([[sg.Text('Selected:'), sg.Text("None", key="selected_file")],
                [sg.Button("Launch", key="launch_btn", disabled=True),
                 sg.Button("Remove from list", key="remove_btn", disabled=True)],
                [sg.FileBrowse("Add to list", key="add_btn", enable_events=True)]],
               vertical_alignment="top")
    ],
]

main_window = sg.Window("Test", layout, size=(580, 400))
while True:
    event, values = main_window.read()
    print(event, values)

    if event == sg.WIN_CLOSED:
        sys.exit()

    if event == "app_list" and len(values.get('app_list')) > 0:
        selected_file = files[values["app_list"][0]]
        main_window["selected_file"].update(selected_file[1])
        main_window["launch_btn"].update(disabled=False)
        main_window["remove_btn"].update(disabled=False)

    if len(values.get('app_list')) > 0:
        selected_file = files[values["app_list"][0]]
        print(selected_file)
        if event == "launch_btn":
            os.popen(fr"{apps_path}\{selected_file[0]}\{selected_file[1]}.lnk")
        if event == "remove_btn":
            os.remove(fr"{apps_path}\{selected_file[0]}\{selected_file[1]}.lnk")
            files.remove(selected_file)
            main_window["app_list"].update(files)
    else:
        main_window["launch_btn"].update(disabled=True)
        main_window["remove_btn"].update(disabled=True)
        main_window["selected_file"].update("None")

    if event == "add_btn":
        if values.get('add_btn') != "":
            basename = os.path.basename(values.get('add_btn'))
            shortcut = winshell.shortcut(values.get('add_btn'))
            shortcut.path = apps_path
            shortcut.write(apps_path) #
