# VoltEase — Electricity Bill Management System

A Python mini-project with an animated opening screen, consumer meter-reading form, tariff-based energy calculation, bill display, and CSV/text file saving.

## Requirements
- Python 3.10 or newer
- Tkinter (included with most standard Python installations)

No pip packages are required for the main application.

## Run
1. Extract the `VoltEase` folder.
2. Open the folder in VS Code or PyCharm.
3. Run `main.py`, or from a terminal run:

   ```bash
   python main.py
   ```

4. Enter the consumer details and meter readings.
5. Click **Calculate Bill**.
6. Click **Save Bill to File**. The app creates a `bills` folder with `consumer_bills.csv` and individual text bills.

## Academic tariff used
The rates are examples from the supplied project poster, not official tariff guidance. The code uses progressive slabs:
- First 100 units: ₹2/unit
- Next 100 units: ₹3/unit
- Next 100 units: ₹5/unit
- Above 300 units: ₹7/unit

Fixed charge: ₹75. Other charges: ₹25. Edit these constants in `main.py` if your instructor specifies different values.

## Example
Previous reading = 1250, current reading = 1400
- Units consumed = 150
- Energy charges = (100 × ₹2) + (50 × ₹3) = ₹350
- Fixed charges = ₹75
- Other charges = ₹25
- Total = ₹450

The sample poster shows ₹450 energy charges for 150 units, which applies ₹3 to all 150 units rather than progressive slabs. Confirm with your instructor which interpretation is expected. To use a single rate based on the slab, replace `calculate_energy_charge()` with the alternative described in the project notes.

## Suggested next improvements
- Search and view saved bills
- Edit/delete consumer records
- Add charts with Matplotlib
- Export a PDF bill
- Add unit tests
"# VoltEase" 
