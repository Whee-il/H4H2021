#!/usr/bin/env python
from rgbmatrix import graphics
from baseled import BaseLED
from graphlib import BedGraph

import argparse
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions

class Renderer:
    
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument("-r", "--led-rows", action="store", help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32", default=32, type=int)
        self.parser.add_argument("--led-cols", action="store", help="Panel columns. Typically 32 or 64. (Default: 64)", default=64, type=int)
        self.parser.add_argument("-c", "--led-chain", action="store", help="Daisy-chained boards. Default: 1.", default=1, type=int)
        self.parser.add_argument("-P", "--led-parallel", action="store", help="For Plus-models or RPi2: parallel chains. 1..3. Default: 1", default=1, type=int)
        self.parser.add_argument("-p", "--led-pwm-bits", action="store", help="Bits used for PWM. Something between 1..11. Default: 11", default=11, type=int)
        self.parser.add_argument("-b", "--led-brightness", action="store", help="Sets brightness level. Default: 100. Range: 1..100", default=100, type=int)
        self.parser.add_argument("-m", "--led-gpio-mapping", help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm" , choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'], type=str)
        self.parser.add_argument("--led-scan-mode", action="store", help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)", default=1, choices=range(2), type=int)
        self.parser.add_argument("--led-pwm-lsb-nanoseconds", action="store", help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130", default=130, type=int)
        self.parser.add_argument("--led-show-refresh", action="store_true", help="Shows the current refresh rate of the LED panel")
        self.parser.add_argument("--led-slowdown-gpio", action="store", help="Slow down writing to GPIO. Range: 0..4. Default: 1", default=1, type=int)
        self.parser.add_argument("--led-no-hardware-pulse", action="store", help="Don't use hardware pin-pulse generation")
        self.parser.add_argument("--led-rgb-sequence", action="store", help="Switch if your matrix has led colors swapped. Default: RGB", default="RGB", type=str)
        self.parser.add_argument("--led-pixel-mapper", action="store", help="Apply pixel mappers. e.g \"Rotate:90\"", default="", type=str)
        self.parser.add_argument("--led-row-addr-type", action="store", help="0 = default; 1=AB-addressed panels;2=row direct", default=0, type=int, choices=[0,1,2])
        self.parser.add_argument("--led-multiplexing", action="store", help="Multiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZStripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven (Default: 0)", default=0, type=int)

    def usleep(self, value):
        time.sleep(value / 1000000.0)

    def process(self, graph:BedGraph):
        self.args = self.parser.parse_args()

        options = RGBMatrixOptions()

        if self.args.led_gpio_mapping != None:
            options.hardware_mapping = self.args.led_gpio_mapping
        options.rows = self.args.led_rows
        options.cols = self.args.led_cols
        options.chain_length = self.args.led_chain
        options.parallel = self.args.led_parallel
        options.row_address_type = self.args.led_row_addr_type
        options.multiplexing = self.args.led_multiplexing
        options.pwm_bits = self.args.led_pwm_bits
        options.brightness = self.args.led_brightness
        options.pwm_lsb_nanoseconds = self.args.led_pwm_lsb_nanoseconds
        options.led_rgb_sequence = self.args.led_rgb_sequence
        options.pixel_mapper_config = self.args.led_pixel_mapper
        if self.args.led_show_refresh:
          options.show_refresh_rate = 1

        if self.args.led_slowdown_gpio != None:
            options.gpio_slowdown = self.args.led_slowdown_gpio
        if self.args.led_no_hardware_pulse:
          options.disable_hardware_pulsing = True

        self.matrix = RGBMatrix(options = options)

        try:
            # Start loop
            print("Press CTRL-C to stop")
            self.Render(graph)
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True

    def DrawRect(self, canvas, color, centroid:tuple, size:tuple):
        c_x, c_y = centroid
        width, height = size

        x1 = c_x - width/2
        y1 = c_y - height/2
        x2 = c_x + width/2
        y2 = c_y + height/2

        graphics.DrawLine(canvas, x1, y1, x1, y2, color)
        graphics.DrawLine(canvas, x1, y1, x2, y1, color)
        graphics.DrawLine(canvas, x1, y2, x2, y2, color)
        graphics.DrawLine(canvas, x2, y2, x2, y1, color)

    def EreaseRect(self, canvas, centroid:tuple, size:tuple):
        c_x, c_y = centroid
        width, height = size

        x1 = int(c_x - width/2)
        y1 = int(c_y - height/2)
        
        for x in range(x1, x1+width+1):
            for y in range(y1, y1+height+1):
                canvas.SetPixel(x,y,0,0,0)

    def traverse(self, path, graph):
        name = graph.bed_nodes[path[0]].name
        for i in range(1, len(path)):
            graph.bed_nodes[path[i]].occupied=True
            graph.bed_nodes[path[i]].name = name

            graph.bed_nodes[path[i-1]].occupied = False
            self.Render(graph)
            time.sleep(1)
        

    def Render(self, graph:BedGraph):
        canvas = self.matrix
        white = graphics.Color(50,50,50)
        pink = graphics.Color(100,50,50)
        bed_size = (8,15)
        font = graphics.Font()
        font.LoadFont("../fonts/4x6.bdf")
        
        self.DrawRect(canvas, pink, (57,16), (12,64))

        # Draw Beds
        for node in graph.bed_nodes:
            if node.occupied:
                self.DrawRect(canvas, white, node.centroid, bed_size)
                x, y = node.centroid
                x = x-1
                y = y
                graphics.DrawText(canvas, font, x,y, white, node.name[0])
                y = y+6
                graphics.DrawText(canvas, font, x,y, white, node.name[1])
            else:
                self.EreaseRect(canvas, node.centroid, bed_size)