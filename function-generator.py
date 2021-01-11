import ure
import sys
import math
import time
import machine
import uselect

print("Running select loop")

spoll = uselect.poll()
spoll.register(sys.stdin, uselect.POLLIN)

tokenize = ure.compile(" +")

waveform = {
    'waveform': 'square',
    'wavelength': 100000,
    'duty': 0.5,
    'vmin': 0,
    'vmax': 3.3,
}

dac = machine.DAC(machine.Pin(25, machine.Pin.OUT), bits=8)

def square(t):
    if t < waveform['duty']:
        return 1
    else:
        return 0

def triangle(t):
    if t < 0.5:
        return 2*t
    else:
        return 1 - 2*(t-.5)

def sawtooth(t):
    return t

def sin(t):
    return math.sin(t*2*cmath.pi)/2 + .5

def read_command():
    command = ''
    print('> ', end='')

    while True:
        if spoll.poll(1):
            char = sys.stdin.read(1)
            print(char, end='')

            if char == '\n':
                break
            else:
                command += char

    return command

while True:
    command = read_command()
    args = tokenize.split(command)
    command_name = args.pop(0)

    if command_name == 'waveform':
        if args[0] == 'square' or args[0] == 'triangle' or args[0] == 'sawtooth' or args[0] == 'sin':
            waveform['waveform'] = args[0]
        else:
            print('Unknown waveform type:', args[0])
    elif command_name == 'frequency':
        waveform['wavelength'] = 1/float(args[0]) * 1000000
    elif command_name == 'wavelength':
        waveform['wavelength'] = float(args[0])
    elif command_name == 'duty':
        waveform['duty'] = float(args[0])/100
    elif command_name == 'vmin':
        waveform['vmin'] = float(args[0])
    elif command_name == 'vmax':
        waveform['vmax'] = float(args[0])
    elif command_name == 'pulse':
        pulses = 1
        if len(args) > 0:
            pulses = int(args[0])

        last_dac_out = -1
        start = time.ticks_us()
        end_delta = pulses*waveform['wavelength']

        while True:
            delta = time.ticks_diff(time.ticks_us(), start)
            if delta >= end_delta:
                break

            t = (delta % waveform['wavelength'])/waveform['wavelength']
            scaled = globals()[waveform['waveform']](t)
            vout = waveform['vmin'] + scaled * (waveform['vmax'] - waveform['vmin'])
            dac_out = round(255 * vout/3.3)

            if dac_out != last_dac_out:
                dac.write(dac_out)

        dac.write(0)
    else:
        print('unknown command:', command_name)
