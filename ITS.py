# %%
from owlready2 import *
onto = get_ontology("Geo.owx").load()


# %%
for individual in onto.Country.instances():
    print(individual.name)

# %%

# Function to load countries into the ontology
def load_countries(countries):
    for country in countries:
        instance = onto.Country(country["name"])
        instance.isPartOf = [asia if country["continent"] == "Asia" else europe]
        
        # Append values to the data properties
        instance.Population.append(country["Population"])
        instance.Area.append(country["Area"])

# Function to load rivers into the ontology
def load_rivers(rivers):
    for river in rivers:
        instance = onto.River(river["name"])
        instance.Length.append(river["Length"])  # Append Length to the data property
        instance.flowsThrough = [onto[country] for country in river["flows_through"]]

# Function to load mountains into the ontology
def load_mountains(mountains):
    for mountain in mountains:
        instance = onto.Mountain(mountain["name"])
        instance.height.append(mountain["Height"])  # Append Height to the data property
        instance.isLocatedIn = [onto[country] for country in mountain["located_in"]]

# Data for countries, rivers, and mountains
countries = [
    {"name": "Russia", "continent": "Asia", "Population": "146599183", "Area": "17098242"},
    {"name": "South Korea", "continent": "Asia", "Population": "51329899", "Area": "100032"},
]

rivers = [
    {"name": "Volga", "Length": "3530", "flows_through": ["Russia"]},
    {"name": "Amur", "Length": "2824", "flows_through": ["Russia", "China"]},
    {"name": "Danube", "Length": "2850", "flows_through": ["Germany"]},
]

mountains = [
    {"name": "K2", "Height": "8611", "located_in": ["China"]},
    {"name": "Kangchenjunga", "Height": "8586", "located_in": ["India"]},
    {"name": "Lhotse", "Height": "8516", "located_in": [ "China"]},
    {"name": "Makalu", "Height": "8485", "located_in": [ "China"]},
 
]

# Create instances of Continents
asia = onto.Continent("Asia")
europe = onto.Continent("Europe")

# Call functions to load data
load_countries(countries)
load_rivers(rivers)
load_mountains(mountains)

# Save the updated ontology
onto.save(file="updated_ontology.owl", format="rdfxml")

# %%
from owlready2 import *
import tkinter as tk
from tkinter import ttk, messagebox

# Load the ontology
onto = get_ontology("updated_ontology.owl").load()

# Function to get countries in a continent
def get_countries(continent):
    results = []
    for country in onto.Country.instances():
        if country.isPartOf and country.isPartOf[0].name == continent:
            results.append(country.name)
    return results

# Function to get rivers or mountains in a country
def get_features(country, feature_type):
    results = []
    for feature in getattr(onto, feature_type).instances():
        if (feature.isLocatedIn and feature.isLocatedIn[0].name == country) or \
           (feature.flowsThrough and feature.flowsThrough[0].name == country):
            results.append(feature.name)
    return results

# Event handlers
def update_countries(event):
    continent = continent_combobox.get()
    if continent:
        countries = get_countries(continent)
        country_combobox['values'] = countries
        country_combobox.set("")
        result_box.delete(1.0, tk.END)

def display_features():
    country = country_combobox.get()
    feature_type = feature_combobox.get()
    if country and feature_type:
        features = get_features(country, feature_type)
        result_box.delete(1.0, tk.END)
        if features:
            result_box.insert(tk.END, f"Features in {country} ({feature_type}):\n")
            result_box.insert(tk.END, "\n".join(features))
        else:
            result_box.insert(tk.END, f"No {feature_type}s found in {country}.")
    else:
        messagebox.showwarning("Input Required", "Please select both a country and a feature type.")

# Create the main application window
app = tk.Tk()
app.title("Geography Tutoring System")
app.geometry("800x600")
app.configure(bg="#F4F6F9")

# Header Frame
header_frame = tk.Frame(app, bg="#3A7DFF", pady=15)
header_frame.pack(fill=tk.X)
header_label = tk.Label(header_frame, text="Geography Tutoring System", font=("Arial", 18, "bold"), fg="white", bg="#3A7DFF")
header_label.pack()

# Main Frame (for dropdowns, button, and results)
main_frame = tk.Frame(app, bg="#F4F6F9")
main_frame.pack(pady=20, padx=30, fill=tk.BOTH)

# Continent Section
continent_label = tk.Label(main_frame, text="Select a Continent:", font=("Arial", 12, "bold"), bg="#F4F6F9")
continent_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
continent_combobox = ttk.Combobox(main_frame, font=("Arial", 12), width=25)
continent_combobox.grid(row=0, column=1, pady=5)
continent_combobox['values'] = [c.name for c in onto.Continent.instances()]  # Populate with Continent names
continent_combobox.bind("<<ComboboxSelected>>", update_countries)

# Country Section
country_label = tk.Label(main_frame, text="Select a Country:", font=("Arial", 12, "bold"), bg="#F4F6F9")
country_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
country_combobox = ttk.Combobox(main_frame, font=("Arial", 12), width=25)
country_combobox.grid(row=1, column=1, pady=5)

# Feature Section
feature_label = tk.Label(main_frame, text="Select a Feature (River/Mountain):", font=("Arial", 12, "bold"), bg="#F4F6F9")
feature_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
feature_combobox = ttk.Combobox(main_frame, values=["River", "Mountain"], font=("Arial", 12), width=25)
feature_combobox.grid(row=2, column=1, pady=5)

# Show Button with Hover Effect
def on_enter_button(event):
    show_button.config(bg="#3A7DFF")

def on_leave_button(event):
    show_button.config(bg="#4CAF50")

show_button = tk.Button(main_frame, text="Show Features", command=display_features, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15)
show_button.grid(row=3, column=1, pady=20)
show_button.bind("<Enter>", on_enter_button)
show_button.bind("<Leave>", on_leave_button)

# Results Section
result_label = tk.Label(app, text="Results:", font=("Arial", 14, "bold"), bg="#F4F6F9")
result_label.pack(pady=5)

result_frame = tk.Frame(app)
result_frame.pack(padx=30)
result_box = tk.Text(result_frame, height=15, width=60, font=("Arial", 12), wrap=tk.WORD, bd=2, relief="solid", bg="#F0F0F0")
result_box.pack(side=tk.LEFT, padx=5, pady=5)
scrollbar = tk.Scrollbar(result_frame, command=result_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_box.config(yscrollcommand=scrollbar.set)

# Run the application
app.mainloop()



