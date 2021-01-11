# ESP32 Function Generator

Lame CLI-controlled function generator for the ESP32.  Quarter-assed
at best.  The ESP32 has an ok DAC.  Eight bits with output limited to
0-3.3V.  I made it much worse by using MicroPython, which is not at
all suitable for high-performance systems.

This would be greatly improved by rewriting it in C and adding
additional hardware to filter, scale and offset the output.

## Commands

* waveform <square | triangle | sawtooth | sin>
* frequency <Hz>
* wavelength <us>
* duty <%>
* vmin <V>
* vmax <V>
* pulse [number of cycles]

## Example

Send 100 1ms pulses

```bash
waveform square
wavelength 2
pulse 100
```
