import time
import subprocess
from . import search as src
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify, send_from_directory, Response, session


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py
# Load default config and override config from an environment variable

app.config.update(dict( 
    SECRET_KEY = 'devkey', USERNAME = 'admin', PASSWORD = 'default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def command_terminal(bash, no_output=False):
    process = subprocess.Popen(bash, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if not no_output:
        print(bash)
        print(output, error)

def seek_and_destroy(seek):
    
    flag = True
    first_run = True

    while flag:
        
        process = subprocess.Popen("wmctrl -l", stdout=subprocess.PIPE, shell=True)
        x, y = process.communicate()
        x = str(x)[:-3]
         
        all_windows = x.split("  0 fsiles ")
        mozilla = [s for s in all_windows if "Mozilla" in s]

        if first_run:
            tab = mozilla
            first_run=False
        elif mozilla == tab:
            flag = False
            break
        
        print("\n{}\n".format(mozilla))
        for s in mozilla:
            if seek.lower() in s.lower():
               command_terminal('firefox --new-tab google.com; wmctrl -a firefox;xdotool key Ctrl+w;xdotool key Ctrl+w;', no_output=True)
               flag = False
            else:
                command_terminal('firefox --new-tab google.com; wmctrl -a firefox;xdotool key Ctrl+w;xdotool key Ctrl+Tab;', no_output=True)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/firefox", methods=["POST", "GET"])
def firefox():
    
    args = request.form.get('link_to', '')

    if " " not in args and "." in args:

        command_terminal('firefox "{}"'.format(args))

    elif "@dzr" in args[:4].lower():

        play_dzr = src.deezer(args[5:], limit="1")["data"][0]["link"]
        command_terminal('firefox "{}"'.format(play_dzr))

    elif "@p" in args[:2].lower():
        
        seek_and_destroy('youtube')
                   
        search = args[3:]
        play_yt = src.youtube(search)
        command_terminal('firefox --new-tab {};'.format(play_yt))
    
    elif "@cmd" in args.lower()[:4]:
        command_terminal(args[5:])
    
    elif "@op" in args.lower()[:3]:
        seek_and_destroy("oioi")
        bash = 'firefox --new-tab "https://jajji.onepieceex.com.br/?midia=1&numero={}"'.format(args[4:]) 
        print(bash)
        command_terminal(bash)
        command_terminal('firefox --new-tab google.com; wmctrl -a firefox;xdotool key Ctrl+w;', no_output=True)
        time.sleep(2)
        command_terminal('xdotool key Return;', no_output=True)
        time.sleep(1)
        command_terminal('xdotool key space', no_output=False)
               

    elif "@q!" in args.lower()[:3]:
        seek_and_destroy(args[4:])

    else:
        args = args.replace(" ","%20").lower()
        bashCommand = 'xdg-open "http://www.google.com/search?q={}"'.format(args)
        command_terminal(bashCommand)


    return redirect("/")

if __name__ == "__main__":
    app.run(threaded=True, debug=True, host="0.0.0.0")
