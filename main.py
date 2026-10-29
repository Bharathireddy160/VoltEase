import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os

APP_NAME = "VoltEase"
FIXED_CHARGE = 75.00
OTHER_CHARGES = 25.00

# Educational rates only; not an official electricity tariff.
# Progressive slabs: each rate applies only to units within that range.
TARIFF_SLABS = [
    (100, 2.00),
    (100, 3.00),
    (100, 5.00),
    (float("inf"), 7.00),
]

DATA_DIR = "bills"
CSV_FILE = os.path.join(DATA_DIR, "consumer_bills.csv")


def calculate_energy_charge(units):
    remaining = units
    total = 0.0
    breakdown = []
    lower = 0

    for slab_size, rate in TARIFF_SLABS:
        if remaining <= 0:
            break
        slab_units = min(remaining, slab_size)
        charge = slab_units * rate
        total += charge
        upper = "above" if slab_size == float("inf") else str(lower + slab_size)
        breakdown.append((slab_units, rate, charge))
        remaining -= slab_units
        if slab_size != float("inf"):
            lower += slab_size

    return total, breakdown


def ensure_csv():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Date", "Consumer Number", "Consumer Name",
                "Previous Reading", "Current Reading", "Units",
                "Energy Charges", "Fixed Charges", "Other Charges", "Total"
            ])


class VoltEaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VoltEase | Electricity Bill Management")
        self.root.geometry("1000x700")
        self.root.minsize(850, 620)
        self.root.configure(bg="#f4f7fb")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=9)
        self.style.configure("TLabel", font=("Segoe UI", 10), background="#f4f7fb")
        self.style.configure("Header.TLabel", font=("Segoe UI", 22, "bold"),
                             foreground="#ffffff", background="#102b55")
        self.style.configure("Section.TLabel", font=("Segoe UI", 13, "bold"),
                             foreground="#102b55", background="#f4f7fb")
        self.style.configure("TEntry", padding=7)
        self.show_intro()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_intro(self):
        self.clear()
        self.root.configure(bg="#081a38")
        canvas = tk.Canvas(self.root, bg="#081a38", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        canvas.create_oval(70, 80, 230, 240, fill="#123c70", outline="")
        bulb = canvas.create_oval(115, 105, 185, 175, fill="#ffd447", outline="#fff0a6", width=3)
        canvas.create_rectangle(132, 170, 168, 187, fill="#d6e1f0", outline="")
        canvas.create_rectangle(138, 187, 162, 195, fill="#aebdd1", outline="")
        for x1, y1, x2, y2 in [(150, 70, 150, 48), (92, 104, 75, 91),
                                (208, 104, 225, 91), (89, 170, 67, 170),
                                (211, 170, 233, 170)]:
            canvas.create_line(x1, y1, x2, y2, fill="#ffd447", width=4, capstyle=tk.ROUND)

        title = canvas.create_text(530, 155, text="VoltEase", fill="#ffffff",
                                   font=("Segoe UI", 42, "bold"))
        subtitle = canvas.create_text(530, 210, text="ELECTRICITY BILL MANAGEMENT SYSTEM",
                                      fill="#ffd447", font=("Segoe UI", 15, "bold"))
        description = canvas.create_text(
            530, 260, text="Simple. Accurate. Efficient.",
            fill="#d9e6ff", font=("Segoe UI", 13)
        )
        progress_bg = canvas.create_rectangle(300, 330, 760, 342, fill="#19365f", outline="")
        progress = canvas.create_rectangle(300, 330, 300, 342, fill="#ffd447", outline="")
        hint = canvas.create_text(530, 370, text="Preparing your workspace...",
                                  fill="#c7d7f2", font=("Segoe UI", 10))
        self.root.update_idletasks()

        def animate(step=0):
            if not canvas.winfo_exists():
                return
            width = min(460, step * 8)
            canvas.coords(progress, 300, 330, 300 + width, 342)
            # Gentle pulsing glow around the bulb.
            color = "#ffd447" if step % 2 == 0 else "#ffe88a"
            canvas.itemconfig(bulb, fill=color)
            if step < 58:
                self.root.after(35, lambda: animate(step + 1))
            else:
                self.root.after(350, self.show_dashboard)

        self.root.after(250, animate)

    def show_dashboard(self):
        self.clear()
        self.root.configure(bg="#f4f7fb")

        header = tk.Frame(self.root, bg="#102b55", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="⚡ VoltEase", font=("Segoe UI", 24, "bold"),
                 fg="#ffffff", bg="#102b55").pack(side="left", padx=28, pady=20)
        tk.Label(header, text="ELECTRICITY BILL MANAGEMENT", font=("Segoe UI", 11, "bold"),
                 fg="#ffd447", bg="#102b55").pack(side="right", padx=28)

        body = tk.Frame(self.root, bg="#f4f7fb", padx=26, pady=20)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="Generate Consumer Bill", font=("Segoe UI", 20, "bold"),
                 fg="#102b55", bg="#f4f7fb").pack(anchor="w")
        tk.Label(body, text="Enter consumer details and meter readings to calculate the bill.",
                 font=("Segoe UI", 10), fg="#5b6880", bg="#f4f7fb").pack(anchor="w", pady=(4, 16))

        columns = tk.Frame(body, bg="#f4f7fb")
        columns.pack(fill="both", expand=True)
        form = tk.LabelFrame(columns, text=" Consumer Details ", font=("Segoe UI", 11, "bold"),
                             bg="#ffffff", fg="#102b55", padx=18, pady=18)
        form.pack(side="left", fill="y", padx=(0, 16))
        result_frame = tk.LabelFrame(columns, text=" Bill Summary ", font=("Segoe UI", 11, "bold"),
                                     bg="#ffffff", fg="#102b55", padx=18, pady=18)
        result_frame.pack(side="left", fill="both", expand=True)

        self.entries = {}
        fields = [
            ("Consumer Number", "consumer_no"),
            ("Consumer Name", "consumer_name"),
            ("Previous Reading", "previous"),
            ("Current Reading", "current"),
        ]
        for row, (label, key) in enumerate(fields):
            tk.Label(form, text=label, bg="#ffffff", fg="#29364d",
                     font=("Segoe UI", 10, "bold")).grid(row=row*2, column=0, sticky="w", pady=(7, 3))
            entry = ttk.Entry(form, width=30)
            entry.grid(row=row*2+1, column=0, sticky="ew", pady=(0, 5))
            self.entries[key] = entry

        self.entries["consumer_no"].insert(0, "10023456")
        self.entries["consumer_name"].insert(0, "Ravi Kumar")
        self.entries["previous"].insert(0, "1250")
        self.entries["current"].insert(0, "1400")

        button_row = tk.Frame(form, bg="#ffffff")
        button_row.grid(row=8, column=0, sticky="ew", pady=(16, 0))
        ttk.Button(button_row, text="Calculate Bill", command=self.calculate).pack(fill="x", pady=4)
        ttk.Button(button_row, text="Save Bill to File", command=self.save_bill).pack(fill="x", pady=4)
        ttk.Button(button_row, text="Clear Form", command=self.clear_form).pack(fill="x", pady=4)

        self.result = tk.Text(result_frame, height=19, wrap="word", font=("Consolas", 10),
                              bg="#f8fbff", fg="#17243b", relief="flat", padx=12, pady=12)
        self.result.pack(fill="both", expand=True)
        self.result.insert("1.0", "Your bill will appear here after you click Calculate Bill.")
        self.result.configure(state="disabled")

        footer = tk.Label(body,
            text="Educational project tariff only — verify official AP tariff rules before real-world use.",
            bg="#f4f7fb", fg="#7b4b00", font=("Segoe UI", 9, "italic"))
        footer.pack(anchor="w", pady=(12, 0))
        self.last_bill = None

    def calculate(self):
        consumer_no = self.entries["consumer_no"].get().strip()
        consumer_name = self.entries["consumer_name"].get().strip()
        if not consumer_no or not consumer_name:
            messagebox.showerror("Missing details", "Please enter consumer number and consumer name.")
            return
        try:
            previous = float(self.entries["previous"].get().strip())
            current = float(self.entries["current"].get().strip())
            if previous < 0 or current < 0:
                raise ValueError
            if current < previous:
                messagebox.showerror("Invalid readings",
                                     "Current reading cannot be less than previous reading.")
                return
        except ValueError:
            messagebox.showerror("Invalid input", "Enter valid non-negative numeric meter readings.")
            return

        units = current - previous
        energy, breakdown = calculate_energy_charge(units)
        total = energy + FIXED_CHARGE + OTHER_CHARGES
        bill = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "consumer_no": consumer_no,
            "consumer_name": consumer_name,
            "previous": previous,
            "current": current,
            "units": units,
            "energy": energy,
            "fixed": FIXED_CHARGE,
            "other": OTHER_CHARGES,
            "total": total,
            "breakdown": breakdown,
        }
        self.last_bill = bill

        lines = [
            "=" * 43,
            "       VOLTEASE ELECTRICITY BILL",
            "=" * 43,
            f"Date             : {bill['date']}",
            f"Consumer Number  : {consumer_no}",
            f"Consumer Name    : {consumer_name}",
            f"Previous Reading : {previous:g}",
            f"Current Reading  : {current:g}",
            f"Units Consumed   : {units:g} kWh",
            "-" * 43,
            "ENERGY CHARGE BREAKDOWN",
        ]
        for index, (slab_units, rate, charge) in enumerate(breakdown, start=1):
            lines.append(f"Slab {index}: {slab_units:g} units x Rs.{rate:.2f} = Rs.{charge:.2f}")
        lines += [
            "-" * 43,
            f"Energy Charges   : Rs. {energy:.2f}",
            f"Fixed Charges    : Rs. {FIXED_CHARGE:.2f}",
            f"Other Charges    : Rs. {OTHER_CHARGES:.2f}",
            "=" * 43,
            f"TOTAL BILL       : Rs. {total:.2f}",
            "=" * 43,
            "",
            "Note: Academic demonstration rates only."
        ]
        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("1.0", "\n".join(lines))
        self.result.configure(state="disabled")

    def save_bill(self):
        if not self.last_bill:
            messagebox.showwarning("No bill", "Please calculate the bill before saving.")
            return
        ensure_csv()
        b = self.last_bill
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                b["date"], b["consumer_no"], b["consumer_name"],
                b["previous"], b["current"], b["units"], f"{b['energy']:.2f}",
                f"{b['fixed']:.2f}", f"{b['other']:.2f}", f"{b['total']:.2f}"
            ])

        safe_no = "".join(ch for ch in b["consumer_no"] if ch.isalnum() or ch in "-_")
        text_path = os.path.join(DATA_DIR, f"bill_{safe_no}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(text_path, "w", encoding="utf-8") as file:
            file.write(self.result.get("1.0", "end").strip() + "\n")
        messagebox.showinfo("Bill saved", f"Bill saved successfully.\n\nCSV history: {CSV_FILE}\nText bill: {text_path}")

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.last_bill = None
        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("1.0", "Form cleared. Enter details and calculate a new bill.")
        self.result.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = VoltEaseApp(root)
    root.mainloop()
