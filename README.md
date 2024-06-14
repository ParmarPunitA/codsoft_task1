# TODO List Application

This TODO List application is developed as part of an internship assignment at Codsoft. It is built using Python and Tkinter library for the GUI, and incorporates custom widgets for enhanced user interface elements.

## Features

- **Add and Delete TODO Lists**: Add new TODO lists with customizable names and delete existing lists.
- **Manage Tasks**: Each TODO list can contain multiple tasks that can be added, deleted, or marked as complete/incomplete.
- **Edit TODO List Name**: Rename existing TODO lists directly from the interface.
- **Save and Load Data**: Data is automatically saved to a JSON file (`todo-list.json`) upon exit and loaded on startup.

## Technologies Used

- **Python**: Backend logic and scripting.
- **Tkinter**: Python's standard GUI library.
- **PIL (Pillow)**: Python Imaging Library used for image handling.
- **JSON**: Data storage and retrieval.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ParmarPunita/codsoft_task1.git
   cd codsoft_task1
   ```

2. **Installing Dependencies**
   You need to be in parent directory of the codsoft_task1
     - ```cd ..``` (use this to navigate back to parent folder if you are in codsoft_task1)
     - ```python python3 -m venv codsoft_task1``` (make a virtual environment using lastest 3.x python version on your device, use python --version to know the installed version)
     - ```bash (use activate.fish if you are using fish shell)
       source codsoft_task1/bin/activate
       ```
     - ```cd codsoft_task1```
     - ```pip install -r requirements.txt```

3. **Usage**

  ```python3
  python3 -u TODO_List.py```

  
