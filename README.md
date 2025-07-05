# yeemidi
Control your Yeelight bulbs using MIDI! 

## Operation Notes

### Not working well

- Trying multiple groups to do the same thing at the same time. It will never happen at the same time, delays will be introduced and it won't look nice. (Since the bulbs do not support multicast)

### Working kinda well

- Events on bulbs at the same group occur nearly at the same time.

- The most intense output is when the bulb is set to `CT` mode and the temperature is set halfway in between.
