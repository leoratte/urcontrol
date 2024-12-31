import rtmidi

def print_midi_ports():
    print('Input:')
    for port in rtmidi.MidiIn().get_ports():
        print(f'  {port}')
    print('Output:')
    for port in rtmidi.MidiOut().get_ports():
        print(f'  {port}')

def open_midi_ports(midi_in_port = None, midi_out_port = None):
    midi_in = rtmidi.MidiIn()
    if midi_in_port:
        try:
            index = midi_in.get_ports().index(midi_in_port)
        except ValueError:
            print(f'Cannot find input midi port {midi_in_port}')
            sys.exit(1)
    else:
        index = -1
        for i, v in enumerate(midi_in.get_ports()):
            if 'Steinberg UR' in v:
                index = i
        if index == -1:
            print(f'Cannot find Steinberg UR device')
            sys.exit(1)
    midi_in.open_port(index)
    midi_in.ignore_types(sysex=False)

    midi_out = rtmidi.MidiOut()
    if midi_out_port:
        try:
            index = midi_out.get_ports().index(midi_out_port)
        except ValueError:
            print(f'Cannot find input midi port {midi_out_port}')
            sys.exit(1)
    else:
        index = -1
        for i, v in enumerate(midi_out.get_ports()):
            if 'Steinberg UR' in v:
                index = i
        if index == -1:
            print(f'Cannot find Steinberg UR device')
            sys.exit(1)
    midi_out.open_port(index)

    return midi_in, midi_out