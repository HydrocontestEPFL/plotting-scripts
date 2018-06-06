import matplotlib.pyplot as plt
import pandas
import numpy as np
import argparse

# settings
RIGHT_FLAP_CHANNEL = 5
RIGHT_FLAP_ZERO = 1500
RIGHT_FLAP_GAIN = 0.0001
LEFT_FLAP_CHANNEL = 4
LEFT_FLAP_ZERO = 1500
LEFT_FLAP_GAIN = 0.0001
RUDDER_CHANNEL = 2
RUDDER_ZERO = 1500
RUDDER_GAIN = 0.0001
THRUST_CHANNEL = 1
THRUST_ZERO = 1500
THRUST_GAIN = 0.001

def channel_line(ch):
    return [int(i) for i in ch.strip('[] ').split(',')]

def parse_channels(ch):
    df = pandas.DataFrame()
    ch = np.array([channel_line(line) for line in ch])
    df['thrust'] = (ch[:,THRUST_CHANNEL-1] - THRUST_ZERO) * THRUST_GAIN
    df['rudder'] = (ch[:,RUDDER_CHANNEL-1] - RUDDER_ZERO) * RUDDER_GAIN
    df['left_flap'] = (ch[:,LEFT_FLAP_CHANNEL-1] - LEFT_FLAP_ZERO) * LEFT_FLAP_GAIN
    df['right_flap'] = (ch[:,RIGHT_FLAP_CHANNEL-1] - RIGHT_FLAP_ZERO) * RIGHT_FLAP_GAIN
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='RC output CSV log')
    parser.add_argument('outfile', help='CSV output file name')
    args = parser.parse_args()

    src = pandas.read_csv(args.file, sep=';')

    ch = parse_channels(src['channels'])
    time = src[['time_stamp', 'seq', 'secs', 'nsecs']].copy()
    out = pandas.concat([time, ch], axis=1)

    out.to_csv(args.outfile, sep=';')
    print('wrote {} lines to {}'.format(len(out)+1, args.outfile))

if __name__ == '__main__':
    main()