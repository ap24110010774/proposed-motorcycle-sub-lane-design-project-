from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd


def read_tripinfo(tripinfo_file):
    tree = ET.parse(tripinfo_file)
    root = tree.getroot()

    trips = root.findall("tripinfo")

    if len(trips) == 0:
        return None

    total_duration = 0
    total_waiting = 0
    total_speed = 0

    cars = bikes = trucks = 0

    car_delay = 0
    bike_delay = 0
    truck_delay = 0

    car_count = 0
    bike_count = 0
    truck_count = 0

    for trip in trips:

        duration = float(trip.attrib["duration"])
        waiting = float(trip.attrib["waitingTime"])
        delay = float(trip.attrib["timeLoss"]) 
        length = float(trip.attrib["routeLength"])

        speed = length / duration

        total_duration += duration
        total_waiting += waiting
        total_speed += speed

        vtype = trip.attrib["vType"].lower()

        if "bike" in vtype or "motorcycle" in vtype:
            bikes += 1
        elif "truck" in vtype:
            trucks += 1
        else:
            cars += 1

    return {
    "Trips": len(trips),

    "Average Travel Time (s)": round(total_duration / len(trips), 2),

    "Average Waiting Time (s)": round(total_waiting / len(trips), 2),

    "Average Speed (m/s)": round(total_speed / len(trips), 2),

    "Cars": cars,
    "Bikes": bikes,
    "Trucks": trucks,

    "Car Delay (s)": round(car_delay / car_count, 2) if car_count > 0 else 0,

    "Bike Delay (s)": round(bike_delay / bike_count, 2) if bike_count > 0 else 0,

    "Truck Delay (s)": round(truck_delay / truck_count, 2) if truck_count > 0 else 0
}


def read_summary(summary_file):

    tree = ET.parse(summary_file)
    root = tree.getroot()

    steps = root.findall("step")

    mean_speed = 0
    running = 0
    waiting = 0

    for step in steps:

        mean_speed += float(step.attrib["meanSpeed"])
        running += float(step.attrib["running"])
        waiting += float(step.attrib["meanWaitingTime"])

    n = len(steps)

    return {
        "Mean Simulation Speed (m/s)": round(mean_speed/n,2),
        "Average Running Vehicles": round(running/n,2),
        "Average Waiting Time Summary": round(waiting/n,2)
    }


def read_edgedata(edge_file):

    tree = ET.parse(edge_file)
    root = tree.getroot()

    edges = root.findall(".//edge")

    density = 0
    occupancy = 0
    flow = 0
    timeloss = 0

    for edge in edges:

        density += float(edge.attrib["density"])
        occupancy += float(edge.attrib["occupancy"])
        flow += float(edge.attrib["flow"])
        timeloss += float(edge.attrib["timeLoss"])

    n = len(edges)

    return {
        "Average Density": round(density/n,2),
        "Average Occupancy": round(occupancy/n,2),
        "Average Flow": round(flow/n,2),
        "Average Time Loss": round(timeloss/n,2)
    }

ROOT = Path(r"D:\internship")

results = []

for case in ROOT.iterdir():

    if not case.is_dir():
        continue

    for scenario in case.iterdir():

        if not scenario.is_dir():
            continue

        if scenario.name.lower() == "base network":
            continue

        tripinfo_file = scenario / "tripinfo.xml"
        summary_file = scenario / "summary.xml"
        edge_file = scenario / "edgedata.xml"

        if not (tripinfo_file.exists()
                and summary_file.exists()
                and edge_file.exists()):
            continue

        trip = read_tripinfo(tripinfo_file)

        if trip is None:
            continue

        summary = read_summary(summary_file)
        edge = read_edgedata(edge_file)

        row = {
            "Traffic System": case.name,
            "Traffic Composition": scenario.name
        }

        row.update(trip)
        row.update(summary)
        row.update(edge)

        results.append(row)

df = pd.DataFrame(results)

print(df)

df.to_excel("results.xlsx", index=False)

print("\n✅ Results saved successfully!")