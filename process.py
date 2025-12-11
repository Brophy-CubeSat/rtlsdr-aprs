import csv
import re


def process_lat_long(val):
    return (val[:-5], val[-5:])


def main():
    global all_lines
    global new_lines
    new_lines = []

    with open("log.txt") as log:
        all_lines = log.readlines()

    for i, l in enumerate(all_lines):
        if l.startswith("KK7YHU-11"):
            new_lines.append(all_lines[i + 1])

    global data
    data = []

    for l in new_lines:
        timem = re.search("/([0-9]{6})h", l)
        if timem:
            time = timem.group(1)
        else:
            # print(l)
            continue
        latm = re.search("h([0-9.]+)([NS])/", l)
        lat = process_lat_long(latm.group(1))
        latd = latm.group(2)
        longm = re.search("/([0-9.]+)([EW])", l)
        long = process_lat_long(longm.group(1))
        longd = longm.group(2)
        # Note: Direwolf has the format (D)DDMM.MM, will all be combined, implement parsing later
        coursem = re.search("/([0-9]{3})/", l)
        course = coursem.group(1)
        altm = re.search("A=([0-9]{6})", l)
        alt = altm.group(1)
        tempm = re.search("([0-9.]+)C", l)
        temp = tempm.group(1)
        pressm = re.search("([0-9.]+)hPa", l)
        press = pressm.group(1)
        vms = re.findall("([0-9.]+)V", l)
        batv = vms[0]
        satm = re.search("([0-9]{2})S", l)
        sat = satm.group(1)
        spv = vms[1]
        spcm = re.search("([-]?[0-9.]+)mA", l)
        spc = spcm.group(1)

        data.append(
            [
                time,
                lat[0],
                lat[1],
                latd,
                long[0],
                long[1],
                longd,
                course,
                alt,
                temp,
                press,
                batv,
                sat,
                spv,
                spc,
            ]
        )

    with open("data.csv", "w", newline="") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(
            [
                "Time (UTC, HHMMSS)",
                "Latitude (Degrees)",
                "Latitude (Minutes)",
                "Latitude (Direction)",
                "Longitude (Degrees)",
                "Longitude (Minutes)",
                "Longitude (Direction)",
                "Course (Degrees)",
                "Altitude (ft)",
                "Temperature (C)",
                "Pressure (hPa)",
                "Bat Voltage (V)",
                "Satellites",
                "SP Voltage (V)",
                "SP Current (mA)",
            ]
        )

        writer.writerows(data)


if __name__ == "__main__":
    main()
