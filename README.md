# AudioController

# What this script does

This script, when activated, auto-mutes your main web browser (that you set manually) when VLC is playing a media file, and unmutes it when you pause the
media file. If you are watching a youtube video, it will also pause the video (give it like 10 seconds at startup to realize youtube is playing)

# Why it exists

I like listening to streams while working/studying. But sometimes I need to listen to a recorded lecture as well. To listen to the lecture, I would have to
mute the stream I was listening to. But sometimes the lectures contained so much information that I would need to pause *them* to write down everything. But I
don't like silence, and so I would unmute the stream. Then when I was done writing the information, I would mute the stream and unpause the lecture.

This was getting very annoying. So I wrote a script to automate it.

I understand this solves an incredibly specific problem, but on the off chance that someone needs something like this, I'm uploading it to github. 
It's a bit of a pain in the ass to set up, but if you're like me then it's 100% worth it. Have fun.

I've only tested it out on Windows 10.

# Issues

If there are issues getting VLC to launch the status page, try installing the 32bit version instead.
If there are issues with access denied for pygetwindow, try upgrading pip and reinstalling the required packages
