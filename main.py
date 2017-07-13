import json
from pprint import pprint
import pygame
import sys


def loadJson():
    f = open("courses_ece.json", "r")

    courses = dict()
    for line in f:
        tmp = json.loads(line)
        courses[tmp["code"]] = tmp
        # print tmp["code"]

    f.close()
    return courses


width = 1024
height = 600

numCols = 6
numRows = 10
blockW = width / numCols
blockH = height / numRows

day_to_width = {"MONDAY": 1, "TUESDAY": 2, "WEDNESDAY": 3, "THURSDAY": 4, "FRIDAY": 5}


def getCoordinatesFromTimes(times):
    x = blockW
    y = blockH
    w = blockW - 5
    h = blockH

    if times["day"] in day_to_width:
        x = blockW * day_to_width[times["day"]]
    y = (times["start"] / 3600 - 8) * blockH
    h = (times["end"] - times["start"]) / 3600 * blockH - 5

    return (x, y, w, h)


pygame.init()
screen = pygame.display.set_mode((width, height))
myfont = pygame.font.SysFont("monospace", 15)
fontSmaller = pygame.font.SysFont("monospace", 12)

black = (0, 0, 0)
gray = (50, 50, 50)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
courseColors = []
courseColors.append((0, 255, 0))
courseColors.append((255, 255, 0))
courseColors.append((128, 0, 128))
courseColors.append((255, 165, 0))
courseColors.append((199, 21, 133))



def drawCourse(course, wantedSection, color):
    name = myfont.render(course["code"], 2, black)
    for section in course["meeting_sections"]:
        if section["code"] != wantedSection:
            continue

        subTitle = fontSmaller.render(section["code"], 1, black)
        for lecture in section["times"]:
            pos = getCoordinatesFromTimes(lecture)
            screenColor = screen.get_at((pos[0], pos[1]))

            if (screenColor != (255, 255, 255, 255) and screenColor != color):
                print "Collision with", course["code"], "section", section["code"], screenColor
                pygame.draw.rect(screen, red, pos)
            else:
                pygame.draw.rect(screen, color, pos)

            screen.blit(name, (pos[0], pos[1]))
            screen.blit(subTitle, (pos[0], pos[1] + blockH / 3))

courses = loadJson()

# render text
hour_label = []
hour_label.append(myfont.render("9-10", 1, black))
hour_label.append(myfont.render("10-11", 1, black))
hour_label.append(myfont.render("11-12", 1, black))
hour_label.append(myfont.render("12-1", 1, black))
hour_label.append(myfont.render("1-2", 1, black))
hour_label.append(myfont.render("2-3", 1, black))
hour_label.append(myfont.render("3-4", 1, black))
hour_label.append(myfont.render("4-5", 1, black))
hour_label.append(myfont.render("5-6", 1, black))

day_label = []
day_label.append(myfont.render("Monday", 1, black))
day_label.append(myfont.render("Tuesday", 1, black))
day_label.append(myfont.render("Wednesday", 1, black))
day_label.append(myfont.render("Thursday", 1, black))
day_label.append(myfont.render("Friday", 1, black))

screen.fill(black)

for col in range(numCols):
    for row in range(numRows):
        pygame.draw.rect(screen, white, (col*blockW, row*blockH, blockW-5, blockH-5))

for i in range(len(hour_label)):
    screen.blit(hour_label[i], (blockW*3/5, blockH/3 + blockH + i * blockH))

for i in range(len(day_label)):
    screen.blit(day_label[i], (blockW/3 + blockW + i * blockW, blockH/2))



# INSERT COURSES HERE


drawCourse(courses["ECE311H1F"], "L0101", courseColors[0])
drawCourse(courses["ECE311H1F"], "P0103", courseColors[0])
drawCourse(courses["ECE311H1F"], "T0102", courseColors[0])

drawCourse(courses["ECE361H1F"], "L0101", courseColors[1])
drawCourse(courses["ECE361H1F"], "P0101", courseColors[1])
drawCourse(courses["ECE361H1F"], "T0102", courseColors[1])

drawCourse(courses["ECE302H1F"], "L0101", courseColors[2])
drawCourse(courses["ECE302H1F"], "T0104", courseColors[2])

drawCourse(courses["ECE344H1F"], "L0101", courseColors[3])
drawCourse(courses["ECE344H1F"], "P0102", courseColors[3])

drawCourse(courses["ECE345H1F"], "L0101", courseColors[4])
drawCourse(courses["ECE345H1F"], "T0104", courseColors[4])






pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit(); sys.exit();
