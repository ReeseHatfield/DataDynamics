from tkinter import ttk
import src.app.gui_constants as GUI

from src.app.windows.ForecastingWindow.PredictionWindow import PredictionPanel


class MainWindow:
    def __init__(self, master):
        self.tab_control = None
        self.master = master
        self.master.title("DataDynamics")

        self.master.geometry(f"{GUI.WINDOW_HEIGHT}x{GUI.WINDOW_WIDTH}")

        self.create_tabs()

        # Configure the grid to expand properly when window is resized
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def create_tabs(self):
        self.tab_control = ttk.Notebook(self.master, style=GUI.STYLE)

        self.create_tab("Forecasting")
        self.create_tab("Tab Two")
        self.create_tab("Tab Three")
        self.create_tab("Tab Four")

        self.tab_control.grid(row=0, column=0, sticky='nesw', padx=4, pady=4)

    def create_tab(self, tab_name):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text=tab_name)

        frame = ttk.Frame(tab)
        frame.grid(row=0, column=0, sticky='nesw', padx=16, pady=16)

        # Configure the grid of the tab to expand properly when window is resized
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        label = ttk.Label(frame, text=tab_name, font=GUI.TAB_LABEL_STYLE)
        label.grid(row=0, column=0, sticky='nesw', padx=16, pady=16)

        # Add custom widget to the first tab
        if tab_name == "Forecasting":
            prediction_widget = PredictionPanel(frame)
            prediction_widget.grid(row=1, column=0, sticky='nesw', padx=16, pady=16)
