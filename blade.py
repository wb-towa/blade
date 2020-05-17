#/usr/bin/env python

import struct
import argparse


"""
Author: William B
Email: toadwarrior@gmail.com
Date: 2014-Nov-10
Copyright (c) 2014-2020 All Rights Reserved https://github.com/wb-towa/blade/

GPL v3 licence

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "William B"
__copyright__ = "Copyright 2014, William B"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "wb@towa.co"

# TODO:
# - Accept 3 character codes
# - Option to accept / return RGB sets

class Blade(object):

    def __init__(self, color):
        self.color = self._strip_hash(color)

    def _strip_hash(self, color):
        """
        Simplify things and simply remove hashes
        """
        if color.startswith('#'):
            return color.replace('#', '')
        else:
            return color

    def _bounds_check(self, num):
        """
        Bound check - ensure the number is within the 0 to 255 range in
        order to be valid
        """
        if num > 255:
            return 255
        elif num < 1:
            return 0
        else:
            return num

    def blend(self, color2, percent):

        color2 = self._strip_hash(color2)

        r1,g1,b1 = struct.unpack('BBB', self.color.decode('hex'))
        r2,g2,b2 = struct.unpack('BBB', color2.decode('hex'))


        r = self._bounds_check(round((r2-r1)*percent)+r1)
        g = self._bounds_check(round((g2-g1)*percent)+g1)
        b = self._bounds_check(round((b2-b1)*percent)+b1)

        return "%s" % (struct.pack('BBB',*(r,g,b)).encode('hex'))


    def lighten(self, percent):

        # towards white
        tone = 255
        r,g,b = struct.unpack('BBB', self.color.decode('hex'))

        r = self._bounds_check(round((tone-r)*percent)+r)
        g = self._bounds_check(round((tone-g)*percent)+g)
        b = self._bounds_check(round((tone-b)*percent)+b)

        return "%s" % (struct.pack('BBB',*(r,g,b)).encode('hex'))

    def darken(self, percent):

        # towards black
        tone = 0
        r,g,b = struct.unpack('BBB', self.color.decode('hex'))

        r = self._bounds_check(round((tone-r)*percent)+r)
        g = self._bounds_check(round((tone-g)*percent)+g)
        b = self._bounds_check(round((tone-b)*percent)+b)

        return "%s" % (struct.pack('BBB',*(r,g,b)).encode('hex'))


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("colour", help="Colour to modify", type=str)
    parser.add_argument("percent", help="Percentage to blend/shade by (0.0 to 1.0)", type=float)
    parser.add_argument("--blend", "-b", help="Colour to blend colour with", type=str)
    parser.add_argument("--darken", "-d", help="Darken colour", action="store_true")
    parser.add_argument("--lighten", "-l", help="Lighten colour", action="store_true")

    args = parser.parse_args()

    b = Blade(args.colour)

    if args.blend:
        print "Blend %s with %s by %0.2f%% = %s" % (args.colour, args.blend, args.percent, b.blend(args.blend, args.percent))
    elif args.darken:
        print "Darken %s by %0.2f%% = %s" % (args.colour, args.percent, b.darken(args.percent))
    elif args.lighten:
        print "Lighten %s by %0.2f%% = %s" % (args.colour, args.percent, b.lighten(args.percent))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
