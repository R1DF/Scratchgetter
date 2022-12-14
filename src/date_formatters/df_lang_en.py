# Preinstalled English date formatter
def format_date(details, ld):
    # Sample variable: 2016-01-10T05:12:21.000Z
    # Formatting date
    date, time = details.split("T")
    year, month, day = date.split("-")

    if day[0] == "0":
        day = day[1]

    if month[0] == "0":
        month = month[1]

    month = ld["reusable"]["monthsFormatted"][int(month)-1]

    if day[-1] == "1" and day != "11":
        ordinal = "st"
    elif day[-1] == "2" and day != "12":
        ordinal = "nd"
    elif day[-1] == "3" and day != "13":
        ordinal = "rd"
    else:
        ordinal = "th"

    # Formatting time
    time = time[:8]  # Cutting off the ".XXXZ"

    return f"{day}{ordinal} {month} {year} at {time}"
