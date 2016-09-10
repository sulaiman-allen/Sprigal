#!/usr/bin/python3
'''
A small program for playing back audio file playlists based on the the rfid tag the program recieves
over the computer's serial port. Makes use of the pyserial library - http://pyserial.sourceforge.net/
Author: Sulaiman Allen
'''
from serial import *
import subprocess
import csv
import sys

global oldRfid
oldRfid = ''

# Audio Player
PLAYER = 'ncmpcpp'  # ncmpcpp will provide the visuals for this project
CONTROLLER = 'mpc'  # mpc has the option of loading a playlist from the command line

# Serial Init
ser = None

# Catalog
catalog = dict()

try:
    def init():
        '''
        Inital setup function for loading database from file and initalizing serial port
        '''
        # Serial init
        global ser

        try:
            ser = Serial('/dev/ttyUSB0', 9600, timeout=1)
        except serialutil.SerialException:
            print '[+] Serial Port Not Found. Try unplugging USB cable and plugging it back in.'
            exit()

        # Database load
        global catalog

        try:
            with open('albums.csv', 'r') as f:
                # copy the database file to a dictionary
                for d in csv.DictReader(f):
                    catalog[d['rfid']] = d['album']
        except NameError:
            print '[+] Album file not found.'
            exit()

        finally:
            # close the database file
            f.close()
            main()

    def catalogPrint(catalog):
        '''
        Test function that prints out the contents of the album database.

        catalog = a dictionary file loaded at start time that contains the information for
        all the albums available <values> and their corresponding rfid tag ids <keys>.
        '''

        for tagID in catalog:
            print 'tagId = ' + str(tagID) + '. ' + 'Album = ' + str(catalog[tagID])

        line = ''
        # if the tag doesnt do a complete read the first time around, this needs to be done.
        while len(line) != 10:
            line = ser.read(10)
            # clean up the extra garbage at the end of the serial data, (Newline character, etc)
            rfid = line.strip().decode('utf-8')
        print 'rfid == ' + str(rfid) + '.'

    def main():
        '''
        Main function. Searches the rfid tag's id against an entry in a database file.

        catalog = a dictionary file loaded at start time that contains the information for
        all the albums available <values> and their corresponding rfid tag ids <keys>.
        '''

        print '[+] Waiting for tag...\n'
        rfid = ser.read(10)
        # clean up the extra garbage at the end of the serial data, (Newline character, etc)
        rfid = rfid.strip().decode('utf-8')

        # if the tag doesnt do a complete read the first time around, this needs to be done.
        while len(rfid) != 8:
            rfid = ser.read(10)
            rfid = rfid.strip().decode('utf-8')

        try:
            catalog[rfid]
            return loadandplay(rfid, catalog[rfid])

        except KeyError:
            return main()

    def loadandplay(rfid, album):
        '''
        Helper function for the "play" function. Loads and starts the playback of the playlist
        (album). Despite the name, this function actually plays the selected playlist whereas
        the "play" function just continues the playback until the tag is removed.

        rfid = string containing the id for the selected album.
        album = string containing the name of the playlist.
        '''
        subprocess.call([CONTROLLER, '-q', 'load', album])
        subprocess.call([PLAYER, 'play'])
        return play(rfid)

    def play(rfid):
        '''
        Plays the loaded playlist until the rfid tag is no longer present.

        rfid = string containing the id for the selected album.
        '''

        line = ser.read(10)
        rfidLocal = line.strip().decode('utf-8')

        while rfid == rfidLocal:
            line = ser.read(10)
            rfidLocal = line.strip().decode('utf-8')

        return actions(rfid, rfidLocal)

    def trackinfo():
        '''
        Gets the track information from (mpc status) and returns a list

        trackInfo = a list of 2 elements,
        the first being the current track number and the second being the number of
        tracks in the current playlist. (trackInfo = ['1','13'])
        '''
        mpc_output = subprocess.check_output([CONTROLLER, 'status']).decode('utf-8')
        sep = ']'
        output = mpc_output.split(sep, 1)[1]
        output_list = output.split()
        trackInfo = output_list[0]
        trackSliced = trackInfo[1:]
        trackInfo = ''

        for char in trackSliced:
            trackInfo += char

        trackInfo = trackInfo.split('/')
        return trackInfo

    def actions(rfid, rfidLocal):
        '''
        Contains all the options for controlling playback such as advancing tracks and pausing.

        rfid = string containing the id for the selected album.
        rfidLocal = serial read called inside this function and compared against an old value (oldRfid)
        '''
        global oldRfid
        # if the value in rfidLocal is the same as it was the last time around the loop,
        # disregard any action to be taken. This is needed because the button presses send
        # a series of presses depending on the duration of the time the button was pressed
        # down but I only want to register one of them.

        # subprocess.call([PLAYER])

        if rfidLocal == oldRfid:
            oldRfid = rfidLocal
            rfidLocal = ser.read(10)
            rfidLocal = rfidLocal.strip().decode('utf-8')
            return actions(rfid, rfidLocal)

        elif rfidLocal == '22222222':
            trackInfo = trackinfo()
            if int(trackInfo[0]) != 1:
                subprocess.call([PLAYER, 'prev'])
                oldRfid = rfidLocal
                return play(rfid)
            else:
                return play(rfid)

        elif rfidLocal == '33333333':
            trackInfo = trackinfo()
            if int(trackInfo[0]) < int(trackInfo[1]):
                subprocess.call([PLAYER, 'next'])
                oldRfid = rfidLocal
                return play(rfid)
            else:
                return play(rfid)

        elif rfidLocal == '11111111':
            subprocess.call([PLAYER, 'toggle'])
            rfidLocal = ser.read(10)
            rfidLocal = rfidLocal.strip().decode('utf-8')
            oldRfid = rfidLocal
            return actions(rfid, rfidLocal)

        elif rfidLocal == '00000000' or rfidLocal == '':
            # fade out
            for level in range(100, 10, -1):
                subprocess.call([CONTROLLER, '-q', 'volume', str(level)])
                #print 'level = {0}'.format(level)
                if level % 10 == 0: 
                    for crunch in range((level / 10) * 5):
                        sys.stdout.write("#")
                    print "\n"
            subprocess.call([CONTROLLER, '-q', 'stop'])
            # remove all entries from the playlist
            subprocess.call([CONTROLLER, '-q', 'clear'])
            subprocess.call([CONTROLLER, '-q', 'volume', '100'])
            oldRfid = rfidLocal
            return main()

        # if its not a control code, hopefully it will be a database code
        else:
            oldRfid = rfidLocal
            return play(rfid)

except KeyboardInterrupt:
    exit()

if __name__ == '__main__':
    init()

# show crunches/(maybe leds) to show proximity to reader the tag is
# catalogPrint(catalog)

# when the tag is removed, have a welcoming "ready" sound play after the volume is turned back up to indicate its ready to accept another tag. Also have leds increase
# brightness for a quick burst

# if the track is the first track, allow the back button to start the track over or
# have the track loop back to the last track
