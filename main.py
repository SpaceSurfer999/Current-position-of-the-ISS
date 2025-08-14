import time
import turtle
import json
import urllib.request
from urllib.error import URLError


# Constants
FONT = ('Courier', 10, 'bold')
TIME_SLEEP = 5
MAP_IMAGE = 'image/map_c.gif'
ISS_ICON = 'image/iss.gif'
ASTRONAUT_FILE = 'iss.txt'


def get_astronauts():
    """Fetch current astronauts on ISS and save to file."""
    url = 'http://api.open-notify.org/astros.json'
    try:
        with urllib.request.urlopen(url) as res:
            result = json.loads(res.read())

        print(f"Currently {result['number']} astronauts on ISS:")
        astronaut_names = [person['name'] for person in result['people']]

        # Save to file
        with open(ASTRONAUT_FILE, 'w') as file:
            file.write(f"Currently {result['number']} astronauts on ISS:\n\n")
            file.write('\n'.join(astronaut_names))

        return astronaut_names

    except (URLError, json.JSONDecodeError, KeyError) as e:
        print(f"Error getting astronaut data: {type(e).__name__}")
        return ["Data unavailable"]


def get_iss_location(time_sleep=5):
    """Fetch current ISS coordinates."""
    url = 'http://api.open-notify.org/iss-now.json'
    try:
        with urllib.request.urlopen(url) as res:
            result = json.loads(res.read())

        location = result['iss_position']
        latitude = float(location['latitude'])
        longitude = float(location['longitude'])
        print(f"ISS Location: {longitude}, {latitude}")

        time.sleep(time_sleep)
        return longitude, latitude

    except (URLError, json.JSONDecodeError, KeyError) as e:
        print(f"Error getting ISS location: {type(e).__name__}")
        return 0, 0  # Default position on error


def setup_screen():
    """Initialize the turtle screen with world map."""
    screen = turtle.Screen()
    screen.setup(1280, 720)
    screen.setworldcoordinates(-180, -90, 180, 90)

    try:
        screen.bgpic(MAP_IMAGE)
        screen.register_shape(ISS_ICON)
    except turtle.TurtleGraphicsError:
        print(f"Error: Missing image files. Please ensure {MAP_IMAGE} and {ISS_ICON} exist.")
        return None

    return screen


def display_info(screen, astronauts):
    """Display static information on the screen."""
    textbox = turtle.Turtle()
    textbox.hideturtle()
    textbox.penup()
    textbox.color('white')

    texts = [
        ("Hello, this is ISS Tracking", (-180, 80)),
        ("Current crew members:", (-180, 30)),
        ('\n'.join(astronauts), (-180, -25)),
        ("Press 'q' to exit", (-180, -60))
    ]

    for text, pos in texts:
        textbox.goto(pos)
        textbox.write(text, align='left', font=FONT)

    return textbox


def main():
    astronauts = get_astronauts()

    screen = setup_screen()
    if not screen:
        return

    iss = turtle.Turtle()
    iss.penup()
    iss.shape(ISS_ICON)

    display_info(screen, astronauts)
    loc_text = turtle.Turtle()
    loc_text.hideturtle()
    loc_text.penup()
    loc_text.color('white')

    screen.listen()
    screen.onkey(lambda: turtle.bye(), 'q')

    while True:
        try:
            longitude, latitude = get_iss_location(TIME_SLEEP)
            iss.goto(longitude, latitude)

            # Update location text
            loc_text.clear()
            loc_text.goto(-180, -90)
            loc_text.write(f"Location: {longitude:.2f}, {latitude:.2f}",
                           align='left', font=FONT)

        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}")
            break


if __name__ == '__main__':
    main()
