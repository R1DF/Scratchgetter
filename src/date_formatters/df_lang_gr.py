# Preinstalled Greek date formatter
def format_date(details, ld):
    # Sample variable: 2016-01-10T05:12:21.000Z
    # Formatting date
    date, time = details.split("T")
    year, month, day = date.split("-")
    month = ld["reusable"]["monthsFormatted"][int(month)]

    # Formatting time
    time = time[:8]  # Cutting off the ".XXXZ"
    preposition = "στην" if time[:2] == "01" or time[:2] == "13" else "στις"

    return f"{day} {month} {year} {preposition} {time}"
