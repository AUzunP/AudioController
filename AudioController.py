from __future__ import print_function
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import time
import requests
import pygetwindow as gw
import win32com.client as comclt
from firefox_profile import FirefoxProfile

#follow the link below to set up VLC to work with this script
#https://stackoverflow.com/questions/24178980/how-to-monitor-vlc-media-player-on-windows-7-using-python
#make sure all imports are working
#change "firefox.exe" to whatever web browser you're using

#for posterity, to set up VLC:
'''
----------------VLC SETUP------------------------
Tools -> Preferences -> Show Settings (All) --> Interface --> Main Interface --> Lua
Set source directory to VLC path (ex: C:\Program Files (x86)\VideoLAN\VLC\lua\http (note that it can be also be
    located under Program Files, not necessarily Program Files (x86)
Set a password
Enter that password below in the second field of the s.auth declaration
Click the "Main Interfaces" tab again, and make sure to enable the "Web" option. Hit save.
Make sure there is a "status.xml" file in the aforementioned file path (same as source directory text field)
Visit http://localhost:8080/requests/status.xml and enter the password
If connection fails open up VLC --> View --> Add --> Interface --> Web, then try again

--------------USE--------------------------------
For ease of use, and if you are able; set up a batch file to automatically execute the script and assign it
to a macro, or just use the batch file the same as you would an executable file.

Note that the program will continuously run and make checks for VLC paused/playing status every second
unless you close out the command prompt (or press Ctrl+C)

Major thanks goes to user pss on stackoverflow, and luismsgomes on github
'''

playbackState = True

def main():

    global playbackState
    sessions = AudioUtilities.GetAllSessions()

    for session in sessions:

        volume = session._ctl.QueryInterface(ISimpleAudioVolume)

        if (session.Process and session.Process.name() == "firefox.exe"):
            print("Grabbed Firefox")

            if (getVLCState() == "paused"):

                print("VLC is paused")
                #change Firefox volume to 1
                print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
                volume.SetMasterVolume(1.0, None)

                if ((playbackState == False) and watchingYoutube()):
                     switchFirefoxPlaybackState()
                     playbackState = True

            elif (getVLCState() == "playing"):

                print("VLC is playing")
                #change Firefox volume to 0
                print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
                volume.SetMasterVolume(0.0, None)

                if (playbackState and watchingYoutube()):
                    switchFirefoxPlaybackState()
                    playbackState = False

    time.sleep(1)

def switchFirefoxPlaybackState():
    #pause/unpause open youtube video
    #set active window to Firefox
    win = gw.getWindowsWithTitle('Firefox')[0]
    win.minimize()
    win.maximize()
    win.activate()
    #simulate k key to pause youtube video
    wsh = comclt.Dispatch("WScript.Shell")
    wsh.SendKeys("k")
    #reset active window to VLC
    win = gw.getWindowsWithTitle('VLC media player')[0]
    win.activate()

def watchingYoutube():

    for profile in FirefoxProfile.get_profiles():
        recovery_data = profile.get_recovery_data()

        if recovery_data is None:
            continue

        for i, window in enumerate(recovery_data.windows):
            # do something with window:
            # print(f"window {i}")
            # print(f"  workspace: {window.workspace}")
            # print(f"  zindex: {window.zindex}")
            # print(f"  size: {window.size!r}")
            # print(f"  position: {window.position!r}")
            # print(f"  mode: {window.mode}")
            # print(f"  tabs:")

            for j, tab in enumerate(window.tabs):
                # do something with tab:
                # print(f"    tab {j}")
                # print(f"      title: {tab.title}")
                # print(f"      last_accessed: {tab.last_accessed}")
                # print(f"      url: {tab.url}")
                currTab = tab.url

                if ("youtube.com/watch?" in tab.url):
                    print("Watching Youtube")
                    return True

def getVLCState():

    info = getInfo()
    startLoc = info.find("<state>") + 7
    endLoc = info.find("</state>")

    return (info[startLoc:endLoc])

def getInfo():

    s = requests.Session()
    s.auth = ('', '')# Username is blank, just provide the password
    r = s.get('http://localhost:8080/requests/status.xml', verify=False)

    return r.text

getInfo()

if __name__ == "__main__":

    while (True):
        main()
