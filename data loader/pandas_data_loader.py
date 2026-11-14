import ipywidgets as widgets
from IPython.display import display
import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd

def create_file_picker():
    """
    Creates and displayes files on jupyter notebookd using pandas, tkinter, and ipywidgets
    supports csv, xls, spss, json, parquet, and isv files
    """
    #button to open file explorer
    browse_button = widgets.Button(
    description = "Browse files",
    button_style = "primary",
    icon = "folder-open"
    )
    output_area = widgets.Output()
    
    def on_browse_clicked(b):
        with output_area:
            output_area.clear_output()
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            path = filedialog.askopenfilename(
                title = "Select dataset",
                filetypes = [
                ("All Supported Formats", "*.csv;*.xlsx;*.xls;*.json;*.parquet;*.tsv;*.txt"), 
                ("CSV Files", "*.csv"), 
                ("Excel Files", "*.xlsx;*.xls"), 
                ("JSON Files", "*.json"), 
                ("Parquet Files", "*.parquet"), 
                ("Tab-Separated / Text", "*.tsv;*.txt"), 
                ("SPSS Files", "*.sav;*.por")
                #("All Files", "*.*")
                ]
            )
            if path:
                try:
                    global data
                    ext = os.path.splitext(path)[1].lower()
                    # Dynamically select Pandas reader based on file extension
                    if ext == ".csv":
                        data = pd.read_csv(path)
                    elif ext in [".xlsx", ".xls"]:
                        data = pd.read_excel(path)
                    elif ext == ".json":
                        data = pd.read_json(path)
                    elif ext == ".parquet":
                        data = pd.read_parquet(path)
                    elif ext in [".tsv", ".txt"]:
                        data = pd.read_csv(path, sep="\t")
                    elif ext in [".sav", ".por"]:
                        data = pd.read_spss(path)
                    else:
                        # Fallback to CSV if unknown
                        return("File type not supported!")

                    import sys
                    main_module = sys.modules['__main__']
                    setattr(main_module, 'data', data )

                    print(f"Successfully loaded {os.path.basename(path)}")
                    print(f"Dataset shape: {data.shape}")
                    #print(f"Dataset info: {data.info()}")
                    display(data.head(5))
                
                except Exception as e:
                    print(f"Error loading file: {e}")
            else:
                print("No files selected.")

    browse_button.on_click(on_browse_clicked)

    display(widgets.VBox([browse_button, output_area]))
