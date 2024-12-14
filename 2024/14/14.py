import common
from colorama import Fore, Back
import os
import shutil
from PIL import Image, ImageDraw

OUTPUT_DIR = '.output'
SIZE = (101,103)

def run_robot(line, seconds, size):
    px, py = [int(n) for n in line.split(' ')[0][2:].split(',')]
    vx, vy = [int(n) for n in line.split(' ')[1][2:].split(',')]
    x = px + seconds * vx
    y = py + seconds * vy
    x %= size[0]
    y %= size[1]
    return x,y

def part_one(lines, size=SIZE):
    quadrants = [0, 0, 0, 0]
    for line in lines:
        x, y = run_robot(line, 100, size)
        if x < size[0] // 2:
            if y < size[1] // 2:
                quadrants[0] += 1
            elif y > size[1] // 2:
                quadrants[1] += 1
        elif x > size[0] // 2:
            if y < size[1] // 2:
                quadrants[2] += 1
            elif y > size[1] // 2:
                quadrants[3] += 1
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

def draw_robots(i, robots):
    image = Image.new("RGB", (SIZE[0] * 10, SIZE[1] * 10), "black")
    draw = ImageDraw.Draw(image)
    for robot in robots:
        draw.rectangle((robot[0] * 10, robot[1] * 10, robot[0] * 10 + 9, robot[1] * 10 + 9), fill="green")
    image.save(f'{OUTPUT_DIR}/{i:06d}.png')

def part_two(lines):
    robots = []
    for line in lines:
        px, py = [int(n) for n in line.split(' ')[0][2:].split(',')]
        vx, vy = [int(n) for n in line.split(' ')[1][2:].split(',')]
        robots.append([px, py, vx, vy])

    # make directory .output
    # if it exists, delete it, including all contents
    highest = 0
    if os.path.exists(OUTPUT_DIR):
        for file in os.listdir(OUTPUT_DIR):
            try:
                num = int(file.split('.')[0])
                if num > highest:
                    highest = num
            except:
                pass
        for robot in robots:
            robot[0] += robot[2] * highest
            robot[1] += robot[3] * highest
            robot[0] %= SIZE[0]
            robot[1] %= SIZE[1]
        i = highest
    else:
        i = 0
        os.makedirs(OUTPUT_DIR)

    # run, creating images in output
    while True:
        draw_robots(i, robots)
        i += 1
        for robot in robots:
            robot[0] += robot[2]
            robot[0] %= SIZE[0]
            robot[1] += robot[3]
            robot[1] %= SIZE[1]

assert part_one(common.Loader.load_lines('test'), (11,7)) == 12
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')
part_two(common.Loader.load_lines())

# This can also be calculated based on images, there is a repeating pattern tied to the SIZE
# I computed it manually, since it was easy. I also ran the image generator until that number to confirm and now I have a nice tree!
