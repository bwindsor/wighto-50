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


def write_output(output_data: list[dict], output_file: str):
    output_data = sorted(output_data, key=lambda r: (r["Name"], r["StartTime"]))
    with open(output_file, "w") as f:
        fieldnames = ("Name", "Organisation", "Class", "BibNumber", "StartTime", "ControlCardNumber", "StartName")
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        f.write(f"// {','.join(fieldnames)}\n")
        writer.writerows(output_data)


def read_output_file(filename: str):
    with open(filename, "r") as f:
        fieldnames = f.readline().strip().removeprefix("//").strip().split(",")  # Skip first comment row
        reader = csv.DictReader(f, fieldnames=fieldnames)
        return list(reader)


def append_new_entries(old_start_clock_data: list[dict], new_si_extract_data: list[dict]):
    old_names = {r["Name"] for r in old_start_clock_data}
    new_names = {r["Name"] for r in new_si_extract_data}
    names_to_add = new_names - old_names
    new_records = list(filter(lambda x: x["Name"] in names_to_add, new_si_extract_data))
    print(f"Adding {len(new_records)} new records")
    for record in new_records:
        matches = list(filter(lambda r: r["Class"].startswith(record["Class"]) and r["StartTime"] == record["StartTime"].strftime("%H:%M:%S"), old_start_clock_data))
        assert len(matches) <= 1
        if len(matches) == 1:
            print(f"New entry for {record["Name"]} on class {record["Class"]} matches existing start at {matches[0]["StartTime"]} running variation {matches[0]["Class"][-1:]} first")
            existing_start_class = matches[0]["Class"]
            if existing_start_class.endswith(" A"):
                run_order = 1
            elif existing_start_class.endswith(" B"):
                run_order = 0
            else:
                raise ValueError("Unknown class suffix")
        else:
            print(f"New entry for {record["Name"]} on class {record["Class"]} at {record["StartTime"].strftime("%H:%M:%S")} does not coincide with any existing entries")
            run_order = 0

        next_bib_number = max(int(r["BibNumber"]) for r in old_start_clock_data) + 1
        print(f"Next bib number is {next_bib_number}")
        print(f"Select variation {"A" if run_order == 0 else "B"} first")

        old_start_clock_data.append({
            **record,
            "BibNumber": str(next_bib_number),
            "Class": record["Class"] + (" A" if run_order == 0 else " B"),
            "StartTime": record["StartTime"].strftime("%H:%M:%S")
        })
        old_start_clock_data.append({
            **record,
            "BibNumber": str(next_bib_number + 1),
            "Class": record["Class"] + (" B" if run_order == 0 else " A"),
            "StartTime": (record["StartTime"] + datetime.timedelta(minutes=90)).strftime("%H:%M:%S")
        })

    # Update SI numbers
    for record in new_si_extract_data:
        matches = list(filter(lambda r: r["Name"] == record["Name"], old_start_clock_data))
        assert len(matches) == 2
        if matches[0]["ControlCardNumber"] != record["ControlCardNumber"]:
            print(f"Updating SI number for {record["Name"]} on {matches[0]["Class"]} from [{matches[0]["ControlCardNumber"]}] to [{record["ControlCardNumber"]}]")
            matches[0]["ControlCardNumber"] = record["ControlCardNumber"]
        if matches[1]["ControlCardNumber"] != record["ControlCardNumber"]:
            print(f"Updating SI number for {record["Name"]} on {matches[1]["Class"]} from [{matches[1]["ControlCardNumber"]}] to [{record["ControlCardNumber"]}]")
            matches[1]["ControlCardNumber"] = record["ControlCardNumber"]



## Initial Day 1 list generation
# data = read_si_timing_export("Day1SITimingExport.csv")
# data = edit_start_clock_data_day1(data)
# write_output(data, "StartClockFile.csv")

## Initial Day 2 list generation
# data = read_si_timing_export("Day2SITimingExport.csv")
# data = edit_start_clock_data_day2(data)
# write_output(data)


## Day 1 updates
new_data = read_si_timing_export("Day1SITimingExport_20260904_204000.csv")
old_data = read_output_file("StartClockFile.csv")
append_new_entries(old_data, new_data)
write_output(old_data, "StartClockFile_20260904_204000.csv")
