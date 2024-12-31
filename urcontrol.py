#!/usr/bin/env python3

import sys
import os
import argparse
import threading
import time
from ur44c import *

import rtmidi

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



def main():
    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=45)
    parser = argparse.ArgumentParser(description='Command line tool to control UR44C by MIDI', formatter_class=formatter)
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose')
    parser.add_argument('--midi-in', '-mi', action='store', help='Input MIDI port', metavar='PORT', default='')
    parser.add_argument('--midi-out', '-mo', action='store', help='Output MIDI port', metavar='PORT', default='')
    parser.add_argument('--input', '-i', action='store', type=int, metavar='input', help='Input number (for Inputs, default:1)', default=1)
    parser.add_argument('--unit', '-u', action='store', metavar='UNIT', help='Unit name (default:mixer)', default='mixer')

    commands = parser.add_argument_group('Commands')
    command = commands.add_mutually_exclusive_group(required=True)
    command.add_argument('--get-midi-ports', '-m', action='store_true', help='Show MIDI ports in system')
    command.add_argument('--list-units', '-lu', action='store_true', help='List unit names')
    command.add_argument('--list-parameters', '-l', action='store_true', help='List available parameters in unit')
    command.add_argument('--get-parameter', '-g', action='store', metavar='PARAMETER', help='Get parameter value')
    command.add_argument('--set-parameter', '-s', action='store', metavar=('PARAMETER', '(VALUE|min|max|def)'), nargs=2, help='Set parameter value')
    command.add_argument('--reset', action='store_true', help='Reset mixer config')

    command.add_argument('--test', action='store_true', help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.unit=='mixer':
        unit = UR44C_Params_Mixer
    elif args.unit=='chstrip':
        unit = UR44C_Params_ChStrip
    elif args.unit=='clean':
        unit = UR44C_Params_Clean
    elif args.unit=='crunch':
        unit = UR44C_Params_Crunch
    elif args.unit=='lead':
        unit = UR44C_Params_Lead
    elif args.unit=='drive':
        unit = UR44C_Params_Drive
    elif args.unit=='pitchfix':
        unit = UR44C_Params_PitchFix
    elif args.unit=='hall':
        unit = UR44C_Params_Hall
    elif args.unit=='room':
        unit = UR44C_Params_Room
    elif args.unit=='plate':
        unit = UR44C_Params_Plate
    elif args.unit=='delay':
        unit = UR44C_Params_Delay
    elif args.unit=='ducker':
        unit = UR44C_Params_Ducker
    elif args.unit=='mbcomp':
        unit = UR44C_Params_MBComp
    else:
        raise Exception('Unit does not exists')

    if args.get_midi_ports:
        print('Input:')
        for port in rtmidi.MidiIn().get_ports():
            print(f'  {port}')
        print('Output:')
        for port in rtmidi.MidiOut().get_ports():
            print(f'  {port}')
    elif args.list_units:
        print('mixer')
        print('chstrip')
        print('clean')
        print('crunch')
        print('lead')
        print('drive')
        print('pitchfix')
        print('hall')
        print('room')
        print('plate')
        print('delay')
        print('ducker')
        print('mbcomp')
    elif args.list_parameters:
        if args.verbose:
            print('NAME                 MIN.VAL MAX.VAL DEF.VAL   VALUE EXPLAIN                      NOTES')
        for i in vars(unit):
            if not i.startswith('__'):
                if args.verbose:
                    attr = getattr(unit, i)
                    print(f'{i:<20} {attr[1]:>7} {attr[2]:>7} {attr[3] if attr[3] is not None else "":>7}   {attr[4]:<35}{attr[5] if attr[5] else ""}')
                else:
                    print(i)


    elif args.get_parameter:
        midi_in, midi_out = open_midi_ports(args.midi_in, args.midi_out)
        ur44c = UR44C(midi_in, midi_out)
        value = ur44c.GetParameterByName(unit, args.get_parameter, args.input-1)
        if args.verbose:
            attr = getattr(unit, args.get_parameter)
            print(f'{args.get_parameter}  |  {attr[4]}')
            print()
            print(f'CURRENT VALUE: {value}')
            print(f'Minimal: {attr[1]}')
            print(f'Maximum: {attr[2]}')
            print(f'Default: {attr[3]}')
            if attr[5]:
                print(f'Notes: {attr[5]}')
        else:
            print(value)

    elif args.set_parameter:
        midi_in, midi_out = open_midi_ports(args.midi_in, args.midi_out)
        ur44c = UR44C(midi_in, midi_out)
        if args.set_parameter[1]=='min':
            value = getattr(unit, args.set_parameter[0])[1]
        elif args.set_parameter[1]=='max':
            value = getattr(unit, args.set_parameter[0])[2]
        elif args.set_parameter[1]=='def':
            value = getattr(unit, args.set_parameter[0])[3]
        else:
            value = int(args.set_parameter[1])
        result = ur44c.SetParameterByName(unit, args.set_parameter[0], value, args.input-1)
        if not result:
            print('FAILED')
            sys.exit(1)

    elif args.reset:
        midi_in = rtmidi.MidiIn().open_port(0)
        midi_out = rtmidi.MidiOut().open_port(0)
        ur44c = UR44C(midi_in, midi_out)
        ur44c.ResetConfig()

    elif args.test:
        midi_in, midi_out = open_midi_ports(args.midi_in, args.midi_out)
        ur44c = UR44C(midi_in, midi_out)
        for i in range(8):
            ur44c.SetParameterByName(UR44C_Params_Mixer, 'MainMix1Volume', 30, 0)
            time.sleep(0.2)

            ur44c.SetParameterByName(UR44C_Params_Mixer, 'MainMix1Volume', 103, 0)
            time.sleep(0.2)


if __name__=='__main__':
    main()
