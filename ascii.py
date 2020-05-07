"""
ascii.py

A program that converts video into ASCII art and play it.

The code to convert image to ASCII art I stole from Mahesh Venkitachalam on:
https://github.com/electronut/pp/blob/master/ascii/ascii.py

Author: Vuong Hoang <vuonghv.cs@gmail.com> , Mahesh Venkitachalam
"""

import sys
import argparse
import numpy as np
import cv2
import curses

from PIL import Image

# gray scale level values from: 
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray (more detail)
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale2 = '@%#*+=-:. '

DEFAULT_COLS = 120

# Set scale (width/height) default as 0.43 which suits a Courier font
DEFAULT_FONT_SCALE = 0.43

def getAverageL(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)
    # get shape
    w,h = im.shape
    # get average
    return np.average(im.reshape(w*h))

def covertImageToAscii(frame, cols, scale, moreLevels):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images 
    """
    # declare globals
    global gscale1, gscale2
    image = Image.fromarray(frame)

    # store dimensions
    W, H = image.size[0], image.size[1]
    # print("input image dims: %d x %d" % (W, H))
    # compute width of tile
    w = W/cols
    # compute tile height based on aspect ratio and scale
    h = w/scale
    # compute number of rows
    rows = int(H/h)

    # check if image size is too small
    if cols > W or rows > H:
        # print("Image too small for specified cols!")
        exit(0)

    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
        # correct last tile
        if j == rows-1:
            y2 = H
        # append an empty string
        aimg.append("")
        for i in range(cols):
            # crop image to tile
            x1 = int(i*w)
            x2 = int((i+1)*w)
            # correct last tile
            if i == cols-1:
                x2 = W
            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))
            # get average luminance
            avg = int(getAverageL(img))
            # look up ascii char
            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]
            # append ascii char to string
            aimg[j] += gsval
    
    # return txt image
    return aimg

def main():
    desc = 'Program converts video to ASCII Art and play it.'
    parser = argparse.ArgumentParser(description=desc)

    # add expected arguments
    parser.add_argument('--file', help='Path to video file')
    parser.add_argument('--out', help='Path to save output file')
    parser.add_argument('--play', help='Path to output file')
    parser.add_argument('--scale', help=f'Font scale, width/height (default: {DEFAULT_FONT_SCALE})', type=float, default=DEFAULT_FONT_SCALE)
    parser.add_argument('--cols', help=f'Number columns (default: {DEFAULT_COLS})', type=int, default=DEFAULT_COLS)
    parser.add_argument('--detail', help='More detail level (default: False)', action='store_true')

    args = parser.parse_args()

    if args.play:
        curses.wrapper(play_ascii, args.play)
        return

    if not args.file:
        print('Require --file VIDEO, usage -h for help')
        sys.exit(1)

    out_file = args.out
    if not out_file:
        out_file = f'{args.file}.txt'

    print('Start converting video to ASCII Art...')
    video_to_ascii(args.file, args.cols, args.scale, args.detail, out_file)

    # Play ASCII video
    curses.wrapper(play_ascii, out_file)

def play_ascii(screen, ascii_file: str):
    """Play the ASCII video from input file"""
    with open(ascii_file, 'r') as infile:
        header = infile.readline()
        info = header.split(' ')
        fps = int(info[0])
        rows = int(info[1])
        cols = int(info[2])

        screen.clear()
        curses.curs_set(0)  # Hide cursor
        y = 0
        for line in infile:
            screen.addstr(y, 0, line.strip())
            y += 1
            if y % rows == 0: 
                y = 0
                screen.refresh()
                curses.napms(1000//fps)

def video_to_ascii(video_file: str, cols: int, scale: float, detail: bool, out_file: str):
    """Convert video frame-by-frame to ASCII art then store in txt file"""
    print(f'Loading Video File: {video_file}')
    cap = cv2.VideoCapture(video_file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    num_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Compute rows from cols and font scale
    # compute width of tile
    w = frame_width / cols
    # compute tile height
    h = w / scale
    rows = int(frame_height/h)
    print(f'VIDEO INFO: FPS = {fps}, FRAMES = {num_frame}, LENGTH = {num_frame/fps} s')

    idx = 0
    with open(out_file, 'w') as outfile:
        # Store FPS and cols, rows that need to display later
        print(f'Store metadata, fps = {fps}, rows = {rows}, cols = {cols} into {out_file}')
        outfile.write(f'{int(fps)} {rows} {cols}\n')

        while True:
            # Capture frame-by-frame, convert to ASCII and store into file
            ret, frame = cap.read()

            if not ret:
                break

            cv2.imshow('Frame', frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            idx += 1
            print(f'Process frame {idx}/{num_frame} (press "q" to stop)')
            aimg = covertImageToAscii(frame, cols=cols, scale=scale, moreLevels=detail)

            # Write ASCII frame to file, need to show later
            outfile.write('\n'.join(aimg))
            outfile.write('\n')

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    print(f'\nStore output file to "{out_file}"')
    print('You could replay the video with command:')
    print(f'$ python ascii.py --play {out_file}')
    print('Done.')

if __name__ == '__main__':
    main()
