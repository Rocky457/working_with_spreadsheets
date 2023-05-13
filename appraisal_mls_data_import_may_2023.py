import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg ##
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import numpy as np
import customtkinter
import tkinter as tk
from tkinter import filedialog

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

import math

def get_file_path():
    root = customtkinter.CTk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select CSV file to import",
        filetypes=[('CSV files', ".csv")])

    return file_path

def dom_matplot(window):

    # create a figure and axis object
    fig, ax = plt.subplots()

    # plot the graph and set the axis labels and marker style
    ax.plot(solds_df.MLS_SettledDate, solds_df.DOM, linestyle='', marker='o')
    ax.set_xlabel('MLS Settled Date')
    ax.set_ylabel('DOM')


    # add trendline
    x = np.array(mpl_dates.date2num(solds_df.MLS_SettledDate))
    y = np.array(solds_df.DOM)
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(solds_df.MLS_SettledDate, p(x), "r--")

    # calculate the slope and intercept of the trendline
    x = solds_df.MLS_SettledDate.values.astype('datetime64[s]').astype('int')
    y = solds_df.DOM.values
    m, b = np.polyfit(x, y, 1)

    # calculate the R-squared value
    r = np.corrcoef(x, y)[0, 1]
    r_squared = r ** 2

    # format the x-axis date labels
    date_fmt = mpl_dates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(date_fmt)
    fig.autofmt_xdate()

    # create a FigureCanvasTkAgg object from the figure
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    # add the canvas to the window
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


'''         Here I am working on checking correlations with the data, currently buildings 
            but I don't understand how to call acres correctly

def get_correls(window):
    #solds_df.loc[:, 'MLS_SettledDate'] = solds_df['MLS_SettledDate'].astype(str)

    acres_df.loc[:, 'Acres'] = solds_df['Acres'].astype(str)
    # sorts data by settledate
    solds_df_sorted = solds_df.sort_values('MLS_SoldPrice', ascending=True)
    corr_acres = solds_df_sorted['MLS_SoldPrice'].corr(solds_df_sorted['Acres'])

    # create a label for acres corr
    corr_acres_label = tk.Label(window, text=f"correlation between price and acres: {corr_acres}", bg="black", fg="white")
    corr_acres_label.pack()

'''


def csv_filestats(window):
    # create a label for the number of rows
    num_rows_label = tk.Label(window, text=f"Number of rows: {df.shape[0]}", bg="black", fg="white")
    num_rows_label.pack()

    # create a label for the number of columns
    num_col_label = tk.Label(window, text=f"Number of columns: {df.shape[1]}", bg="black", fg="white")
    num_col_label.pack()

    # create a label for the number of solds
    num_solds = tk.Label(window, text=f"Number of Solds: {solds_df.shape[0]}", bg="black", fg="white")
    num_solds.pack()

    # create a label for the number of actives, pendings and active under contracts
    num_actives = tk.Label(window, text=f"Number of Actives/Pendings: "
                                        f"{active_df.shape[0] + pending_df.shape[0] + active_under_C.shape[0]}", bg="black", fg="white")
    num_actives.pack()




def stop(window):
    window.quit()

def show_data_window(df):
    window = customtkinter.CTk()
    window.title("Data Info")
    window.geometry("600x600")

    # create a button to show the stats of the csv sheet called
    csv_button = customtkinter.CTkButton(window, text="CSV file stats", width= 20, command=lambda: csv_filestats(window))
    csv_button.pack()

    # creates a button to show a graph of dom vs settle date
    dom_button = customtkinter.CTkButton(window, text="DOM graph", width= 20, command=lambda: dom_matplot(window))
    dom_button.pack()

    '''
    # create a button to show the stats of the csv sheet called
    corr_button = customtkinter.CTkButton(window, text="Correlation check", width=20, command=lambda: get_correls(window))
    corr_button.pack()
    '''

    # create a button to end the window
    stop_button = customtkinter.CTkButton(window, text="Close", width= 20, command=lambda: stop(window))
    stop_button.pack()
    #the bit that runs the window
    window.mainloop()

# mls_unfil is the raw data from MLS download
mls_unfil = get_file_path()

# read CSV file into pandas DataFrame
df = pd.read_csv(mls_unfil)

# divide data by status. Most real estate statistics only use sold data, but the active,
# pending and active/pending are useful for forecasting exposure time and 1004D addendum data
solds_df = df[(df.Status == "Closed")]
active_df = df[(df.Status == "Active")]
pending_df = df[(df.Status == "Pending")]
active_under_C = df[(df.Status == "ActiveUnderContract")]

# convert 'MLS_SettledDate' column to string
solds_df.loc[:, 'MLS_SettledDate'] = solds_df['MLS_SettledDate'].astype(str)
# sorts data by settledate
solds_df = solds_df.sort_values('MLS_SettledDate', ascending=True)
# convert MLS_SettledDate column to datetime object
solds_df['MLS_SettledDate'] = pd.to_datetime(df['MLS_SettledDate'])
# create a new column with the month of each MLS_SettledDate
solds_df['SettledMonth'] = solds_df['MLS_SettledDate'].dt.month


while True:
    # call the function to display the data information in a window, passing a copy of the DataFrame
    show_data_window(df.copy())
    break

#close opened file
get_file_path.close
