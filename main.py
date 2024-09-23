import os
import time
import turtle
import json
import urllib.request
import webbrowser


def get_astronaut():

    url = 'http://api.open-notify.org/astros.json'
    res = urllib.request.urlopen(url)
    result = json.loads(res.read())
    print(result)

    with open('iss.txt', 'w') as file:

        file.write(f'В настоящий момент на МКС {str(result["number"])} космонавтов:\n\n')
        print('В настоящий момент на МКС ' + str(result["number"]) + ' космонавтов:\n')

        people = result['people']
        a =[]
        for person in people:
            file.write(person['name'] + '\n')
            print(person['name'])
            a.append(person['name'])

    return a


def get_iss_location(time_sl=5):
    url = 'http://api.open-notify.org/iss-now.json'
    res = urllib.request.urlopen(url)
    result = json.loads(res.read())

    location = result['iss_position']
    latitude = float(location['latitude'])
    longitude = float(location['longitude'])
    print('location: ', longitude, latitude)

    time.sleep(time_sl)

    return  longitude, latitude


def main(time_sl, FONT):
    try:
        a = get_astronaut()
    except Exception as e:
        print('Get list if astronaut error:', type(e).__name__)


    screen = turtle.Screen()
    screen.setup(1280, 720)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic('image/map_c.gif')
    screen.register_shape('image/iss.gif')

    iss = turtle.Turtle()
    iss.penup()
    iss.shape('image/iss.gif')


    loc_text = turtle.Turtle()

    textbox = turtle.Turtle()
    textbox.hideturtle()

    textbox.penup()
    textbox.shape()
    textbox.color('white')

    textbox.goto(-180, 80)
    textbox.write("Hello it's ISS", align='left', font=FONT)
    textbox.goto(-180, 30 )
    textbox.write('On board today:', align='left', font=('Courier', 12, 'bold'))
    textbox.goto(-180, -25 )
    textbox.write('\n'.join(a), align='left', font=FONT)
    textbox.goto(-180, -60 )
    textbox.write("For exit press 'q'", align='left', font=FONT)

    longitude, latitude = 0, 0

    while True:

        screen.listen()
        if screen.onkey(lambda: turtle.bye(), 'q'):
            turtle.done()

        try:
            longitude, latitude = get_iss_location(time_sl)
        except Exception as e:
            print('Error :', type(e).__name__)

        curr_time = time.strftime("%Y-%m-%d %H:%M:%S")

        iss.goto(longitude, latitude)

        loc_text.undo()
        loc_text.hideturtle()
        loc_text.penup()
        loc_text.shape()
        loc_text.color('white')
        loc_text.goto(-180, -40 - FONT_SIZE / 4)
        loc_text.write(f"Location : {longitude, latitude}", align='left', font=FONT)


if __name__ == '__main__':
    time_sl = 5
    FONT_SIZE = 10
    FONT = ('Courier', FONT_SIZE, 'bold')
    main(time_sl,  FONT)


