import tkinter as tk
from scraper_test import scrape_system
from company_scraper import get_companies
# Create the main window
window = tk.Tk()
window.title("השגת מידע")

# Create a button and associate it with the function
label = tk.Label(window, text="")

def button_clicked():
    # Pass the argument here
    get_companies()
    scrape_system(label)
    label.config(text="Done!")




button = tk.Button(window, text="Run", command=button_clicked ,width='20', height='7')



# Pack the button into the window
button.pack()
label.pack()

# Start the Tkinter event loop
window.mainloop()
