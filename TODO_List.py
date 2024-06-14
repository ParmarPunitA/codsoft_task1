import customtkinter as ctk
from tkinter import *
from functools import partial
import json
from PIL import Image


todos = {}  
    
def load_todos():
    try:
        with open("todo-list.json","r") as f:
            json_data = f.read()
            todos.update(json.loads(json_data))
    except FileNotFoundError:
        print("File not found")

def todo_list_display():
    for widget in todo_display_frame.winfo_children():
        widget.grid_remove()
    i=0
    for key in todos.keys():
        todo = ctk.CTkButton(todo_display_frame,text=key,fg_color="white",bg_color="white",width=100,text_color="black",compound="left",border_color="lightgrey",corner_radius=10,font=("jetbrainMono",22),hover_color="lightgrey",command=partial(selected_todo, key))
        todo.grid(row=(i+1),column=0,sticky="nsw",columnspan=1,pady=3)
        
        delete_todo_button = ctk.CTkButton(todo_display_frame,image=delete_img,fg_color="white",bg_color="white",corner_radius=10,text="",height=15,width=10,border_color="white",border_width=1,hover_color="lightgrey",command=partial(delete_todo_list,key))
        delete_todo_button.grid(row=(i+1),column=1,sticky="nswe",padx=2,pady=3,columnspan=1,ipadx=2,ipady=2,)
        i+=1

def add_todo_list():

    value = add_todo_entry.get()
    if value == "":
        return
    todos[value] = {}
    
    new_todo = ctk.CTkButton(todo_display_frame,text=f"{value}",fg_color="white",width=100,bg_color="white",text_color="black",corner_radius=10,font=("jetbrainMono",22),hover_color="lightgrey",command=lambda: selected_todo(value))
    new_todo.grid(row=f"{len(todos)+1}",column=0,sticky="nws",pady=3,columnspan=1)
    
    delete_todo_button = ctk.CTkButton(todo_display_frame,image=delete_img,fg_color="white",bg_color="white",corner_radius=10,text="",height=15,width=15,hover_color="lightgrey",command=partial(delete_todo_list,value))
    delete_todo_button.grid(row=f"{len(todos)+1}",column=1,sticky="nswe",padx=5,pady=3,columnspan=1,)
    
    add_todo_entry.delete(0,END)

def clear_tasks():
    editlabel.configure(state="disable", text="")
    editbutton.configure(state="disable", text="")
    save_name.configure(state="disable", text="")
    new_task_entry.configure(state="disable", placeholder_text="")
    new_task_button.configure(state="disable", text="")
    for widget in task_frame.winfo_children():
        widget.grid_remove()

def delete_todo_list(todo_list_name):
    if editlabel.cget("text") == todo_list_name:
        clear_tasks()
        if hasattr(task_frame, 'new_task_entry'):
            new_task_entry.grid_remove()
            new_task_button.grid_remove()
            del task_frame.new_task_entry
            del task_frame.new_task_button
    todos.pop(todo_list_name)
    todo_list_display()

def selected_todo(todo_list_name):
    
    global editbutton, todo_description_frame, new_task_entry, new_task_button
    
    if hasattr(todo_description_frame,'task_frame'):
        clear_tasks()

    editbutton.configure(state="normal", text="EDIT", command=lambda: edit_todo_list_name(todo_list_name))
    save_name.configure(state="disable", text="SAVE")
    if todo_description_frame.winfo_children():
        for widget in todo_description_frame.winfo_children():
            if isinstance(widget, ctk.CTkEntry) and widget == 'testentry':
                widget.grid_remove()

    editlabel.configure(state="normal", text=f"{todo_list_name}")
    
    
    if not hasattr(task_frame, 'new_task_entry'):
        new_task_entry = ctk.CTkEntry(todo_description_frame, placeholder_text="Add Task", placeholder_text_color="lightgrey", height=15, width=180, border_width=2, border_color="black", text_color="black", font=("JetbrainMono", 20), fg_color="white", bg_color="white")
        new_task_entry.grid(row=4, column=0, sticky="nswe", padx=7, ipadx=2, ipady=2, pady=10, columnspan=1)
        task_frame.new_task_entry = new_task_entry

        new_task_button = ctk.CTkButton(todo_description_frame, height=15, width=5, text="ADD", fg_color="white", text_color="grey", font=("jetbrainMono", 14), hover_color="#e0dcdc", border_width=2, border_color="black", corner_radius=10, command=lambda: add_task())
        new_task_button.grid(row=4, column=1, ipadx=2, ipady=2, sticky="nswe", padx=5, pady=10, columnspan=2)
        task_frame.new_task_button = new_task_button
    task_display(todo_list_name)

    if hasattr(todo_description_frame, 'testentry'):
        todo_description_frame.testentry.grid_remove()
    editlabel.configure(state="normal", text=todo_list_name)  
    
def edit_todo_list_name(value):
    editlabel.configure(state="disable")
    global testentry
    testentry = ctk.CTkEntry(todo_description_frame,placeholder_text="enter new name",placeholder_text_color="lightgrey",height=15,width=180,border_width=1,border_color="black",text_color="black",font=("jetbrianMono",20),fg_color="white",bg_color="white",)
    testentry.grid(rowspan=1,columnspan=1,row=0,column=0,sticky="nswe",padx=5,ipadx=5,pady=10)

    save_name.configure(state="normal",command=lambda:save_todo_list_name(value,testentry.get()))

def save_todo_list_name(old_todo_list_name,new_todo_list_name):
    if new_todo_list_name == "":
        return
    testentry.grid_remove()
    editlabel.configure(state="normal",text=f"{new_todo_list_name}")
    todos[new_todo_list_name] = todos.pop(old_todo_list_name)
    todo_list_display()
    testentry.delete(0,END)
    testentry.configure(state="disable")
    save_name.configure(state="disable")
    
def add_task():
    entry_value = new_task_entry.get()
    if entry_value == "":
        return
    selected_todo = editlabel.cget("text")
    todos[selected_todo][entry_value] = False
    new_task_entry.delete(0, END)

    var = ctk.BooleanVar(value=todos[selected_todo][entry_value])
    new_checkbox = ctk.CTkCheckBox(task_frame, text=entry_value, fg_color="white", bg_color="white", text_color="black", border_color="black", corner_radius=2, border_width=2, font=("JetbrainMono", 22), hover_color="lightgrey", checkmark_color="black", variable=var, onvalue=True, offvalue=False, command=lambda: update_task_value(selected_todo, entry_value, var.get()))
    new_checkbox.grid(row=(f"{len(todos[selected_todo])+1}"), column=0, sticky="nsew", padx=35, pady=3, ipadx=5)

    delete_todo_button = ctk.CTkButton(task_frame, image=delete_img, fg_color="white", bg_color="white", corner_radius=10, text="", height=15, width=15, border_color="white", border_width=1, hover_color="lightgrey", command=lambda: delete_task(entry_value))
    delete_todo_button.grid(row=(f"{len(todos[selected_todo])+1}"), column=1, sticky="nswe", padx=2, pady=3, columnspan=1, ipadx=2, ipady=2)

def delete_task(task_name):
    
    todos[editlabel.cget("text")].pop(task_name)
    if task_frame.winfo_children():
        for widget in task_frame.winfo_children():
            widget.grid_remove()
    task_display(editlabel.cget("text"))
    
    
def task_display(todo_list_name):
    if task_frame.winfo_children():
        for widget in task_frame.winfo_children():
            widget.grid_remove()

    global new_task_entry, new_task_button
    index = 0
    for key in todos[todo_list_name].keys():
        var = ctk.BooleanVar(value=(todos[todo_list_name][key] == "completed"))
        task_checkbox = ctk.CTkCheckBox(task_frame, text=key, fg_color="white", bg_color="white", text_color="black", border_color="black", corner_radius=2, border_width=2, font=("JetbrainMono", 22), hover_color="lightgrey", checkmark_color="black", variable=var, onvalue=True, offvalue=False, command=lambda v=var, k=key: update_task_value(todo_list_name, k, v.get()))
        task_checkbox.grid(row=(index+1), column=0, sticky="nsw", padx=35, pady=3, ipadx=5)

        delete_todo_button = ctk.CTkButton(task_frame, image=delete_img, fg_color="white", bg_color="white", corner_radius=10, text="", height=15, width=15, border_color="white", border_width=1, hover_color="lightgrey", command=partial(delete_task, key))
        delete_todo_button.grid(row=(index+1), column=1, sticky="nswe", padx=2, pady=3, columnspan=1, ipadx=2, ipady=2)

        index += 1

    if hasattr(task_frame, 'new_task_entry'):
        new_task_entry.grid(row=4, column=0, sticky="nswe", padx=7, ipadx=2, ipady=2, pady=10, columnspan=1)
        new_task_button.grid(row=4, column=1, ipadx=2, ipady=2, sticky="nswe", padx=5, pady=10, columnspan=2)


def update_task_value(todo_list_name, task_name, new_value):
    todos[todo_list_name][task_name] = "completed" if new_value else "incomplete"
    
def on_closing():
    try:
        json_data = json.dumps(todos)
        with open("todo-list.json", "w") as file:
            file.write(json_data)
    except FileNotFoundError:
        print("File not found")
    
    # left_pane_frame.grid_forget()
    # task_frame.grid_forget()
    # todo_description_frame.destroy()
    app.destroy()

load_todos()


# ROOT APP WINDOW #
ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.resizable(0,0)
width = 1025
height = 850
app.title("TODO List")
app.geometry(f"{width}x{height}")
                                    
app.grid_propagate(FALSE)

app.grid_columnconfigure(0,weight=20,)
app.grid_columnconfigure(1,weight=80,)

app.grid_rowconfigure(0,weight=1)

# LEFT PANE FRAME #

left_pane_frame = ctk.CTkFrame(app,fg_color="white",width=342,height=height,border_width=2,corner_radius=15,border_color="white")

left_pane_frame.grid_propagate(FALSE)

left_pane_frame.grid(row=0,column=0,sticky="nsw",ipadx=5,ipady=5,padx=2,pady=5,)
left_pane_frame.grid_columnconfigure(0,weight=1)
left_pane_frame.grid_columnconfigure(1,weight=1)

left_pane_frame.grid_rowconfigure(0,weight=1)
left_pane_frame.grid_rowconfigure(1,weight=90)
left_pane_frame.grid_rowconfigure(2,weight=2)

# LEFT PANE TO-DO LIST DISPLAY FRAME #

todo_display_frame = ctk.CTkScrollableFrame(left_pane_frame,fg_color="white")
todo_display_frame.grid(row=1,column=0,sticky="nwes",columnspan=2,ipadx=5,ipady=5,padx=5,pady=10)
todo_display_frame.grid_columnconfigure(0,weight=85)
todo_display_frame.grid_columnconfigure(1,weight=5)

label_todo = ctk.CTkLabel(left_pane_frame,fg_color="lightgrey",height=26,text="TO DO List",text_color="black",font=("jetbrainMono",26),corner_radius=10)
label_todo.grid(columnspan=2,row=0,column=0,sticky="new",padx=5,pady=10)


delete_img = ctk.CTkImage(light_image=Image.open("trash-can-regular.png"),dark_image=Image.open("trash-can-regular.png"),)
todo_list_display()

add_todo_entry = ctk.CTkEntry(left_pane_frame,width=250,height=15,fg_color="white",bg_color="white",text_color="black",font=("jetbrainMono",14),placeholder_text="Add TODO",placeholder_text_color="grey",border_width=2,border_color="black",corner_radius=10,)

add_todo_button = ctk.CTkButton(left_pane_frame,height=15,width=5,text="ADD",fg_color="white",text_color="grey",font=("jetbrainMono",14),hover_color="#e0dcdc",border_width=2,border_color="black",corner_radius=20,command=add_todo_list,)

add_todo_entry.grid(row=3,column=0,ipadx=2,ipady=5,sticky="nsew",padx=5,pady=10)
add_todo_button.grid(row=3,column=1,ipadx=2,ipady=5,sticky="nw",padx=5,pady=10)

# RIGHT PANE FRAME #
corner_color = "#28282B"
todo_description_frame = ctk.CTkFrame(app,fg_color="white",width=682,height=height,bg_color="white",border_color="white",corner_radius=15,border_width=2,background_corner_colors=[corner_color,corner_color,corner_color,corner_color])

todo_description_frame.grid_propagate(FALSE)
todo_description_frame.grid(row=0,column=1,sticky="nsew",ipady=13,ipadx=2,padx=5,pady=5,)

todo_description_frame.grid_columnconfigure(0,weight=94)
todo_description_frame.grid_columnconfigure((1,2),weight=6)

todo_description_frame.grid_rowconfigure(0,weight=1)
todo_description_frame.grid_rowconfigure(1,weight=1)
todo_description_frame.grid_rowconfigure(2,weight=80)
todo_description_frame.grid_rowconfigure(3,weight=2)

editlabel = ctk.CTkLabel(todo_description_frame,fg_color="white",text="",text_color="black",text_color_disabled="white",font=("jetbrainMono",24),bg_color="white",height=15)
editlabel.grid(row=0,column=0,columnspan=1,sticky="nsw",padx=35,pady=10,ipadx=5)

editbutton = ctk.CTkButton(todo_description_frame,text="",fg_color="white",bg_color="white",text_color="black",text_color_disabled="white",font=("jetbrainMono",12),hover_color="#e0dcdc",state="disable",width=15)
editbutton.grid(row=0,column=1,sticky="wns",padx=5,pady=10,ipady=1,ipadx=2,)

underline_frame = ctk.CTkFrame(todo_description_frame,fg_color="black",height=0,border_width=1,bg_color="white")
underline_frame.grid(row=1,column=0,columnspan=3,sticky="new",padx=3,)

save_name = ctk.CTkButton(todo_description_frame,text="",fg_color="white",text_color="black",text_color_disabled="white",font=("jetbrainMono",12),hover_color="#e0dcdc",state="disable",width=15)
save_name.grid(row=0,column=2,sticky="wns",pady=10,ipady=1,)

task_frame = ctk.CTkScrollableFrame(todo_description_frame,fg_color="white",bg_color="white")
task_frame.grid(row=2,column=0,sticky="nsew",columnspan=3,padx=5,ipadx=5,ipady=5,pady=10,)
task_frame.grid_columnconfigure(0,weight=96)
task_frame.grid_columnconfigure(1,weight=2)

task_frame.grid_rowconfigure(0,weight=1)

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()