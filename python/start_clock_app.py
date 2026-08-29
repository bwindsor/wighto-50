import csv
import datetime


def read_si_timing_export(filename: str):
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        return sorted([
            {
                "Name": row["Name (Free Format)"],
                "Organisation": row["Club"] or "IND",
                "Class": row["CourseClass"],
                "StartTime": datetime.datetime.strptime(row["StartTime"], "%H:%M:%S"),
                "ControlCardNumber": row["CardNumbers"],
                "StartName": "Start 1"
            }
            for i, row in enumerate(reader)
        ], key=lambda r: (r["Class"], r["StartTime"]))


def edit_start_clock_data_day1(data: list[dict]):
    output_data = []
    for i, row in enumerate(data):
        output_data.append({
            **row,
            "BibNumber": str(i),
            "Class": row["Class"] + (" A" if i % 2 == 0 else " B"),
            "StartTime": row["StartTime"].strftime("%H:%M:%S")
        })

    for i, row in enumerate(data):
        output_data.append({
            **row,
            "BibNumber": str(i + len(data)),
            "Class": row["Class"] + (" B" if i % 2 == 0 else " A"),
            "StartTime": (row["StartTime"] + datetime.timedelta(minutes=90)).strftime("%H:%M:%S")
        })
    return output_data


def edit_start_clock_data_day2(data: list[dict]):
    return [{
        **row,
        "BibNumber": str(i),
        "Class": row["Class"],
        "StartTime": row["StartTime"].strftime("%H:%M:%S")
    } for i, row in enumerate(data)]


def write_output(output_data: list[dict]):
    with open("StartClockFile.csv", "w") as f:
        fieldnames = ("Name", "Organisation", "Class", "BibNumber", "StartTime", "ControlCardNumber", "StartName")
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        f.write(f"// {','.join(fieldnames)}\n")
        writer.writerows(output_data)


data = read_si_timing_export("Day1SITimingExport.csv")
data = edit_start_clock_data_day1(data)
write_output(data)

# data = read_si_timing_export("Day2SITimingExport.csv")
# data = edit_start_clock_data_day2(data)
# write_output(data)
