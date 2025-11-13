import os
import tkinter as tk
from tkinter import filedialog, messagebox

# --- DEEL 1: De Logica (Nu onderdeel van de klasse) ---

class ProjectCreatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Project Mappen Creator")
        
        # Variabelen voor opslag pad en projectnaam
        self.basis_locatie = tk.StringVar(value="Nog geen locatie geselecteerd")
        self.project_naam_var = tk.StringVar()

        # GUI Elementen aanmaken
        self._create_widgets()

    def _create_widgets(self):
        # 1. Projectnaam Invoer
        tk.Label(self.master, text="Projectnaam:").pack(pady=(10, 0))
        self.entry_naam = tk.Entry(self.master, textvariable=self.project_naam_var, width=50)
        self.entry_naam.pack(padx=10)
        self.entry_naam.focus_set()

        # 2. Locatie Selectie
        tk.Label(self.master, text="Basislocatie:").pack(pady=(10, 0))
        
        self.label_locatie = tk.Label(self.master, textvariable=self.basis_locatie, wraplength=380, fg="gray")
        self.label_locatie.pack(padx=10)

        self.btn_selecteer_map = tk.Button(self.master, text="Selecteer Locatie...", command=self.selecteer_map)
        self.btn_selecteer_map.pack(pady=5)

        # 3. Project Aanmaken Knop
        self.btn_creeeren = tk.Button(self.master, text="Creëer Mappenstructuur", command=self.creeër_project, bg="green", fg="white", state=tk.DISABLED)
        self.btn_creeeren.pack(pady=20, ipadx=10, ipady=5)

        # 4. Status/Log Veld
        tk.Label(self.master, text="--- Status ---").pack()
        self.log_text = tk.Text(self.master, height=8, width=50, state=tk.DISABLED, bg="lightgray")
        self.log_text.pack(padx=10, pady=(0, 10))
        
        # Binden van de invoer aan een controlefunctie
        self.project_naam_var.trace_add("write", self._check_inputs)

    def _log_message(self, message, level="info"):
        """Voegt een bericht toe aan het log-veld in de GUI."""
        self.log_text.config(state=tk.NORMAL)
        
        if level == "error":
            tag = "error_tag"
            self.log_text.tag_config(tag, foreground="red")
        elif level == "success":
            tag = "success_tag"
            self.log_text.tag_config(tag, foreground="green")
        else:
            tag = "info_tag"
            self.log_text.tag_config(tag, foreground="black")

        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END) # Scroll naar beneden
        self.log_text.config(state=tk.DISABLED)

    def _check_inputs(self, *args):
        """Controleert of projectnaam is ingevoerd en locatie is geselecteerd."""
        naam_ingevoerd = self.project_naam_var.get().strip()
        locatie_geselecteerd = not self.basis_locatie.get().startswith("Nog geen")
        
        if naam_ingevoerd and locatie_geselecteerd:
            self.btn_creeeren.config(state=tk.NORMAL, bg="blue")
        else:
            self.btn_creeeren.config(state=tk.DISABLED, bg="green") # Terug naar de oorspronkelijke kleur

    def selecteer_map(self):
        """Opent een dialoogvenster om de basislocatie te selecteren."""
        nieuwe_locatie = filedialog.askdirectory(
            title="Selecteer de MAP WAARIN het nieuwe project moet komen",
            initialdir=os.path.expanduser("~") 
        )
        
        if nieuwe_locatie:
            self.basis_locatie.set(os.path.normpath(nieuwe_locatie))
            self._log_message(f"Locatie geselecteerd: {os.path.basename(nieuwe_locatie)}", "info")
        else:
            self._log_message("Locatie selectie geannuleerd.", "info")
            
        self._check_inputs()

    def creeër_project(self):
        """Valideert de invoer en start het aanmaken van de mappen."""
        project_naam = self.project_naam_var.get().strip()
        basis_pad = self.basis_locatie.get()

        if not project_naam:
            messagebox.showerror("Fout", "Voer een geldige projectnaam in.")
            return

        if basis_pad.startswith("Nog geen"):
            messagebox.showerror("Fout", "Selecteer eerst een basislocatie.")
            return

        volledig_project_pad = os.path.join(basis_pad, project_naam)
        
        # Log het begin en wis oude log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self._log_message(f"--- Starten met het aanmaken van project: {project_naam} ---", "info")
        
        # Roep de logica aan
        self._create_project_folders(volledig_project_pad)
        
        messagebox.showinfo("Voltooid", f"Mappenstructuur aangemaakt op:\n{volledig_project_pad}")

    def _create_project_folders(self, base_path):
        """Maakt een vaste mappenstructuur aan op de opgegeven basislocatie."""
        folder_structure = [
            "01_Footage",
            "02_Project",
            "03_Audio",
            "04_Export"
        ]

        for folder_name in folder_structure:
            full_path = os.path.join(base_path, folder_name)

            try:
                os.makedirs(full_path, exist_ok=True)
                self._log_message(f"✅ Map aangemaakt (of bestond al): {folder_name}", "success")
            except Exception as e:
                self._log_message(f"❌ Fout bij het aanmaken van map {folder_name}: {e}", "error")

        self._log_message("--- Mappenstructuur compleet! ---", "info")


if __name__ == "__main__":
    # Hoofdvenster instellen
    root = tk.Tk()
    app = ProjectCreatorApp(root)
    # Start de hoofdloop van de applicatie
    root.mainloop()