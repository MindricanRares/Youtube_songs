#!/usr/bin/env python
import ConfigParser
import urllib2
from lxml import etree
import os
import glob
import smtplib
Config=ConfigParser.ConfigParser()
Config.read('')
def get_list_of_songs(playlist_link):

    print 'Get list of songs started from {0}'.format(playlist_link)
    with open('youtube_songs_downloaded_list', 'r')as file_reader:
        songs_downloaded = file_reader.readlines()

    with open('youtube_songs_downloaded_list', "a") as file_writer:
        response = urllib2.urlopen(playlist_link)
        htmlparser = etree.HTMLParser()
        tree = etree.parse(response, htmlparser)
        for index in range(1, 100):
            song = tree.xpath('//*[@id="pl-load-more-destination"]/tr[{0}]'.format(index))
            if len(song) != 0:
                song_name=song[0].get('data-title')
                song_link='https://www.youtube.com/watch?v=' + str(song[0].get('data-video-id'))+'\n'
                if song_link not in songs_downloaded:
                    print 'Added {0} to the list'.format(song_name.encode('utf-8') )
                    file_writer.write(song_link)
                    print 'Started downloading'
                    os.system('youtube-dl --output "./YoutubeDownload/%(title)s.%(ext)s" --extract-audio --audio-format mp3 {0}'.format(song_link).strip())

            else:
                print 'Playlist over'
                break
    check_size_of_download_folder('./YoutubeDownload/')
    print 'Get list of songs ended'

def check_size_of_download_folder(download_folder,treshold=20):

    print 'Started checking the size of folder'

    os.chdir("./YoutubeDownload")
    if len(glob.glob("*.mp3"))> treshold:
        print 'Number of songs is higher than the limit please clean it'
    else:
        print 'There is still enough space'

    print 'Finished checing the size of folder'


def send_notification_email():

    print 'Sending notification started'

    content= 'Number of songs is higher than the limit please clean it'
    mail=smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(ConfigSectionMap('SectionOne')['user'],ConfigSectionMap('SectionOne')['pass'])
    mail.sendmail(ConfigSectionMap('SectionOne')['user'],ConfigSectionMap('SectionOne')['sender_email'],content)
    mail.close()

    print 'Sending notification ended'



def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
youtube_download_playlist='https://www.youtube.com/playlist?list=PL-ozwwP5MV8atkblX43F8k-RbT58cg1_f'
get_list_of_songs(youtube_download_playlist)
