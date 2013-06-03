all__ = []

from pygame import midi
import time

midi.init()

print midi.get_count()
print midi.get_default_output_id()

output = midi.Output(midi.get_default_output_id()+1)

output.set_instrument(1)
output.note_on(64)
time.sleep(3)
output.note_off(64)

x = raw_input("::")

midi.quit()
