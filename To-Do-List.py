import os
import time
from tkinter import filedialog
import customtkinter
import pickle
import threading

root = customtkinter.CTk()
root.title("To-Do-List")
root.attributes('-topmost', True)
root.resizable(False, False)

settings = {
            "text_size": 20,
            "text_font": "Arial",
            "appearance_mode": "System",
            "font_size": "100%",
            "SCROLL_SPEED": 5,
            }
tasks = []


marked_tasks = []
scroll_pos = 0
running = True

customtkinter.set_appearance_mode(settings.get("appearance_mode"))
customtkinter.set_default_color_theme("dark-blue")


def change_appearance(mode):
    global settings
    customtkinter.set_appearance_mode(mode)
    settings["appearance_mode"] = mode


def change_text_size_font(size_font):
    global settings

    if type(size_font) == str:
        settings["text_font"] = size_font
    else:
        settings["text_size"] = size_font

    # update the label
    text_size_label.configure(text=f"Text size {settings.get('text_size'):.1f}")


def change_font_size(new_scaling: str):
    global settings

    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)
    settings["font_size"] = new_scaling


def remove_elements():
    global marked_tasks
    global tasks

    new_tasks = []

    for i, task in enumerate(tasks):
        if not i+1 in marked_tasks:
            new_tasks.append(task)

    marked_tasks = []
    tasks = new_tasks

    setup_list(scroll_pos)


def add_element(c):
    global tasks

    if tabview_root.current_name == "To Do List":
        if entry.get() != "" and not entry.get().isspace():
            tasks.append(entry.get())
            setup_list(scroll_pos)
            entry.delete(0, customtkinter.END)


def mark_element(element):
    marked_tasks.append(element)


def setup_list(progress):
    global tasks_frame

    # destroys the task frame and all the labels within it
    if tasks_frame is not None:
        tasks_frame.destroy()

    # tasks frame
    tasks_frame = customtkinter.CTkFrame(master=tabview_root.tab("To Do List"), width=260, height=300)
    tasks_frame.grid(row=1, column=0, columnspan=4)

    # tasks label
    tasks_label = customtkinter.CTkLabel(master=tasks_frame, text="Tasks", font=(settings.get("text_font"), settings.get("text_size")))
    tasks_label.place(x=0, y=progress)


    for count, task in enumerate(tasks):
        listbox = customtkinter.CTkCheckBox(master=tasks_frame, text=task, font=(settings.get("text_font"), settings.get("text_size")), command=lambda i=count+1: mark_element(i))
        if settings.get("text_size") <= 30:
            listbox.place(x=0, y=30 + 30 * count + progress)

        else:
            listbox.place(x=0, y=30*settings.get("text_size")/30 + 30 * (count*settings.get("text_size")/30) + progress)


def changed_tabview_root():
    if tabview_root.current_name == "To Do List":
        setup_list(scroll_pos)


def scroll(progress):
    global scroll_pos

    if tabview_root.current_name == "To Do List":
        if (progress.delta > 0 and scroll_pos+progress.delta//settings.get("SCROLL_SPEED") <= 0) or progress.delta < 0:
            scroll_pos += progress.delta//settings.get("SCROLL_SPEED")

            setup_list(scroll_pos)


def save_list(c):
    file_name = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save File", filetypes=(("Dat Files", "*.dat"), ("All Files", "*.*")))

    if file_name != "":
        if not file_name.endswith(".dat"):
            file_name = f"{file_name}.dat"


        output_file = open(file_name, "wb")

        pickle.dump([settings, tasks], output_file)


def load_list(c):
    global settings
    global tasks
    global root

    file_name = filedialog.askopenfilename(initialdir=os.getcwd(), title="Save File", filetypes=(("Dat Files", "*.dat"), ("All Files", "*.*")))

    if file_name != "":
        stuff = pickle.load(open(file_name, "rb"))
        settings, tasks = stuff[0], stuff[1]

        setup_list(scroll_pos)

        update_settings()


def update_settings():
    customtkinter.set_appearance_mode(settings.get("appearance_mode"))
    customtkinter.set_widget_scaling(int(str(settings.get("font_size")).replace("%", "")) / 100)

    # text settings
    text_size_slider.set(settings.get("text_size"))
    change_text_size_font(settings.get("text_size"))
    text_font_optionemenu.set(settings.get("text_font"))

    # appearance settings
    scaling_optionemenu.set(settings.get("font_size"))
    appearance_optionmenu.set(settings.get("appearance_mode"))


def update_root_size():
    time.sleep(1)
    while running:
        root.geometry(f"{frame.winfo_width()}x{frame.winfo_height()}")
        time.sleep(0.03)


def close():
    global running

    save_list("")
    running = False

    root.destroy()


# sidebar frame
frame = customtkinter.CTkFrame(root, width=200, corner_radius=0)
frame.grid(row=0, column=0, rowspan=4)
frame.grid_rowconfigure(4, weight=1)



# ROOT TABVIEW
tabview_root = customtkinter.CTkTabview(master=frame, width=300, height=70, command=changed_tabview_root)
tabview_root.pack(pady=10, padx=10)
tabview_root.add("To Do List")
tabview_root.add("Settings")


# To Do List
entry = customtkinter.CTkEntry(master=tabview_root.tab("To Do List"), width=200)
entry.grid(row=0, column=0)

# add button
add_button = customtkinter.CTkButton(master=tabview_root.tab("To Do List"), text="+", command=lambda: add_element("Button"), width=28)
add_button.grid(row=0, column=1, padx=2)

# remove button
remove_button = customtkinter.CTkButton(master=tabview_root.tab("To Do List"), text="-", command=remove_elements, width=28)
remove_button.grid(row=0, column=2)

# setup the list
tasks_frame = None
setup_list(scroll_pos)



# Settings
tabview_settings = customtkinter.CTkTabview(master=tabview_root.tab("Settings"), width=200, height=70)
tabview_settings.pack()
tabview_settings.add("Appearance")
tabview_settings.add("Text")
tabview_settings.add("Key binds")
tabview_settings.add("Credits")


# appearance size label
font_size_label = customtkinter.CTkLabel(tabview_settings.tab("Appearance"), text="Appearance size")
font_size_label.pack(padx=10)

# appearance size
scaling_optionemenu = customtkinter.CTkOptionMenu(tabview_settings.tab("Appearance"), values=["50%", "60%", "70%", "80%", "90%", "100%", "110%", "120%", "130%", "140%", "150%"], command=change_font_size)
scaling_optionemenu.pack(pady=10, padx=10)
scaling_optionemenu.set(settings.get("font_size"))


# appearance mode label
appearance_optionmenu_label = customtkinter.CTkLabel(tabview_settings.tab("Appearance"), text="Appearance mode")
appearance_optionmenu_label.pack(padx=10)

# appearance
appearance_optionmenu = customtkinter.CTkOptionMenu(tabview_settings.tab("Appearance"), values=["Light", "Dark", "System"], command=change_appearance)
appearance_optionmenu.pack(pady=10, padx=10)
appearance_optionmenu.set(settings.get("appearance_mode"))


# text size label
text_size_label = customtkinter.CTkLabel(tabview_settings.tab("Text"), text="Text size " + str(settings.get("text_size")))
text_size_label.pack(padx=10)

# text size
text_size_slider = customtkinter.CTkSlider(master=tabview_settings.tab("Text"), command=change_text_size_font, from_=10, to=50)
text_size_slider.pack(pady=10, padx=10)
text_size_slider.set(settings.get("text_size"))

# text font label
text_font_label = customtkinter.CTkLabel(tabview_settings.tab("Text"), text="Text font")
text_font_label.pack(padx=10)

# text font
text_font_optionemenu = customtkinter.CTkOptionMenu(tabview_settings.tab("Text"), values=["Arial", "Courier", "Helvetica", "Times"], command=change_text_size_font)
text_font_optionemenu.pack(pady=10, padx=10)
text_font_optionemenu.set(settings.get("text_font"))



# key binds
key_binds_textbox = customtkinter.CTkTextbox(master=tabview_settings.tab("Key binds"))
key_binds_textbox.pack()
key_binds_textbox.insert("0.0", "Add an item to the list:\nEnter\n\n"
                                "Save the list:\nControl-s\n\n"
                                "Load the list:\nControl-l\n\n")


# credits
credits_textbox = customtkinter.CTkTextbox(master=tabview_settings.tab("Credits"), font=("Arial", 10), width=250)
credits_textbox.pack()
credits_textbox.insert("0.0", "This Simple To-Do-List is created by Lefpadlog.\n"
                              "You can use it, but please don\'t take the credits\nfor it.\n"
                              "I hope you have fun with it :) \n"
                              "Feel also free to decode it and learn through it\nmore about python.\n\n"
                              "https://www.youtube.com/@lefpadlog5796")

credits_textbox.tag_add("highlight", "1.37", "1.46")
credits_textbox.tag_add("highlight", "8.0", "8.50")
credits_textbox.tag_config("highlight", background="#444444")


threading.Thread(target=update_root_size).start()


# shortcuts
root.bind("<MouseWheel>", scroll)
root.bind("<Return>", add_element)
root.bind("<Control-s>", save_list)
root.bind("<Control-l>", load_list)
root.protocol('WM_DELETE_WINDOW', close)

root.mainloop()
