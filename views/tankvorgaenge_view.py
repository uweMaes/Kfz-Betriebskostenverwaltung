import tkinter as tk
from tkinter import ttk
from tkcalendar import *
from database.database import Database
import controllers.tankvorgaenge_controller


class TankvorgaengeView:
    def __init__(self, master):
        self.master = master
        self.master.title("Tankvorgänge")

        tk.Label(self.master, text="Datum:").grid(row=0, column=0)
        self.datum_entry = DateEntry(
            self.master, selectmode="day", date_pattern="yyyy-mm-dd"
        )
        self.datum_entry.grid(row=0, column=1)

        tk.Label(self.master, text="Liter:").grid(row=1, column=0)
        self.liter_entry = tk.Entry(self.master)
        self.liter_entry.grid(row=1, column=1)

        tk.Label(self.master, text="Preis:").grid(row=2, column=0)
        self.preis_entry = tk.Entry(self.master)
        self.preis_entry.grid(row=2, column=1)

        tk.Label(self.master, text="Gefahrene Kilometer:").grid(row=3, column=0)
        self.km_entry = tk.Entry(self.master)
        self.km_entry.grid(row=3, column=1)

        ttk.Button(
            self.master,
            text="Speichern",
            command=lambda: controllers.tankvorgaenge_controller.tankvorgang_speichern(
                self.datum_entry.get_date(),
                self.liter_entry.get(),
                self.preis_entry.get(),
                self.km_entry.get(),
            ),
        ).grid(row=4, column=0, columnspan=2)

        self.statistik_label = ttk.Label(self.master, text="Statistik:")
        self.statistik_label.grid(row=5, column=0, sticky=tk.W)

        self.statistik_text = tk.Text(self.master, width=50, height=5)
        self.statistik_text.grid(row=6, column=0, columnspan=2)

        self.anzeigen_statistik()

    def anzeigen_statistik(self):
        db = Database()
        tankvorgaenge_list = db.get_all_tankvorgaenge()

        if not tankvorgaenge_list:
            self.statistik_text.delete(1.0, tk.END)
            self.statistik_text.insert(tk.END, "Keine Tankvorgänge vorhanden")
            return

        liter_summe = sum(tankvorgang.liter for tankvorgang in tankvorgaenge_list)
        km_summe = sum(tankvorgang.gefahrene_km for tankvorgang in tankvorgaenge_list)
        preis_summe = sum(tankvorgang.preis for tankvorgang in tankvorgaenge_list)

        durchschnittlicher_verbrauch = liter_summe / km_summe if km_summe != 0 else 0
        durchschnittlicher_preis = preis_summe / liter_summe if liter_summe != 0 else 0

        statistik_text = f"Durchschnittlicher Verbrauch: {durchschnittlicher_verbrauch:.2f} Liter/km\n"
        statistik_text += f"Durchschnittlicher Preis pro Liter: {durchschnittlicher_preis:.2f} Euro/Liter"

        self.statistik_text.delete(1.0, tk.END)
        self.statistik_text.insert(tk.END, statistik_text)
