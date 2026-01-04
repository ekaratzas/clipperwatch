import argparse
from astropy import constants as const
import astropy.units as u
from astroquery.jplhorizons import Horizons
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import random

targets = [
    {"name": "Mercury", "color": "#A5A5A5", "size": 25, "isSpacecraft": False},
    {"name": "Venus", "color": "#E3BB76", "size": 45, "isSpacecraft": False},
    {"name": "Earth", "color": "#2271B3", "size": 50, "isSpacecraft": False},
    {"name": "Mars", "color": "#E27B58", "size": 40, "isSpacecraft": False},
    {"name": "Jupiter", "color": "#D39C7E", "size": 120, "isSpacecraft": False},
    {"name": "Saturn", "color": "#C5AB6E", "size": 100, "isSpacecraft": False},
    # {'name': 'Uranus', 'color': '#BBE1E4', 'size': 80, 'isSpacecraft': False},
    # {'name': 'Neptune', 'color': '#6081FF', 'size': 80, 'isSpacecraft': False},
    # {'name': 'Pluto', 'color': '#D6C6B2', 'size': 20, 'isSpacecraft': False},
    {
        "name": "Europa Clipper",
        "color": "#E27B58",
        "size": 40,
        "isSpacecraft": True,
        "launch_date": date(2024, 10, 15),
    },
    {
        "name": "Lucy",
        "color": "#E27B58",
        "size": 40,
        "isSpacecraft": True,
        "launch_date": date(2021, 10, 17),
    },
    {
        "name": "Escapade Blue",
        "color": "#E27B58",
        "size": 40,
        "isSpacecraft": True,
        "launch_date": date(2025, 11, 14),
    },
    {
        "name": "Escapade Gold",
        "color": "#E27B58",
        "size": 40,
        "isSpacecraft": True,
        "launch_date": date(2025, 11, 14),
    },
    {
        "name": "Parker",
        "color": "#E27B58",
        "size": 40,
        "isSpacecraft": True,
        "launch_date": date(2018, 8, 13),
    },
    {
        "name": "Psyche",
        "color": "#E27B58",
        "size": 40,
        "isSpacecraft": True,
        "launch_date": date(2023, 10, 14),
    },
    {
        "name": "Juice",
        "color": "#E27B58",
        "size": 40,
        "isSpacecraft": True,
        "launch_date": date(2023, 4, 15),
    },
    {
        "name": "Osiris",
        "color": "#E27B58",
        "size": 40,
        "isSpacecraft": True,
        "launch_date": date(2016, 9, 9),
    },
    {
        "name": "Voyager 1",
        "color": "#E27B58",
        "size": 40,
        "isSpacecraft": True,
        "launch_date": date(1977, 9, 7),
    },
    {
        "name": "Voyager 2",
        "color": "#E27B58",
        "size": 40,
        "isSpacecraft": True,
        "launch_date": date(1977, 8, 21),
    },
    {
        "name": "New Horizons",
        "color": "#E27B58",
        "size": 40,
        "isSpacecraft": True,
        "launch_date": date(2006, 1, 20),
    },
    {
        "name": "Juno",
        "color": "#E27B58",
        "size": 40,
        "isSpacecraft": True,
        "launch_date": date(2011, 8, 6),
    }
]


def MapNameToJplId(name):
    # https://astroquery.readthedocs.io/en/stable/api/astroquery.jplhorizons.HorizonsClass.html#astroquery.jplhorizons.HorizonsClass
    # https://ssd.jpl.nasa.gov/horizons/manual.html#center
    idMap = {
        "Sun": "10",
        "Mercury": "199",
        "Venus": "299",
        "Earth": "399",
        "Mars": "499",
        "Jupiter": "599",
        "Europa": "502",
        "Saturn": "699",
        "Uranus": "799",
        "Neptune": "899",
        "Pluto": "999",
        "Europa Clipper": "2024-182A",
        "Lucy": "2021-093A",
        "Escapade Blue": "2025-260A",
        "Escapade Gold": "2025-260B",
        "Parker": "2018-065A",
        "Juice": "2023-053A",
        "Psyche": "2023-157A",
        "Juno": "2011-040A",
        "Osiris": "2016-055A",
        "Voyager 1": "1977-084A",
        "Voyager 2": "1977-076A",
        "New Horizons": "2006-001A",
    }
    return idMap[name]


targetSpacecraft = None


def FindTargetSpacecraft(name):
    global targetSpacecraft
    targetSpacecraft = next(
        (target for target in targets if target["name"] == name), None
    )
    return targetSpacecraft

def GetRandomSpacecraft():
    global targetSpacecraft
    count = sum(1 for target in targets if target["isSpacecraft"] is True)
    n = random.randrange(count)
    for i, target in enumerate(target for target in targets if target["isSpacecraft"] is True):
        if i == n:
            print(f"Selected {target['name']}!")
            targetSpacecraft = target
            return targetSpacecraft

# I tried parallelizing jpl GET requests but nasa starts throttling if > 2 parallel requests.
# Even 2 parallel requests reduced execution time from 6 secs to 4 secs but not worth it imho.
def GetAstroData(target, observer="Sun", getDataSinceLaunch=False):
    try:
        observerLocation = "500@" + MapNameToJplId(observer)
        if getDataSinceLaunch:
            stop = date.today().isoformat()
            start = target["launch_date"].isoformat()
            obj = Horizons(
                id=MapNameToJplId(target["name"]),
                location=observerLocation,
                epochs={"start": start, "stop": stop, "step": "7d"},
                id_type=None,
            )
        else:
            obj = Horizons(
                id=MapNameToJplId(target["name"]),
                location=observerLocation,
                id_type=None,
            )
        # https://astroquery.readthedocs.io/en/stable/jplhorizons/jplhorizons.html
        # https://astroquery.readthedocs.io/en/stable/api/astroquery.jplhorizons.HorizonsClass.html#astroquery.jplhorizons.HorizonsClass.ephemerides
        # https://ssd.jpl.nasa.gov/horizons/manual.html#output
        # 18. Heliocentric ecliptic longitude & latitude
        # 19. Heliocentric range & range-rate
        # 20. Observer range & range-rate
        # 29. Constellation Name
        # 33. Galactic longitude and latitude
        eph = obj.ephemerides(quantities="18,19,20")
        target["targetname"] = eph[0]["targetname"].split("(")[0]
        if getDataSinceLaunch:
            ephKey = "ephSinceLaunch" + observer
            target[ephKey] = eph
        else:
            ephKey = "eph" + observer
            target[ephKey] = eph[0]
        # keplerian elements
        if not target["isSpacecraft"]:
            target["el"] = obj.elements()[0]
    except Exception as e:
        print(f"JPL Get error: {e}")
        exit(1)


def PlotStars(ax, xlimit, ylimit):
    ax.set_facecolor("#050508")
    num_stars = 800
    star_x = np.random.uniform(-xlimit, xlimit, num_stars)
    star_y = np.random.uniform(-ylimit, ylimit, num_stars)
    star_sizes = np.random.uniform(0.1, 3.0, num_stars)
    ax.scatter(
        star_x,
        star_y,
        s=star_sizes,
        color="white",
        alpha=0.6,
        edgecolors="none",
        zorder=0,
    )


def PlotTargets(ax):
    # plot sun!
    ax.scatter(0, 0, s=200, color="yellow", label="Sun", zorder=3)

    for obj in targets:
        if obj["isSpacecraft"] and obj != targetSpacecraft:
            continue
        GetAstroData(obj)
        # print(obj)
        eph = obj["ephSun"]
        lon = eph["EclLon"]
        dist = eph["r"]

        angle_rad = np.radians(lon)

        # Calculate Cartesian coordinates (x, y)
        x = dist * np.cos(angle_rad)
        y = dist * np.sin(angle_rad)

        # Plot the object
        if not obj["isSpacecraft"]:
            ax.scatter(
                x,
                y,
                s=obj["size"],
                color=obj["color"],
                label=obj["targetname"],
                zorder=3,
            )

            el = obj["el"]
            # https://astroquery.readthedocs.io/en/stable/api/astroquery.jplhorizons.HorizonsClass.html#astroquery.jplhorizons.HorizonsClass.elements
            a = el["a"]  # Semi-major axis
            ec = el["e"]  # Eccentricity
            w = el["w"]  # Argument of periapsis
            om = el["Omega"]  # Longitude of ascending node

            # https://en.wikipedia.org/wiki/Conic_section#Polar_coordinates
            # https://en.wikipedia.org/wiki/Conic_section#Conic_parameters
            # 1. Create 360 points for the orbit
            theta = np.linspace(0, 2 * np.pi, 360)

            # 2. Calculate the distance 'r' for every point on the ellipse
            # formula: r = a(1 - e^2) / (1 + e*cos(theta))
            r = (a * (1 - ec**2)) / (1 + ec * np.cos(theta))

            # 3. Convert to X, Y coordinates
            x = r * np.cos(theta)
            y = r * np.sin(theta)

            # 4. Rotate the ellipse so it points the right way
            # We add the Argument of Perihelion and Longitude of Ascending Node
            # as this is essentially the longitude of perihelion.
            # We are using it to swing the ellipsis in the 2d map, essentially
            # performing the entire rotation in the same plane.
            total_rotation = np.radians(w + om)
            # https://en.wikipedia.org/wiki/Rotation_matrix#In_two_dimensions
            x_rot = x * np.cos(total_rotation) - y * np.sin(total_rotation)
            y_rot = x * np.sin(total_rotation) + y * np.cos(total_rotation)

            # 5. Plot the path
            ax.plot(x_rot, y_rot, color="white", alpha=0.2, lw=0.8)

        else:
            # spaceship pew pew
            ax.scatter(
                x,
                y,
                s=60,
                color="red",
                marker="D",
                edgecolors="cyan",
                linewidth=1,
                zorder=5,
                label=obj["targetname"],
            )
            ax.text(
                x + 0.2,
                y + 0.2,
                obj["name"],
                color="cyan",
                fontsize=6,
                fontweight="bold",
            )


def PlotSpacecraftTail(ax):
    obj = targetSpacecraft
    GetAstroData(obj, "Sun", True)

    x_list = []
    y_list = []

    for week in obj["ephSinceLaunchSun"]:
        lon = week["EclLon"]
        dist = week["r"]

        angle_rad = np.radians(lon)

        # Cartesian coordinates (x, y)
        x = dist * np.cos(angle_rad)
        y = dist * np.sin(angle_rad)

        x_list.append(x)
        y_list.append(y)

    x_array = np.array(x_list)
    y_array = np.array(y_list)

    ax.plot(x_array, y_array, color="cyan", linestyle="--", lw=1.0, alpha=0.6, zorder=4)
    return


def GetDistSpeedFrom(obj, observer):
    ephKey = "eph" + observer
    dist = obj[ephKey]["delta"]
    speed = obj[ephKey]["delta_rate"]
    if speed > 0:
        motion = "moving away"
    else:
        motion = "moving closer"
    speed = abs(speed)
    message = f"Distance to {observer}: {dist:.5f} AU and {motion} @ {speed:.5f} Km/s"
    return message


def GetSignalDelay(obj):
    distEarthAu = obj["ephEarth"]["delta"] * u.au
    distEarthKm = distEarthAu.to(u.km)
    lightSpeedKm = const.c.to(u.km / u.s)
    ltt = distEarthKm / lightSpeedKm
    message = f"Signal Delay: {ltt:.3f}"
    return message


def GetMissionDays(obj):
    days_passed = (date.today() - obj["launch_date"]).days
    return f"Mission day: {days_passed}"


def PlotTitleLegendStatusBar(ax):
    title = f"{targetSpacecraft['name']} Mission Status"
    plt.title(title, color="white", fontsize=15, pad=20)
    plt.legend(loc="upper right", frameon=False)

    obj = targetSpacecraft

    GetAstroData(obj, observer="Earth")
    GetAstroData(obj, observer="Europa")

    message = f"""
    {obj["name"]}
    System Status: Nominal
    Epoch: {obj["ephSun"]["datetime_str"]}
    {GetMissionDays(obj)}
    {GetSignalDelay(obj)}
    {GetDistSpeedFrom(obj, "Sun")}
    {GetDistSpeedFrom(obj, "Earth")}
    {GetDistSpeedFrom(obj, "Europa")}
    """

    plt.text(
        -15.5, -8.5, message, color="cyan", fontsize=8, family="monospace", alpha=0.7
    )


def PrintOrSave(save_on_disk, filename):
    if save_on_disk:
        plt.tight_layout(pad=0)  # Removes margins
        plt.savefig(filename, dpi=100, pad_inches=0)
        print("Image saved.")
    else:
        plt.show()


def Plot(save_on_disk, filename):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)

    # 16:9 aspect ratio
    xlimit = 16
    ylimit = 9

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-xlimit, xlimit)
    ax.set_ylim(-ylimit, ylimit)

    PlotStars(ax, xlimit, ylimit)
    PlotTargets(ax)
    PlotSpacecraftTail(ax)
    PlotTitleLegendStatusBar(ax)

    PrintOrSave(save_on_disk, filename)


def ListSpacecraft():
    print("Listing spacecraft...")
    for target in targets:
        if target["isSpacecraft"]:
            print(target["name"])
    exit(0)


def main():
    parser = argparse.ArgumentParser(
        description="ClipperWatch: Real-time Europa Clipper Tracking"
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the image to disk instead of showing a window",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="clipper_watch.png",
        help="Filename for the saved image (default: clipper_watch.png)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List supported spacecraft",
    )
    parser.add_argument(
        "--spacecraft",
        type=str,
        default="Europa Clipper",
        help="spacecraft to display (default: Europa Clipper)",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Choose a spacecraft at random",
    )
    args = parser.parse_args()

    print("Starting ClipperWatch...")

    if args.list:
        ListSpacecraft()

    if args.random:
        GetRandomSpacecraft()
    elif FindTargetSpacecraft(args.spacecraft) is None:
        print(f"Spacecraft {args.spacecraft} not found!")
        exit(1)

    if args.save:
        print(f"Mode: Save to disk -> {args.output}")
    else:
        print("Mode: Interactive Window")

    Plot(save_on_disk=args.save, filename=args.output)


if __name__ == "__main__":
    main()
