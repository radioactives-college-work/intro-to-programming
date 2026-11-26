"""
Kestrel Vale Vets: Appointment Attendance Analytics (teacher model prototype).

This follows the model algorithm designs in the teacher guide. It reads
Task3_data.csv, lets the user choose an appointment type and shows attendance
trends and missed appointments over the three weeks of data. It exists so the
model answers can be checked by running them. Students are NOT asked to write
code in this task.
"""
import csv
from collections import Counter
from datetime import datetime

REQUIRED_COLUMNS = ["Date", "AppointmentType", "Slots", "Booked", "Attended"]
TREND_LIMIT = 5  # percent change needed before a trend is called rising or falling


def load_data(path):
    """Read the CSV, validate every row and tidy the appointment type names.

    Args:
        path (str): location of the CSV file.

    Returns:
        tuple: (records, problems) where records is a list of dicts with the
        keys date, kind, slots, booked, attended (None when missing) and
        problems is a list of text notes about rows that were rejected or
        have missing values.
    """
    records, problems, spellings = [], [], Counter()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValueError("Unexpected columns: " + str(reader.fieldnames))
        for line_no, row in enumerate(reader, start=2):
            name = row["AppointmentType"].strip()
            try:
                day = datetime.strptime(row["Date"].strip(), "%Y-%m-%d").date()
                slots = int(row["Slots"])
                booked = int(row["Booked"])
                attended = None if row["Attended"].strip() == "" else int(row["Attended"])
            except ValueError:
                problems.append(f"Line {line_no}: rejected, a value could not be read")
                continue
            if slots <= 0 or not 0 <= booked <= slots:
                problems.append(f"Line {line_no}: rejected, booked is outside 0 to slots")
                continue
            if attended is not None and not 0 <= attended <= booked:
                problems.append(f"Line {line_no}: rejected, attended ({attended}) is more than booked ({booked}) for {name} on {day}")
                continue
            spellings[name] += 1
            records.append(dict(date=day, kind=name, slots=slots, booked=booked, attended=attended))
            if attended is None:
                problems.append(f"Line {line_no}: attended is blank for {name} on {day}, left out of the figures")
    # keep the most common spelling of each name, compared without case
    best = {}
    for name, count in spellings.items():
        key = name.lower()
        if key not in best or count > spellings[best[key]]:
            best[key] = name
    for r in records:
        r["kind"] = best[r["kind"].lower()]
    return records, problems


def type_names(records):
    """Return the appointment types in alphabetical order, with no repeats."""
    return sorted({r["kind"] for r in records})


def analyse(records, kind):
    """Work out the attendance figures for one appointment type.

    Cancelled sessions (booked is 0) and days with missing attendance are left
    out of every average, highest and lowest value, but still appear in the
    table. Rejected rows never reach this function.

    Returns:
        dict: totals, averages, highest and lowest day, weekly averages, trend,
        fill rate, missed rate and the daily rows used for the table and chart.
    """
    first_day = min(r["date"] for r in records)
    rows = sorted((r for r in records if r["kind"] == kind), key=lambda r: r["date"])
    for r in rows:
        r["week"] = (r["date"] - first_day).days // 7 + 1
        if r["booked"] == 0:
            r["status"] = "Cancelled"
        elif r["attended"] is None:
            r["status"] = "Missing"
        else:
            r["status"] = "OK"
    valid = [r for r in rows if r["status"] == "OK"]
    if not valid:
        return None
    total = sum(r["attended"] for r in valid)
    highest = max(valid, key=lambda r: r["attended"])
    lowest = min(valid, key=lambda r: r["attended"])
    weeks = {}
    for w in (1, 2, 3):
        wk = [r["attended"] for r in valid if r["week"] == w]
        weeks[w] = dict(total=sum(wk), days=len(wk), avg=sum(wk) / len(wk) if wk else None)
    if not weeks[1]["avg"] or weeks[3]["avg"] is None:
        change, label = None, "Not enough data"
    else:
        change = (weeks[3]["avg"] - weeks[1]["avg"]) / weeks[1]["avg"] * 100
        label = "Rising" if change > TREND_LIMIT else "Falling" if change < -TREND_LIMIT else "Steady"
    running = [r for r in rows if r["status"] != "Cancelled"]
    fill = sum(r["booked"] for r in running) / sum(r["slots"] for r in running) * 100
    booked_valid = sum(r["booked"] for r in valid)
    missed = (booked_valid - total) / booked_valid * 100
    return dict(
        kind=kind, rows=rows, total=total, days=len(valid), average=total / len(valid),
        highest=highest, lowest=lowest, weeks=weeks, change=change, trend=label,
        fill_rate=fill, missed_rate=missed, missed=booked_valid - total,
        cancelled=sum(r["status"] == "Cancelled" for r in rows),
        missing=sum(r["status"] == "Missing" for r in rows),
    )


def show_summary(result):
    """Print the text summary, the daily table and a simple bar graph."""
    r = result
    print(f"\nATTENDANCE TRENDS: {r['kind'].upper()}")
    print("-" * 52)
    print(f"Total attended:        {r['total']} over {r['days']} days")
    print(f"Daily average:         {r['average']:.1f}")
    print(f"Highest day:           {r['highest']['date']:%a %d %b} ({r['highest']['attended']})")
    print(f"Lowest day:            {r['lowest']['date']:%a %d %b} ({r['lowest']['attended']})")
    for w, d in r["weeks"].items():
        shown = "no data" if d["avg"] is None else f"{d['avg']:.1f}"
        print(f"Week {w} daily average:  {shown}")
    if r["change"] is None:
        print(f"Trend:                 {r['trend']}")
    else:
        print(f"Trend:                 {r['trend']} ({r['change']:+.1f}% week 1 to week 3)")
    print(f"Average fill rate:     {r['fill_rate']:.0f}% of slots booked")
    print(f"Missed appointments:   {r['missed']} ({r['missed_rate']:.0f}% of bookings)")
    if r["cancelled"] or r["missing"]:
        print(f"Note: {r['cancelled']} cancelled day(s) and {r['missing']} day(s) with missing data left out of the figures.")
    print("\nDate        Booked Attended  Graph")
    for row in r["rows"]:
        shown = "-" if row["attended"] is None else str(row["attended"])
        bar = "#" * (row["attended"] or 0)
        note = "  (" + row["status"].lower() + ")" if row["status"] != "OK" else ""
        print(f"{row['date']:%a %d %b}  {row['booked']:>6} {shown:>8}  {bar}{note}")


def main():
    """Load the data, then let the user pick appointment types until they quit."""
    records, problems = load_data("Task3_data.csv")
    for note in problems:
        print("Data note:", note)
    names = type_names(records)
    while True:
        print("\nAppointment types:")
        for i, name in enumerate(names, start=1):
            print(f"  {i}. {name}")
        choice = input(f"Choose 1 to {len(names)}, or Q to quit: ").strip().lower()
        if choice == "q":
            break
        if choice.isdigit() and 1 <= int(choice) <= len(names):
            result = analyse(records, names[int(choice) - 1])
            if result is None:
                print("No usable data for this appointment type.")
            else:
                show_summary(result)
        else:
            print("Please enter a number from the list, or Q.")


if __name__ == "__main__":
    main()
