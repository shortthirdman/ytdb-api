# https://github.com/dropbox/dropbox-sdk-python/blob/master/example/oauth/commandline-oauth.py
import dropbox
import pytube
from flask import Flask, request, json
import os
import platform
import sys

app = Flask(__name__)
app.config["DEBUG"] = True

global SAVE_PATH

@app.route('/ytdb/api/process', methods=['GET'])
def processYTVideos():
    queryParam: object = request.args

    idStr = queryParam.get('video_id')
    urlStr = queryParam.get('video_url')

    if idStr:
        downloadYouTube('https://youtube.com/watch?v=' + idStr)
    elif urlStr:
        downloadYouTube(urlStr)
    else:
        return json.dumps({ "message": "No video_url or video_id provided." })


def downloadYouTube(video_url):
    try:
        yt = pytube.YouTube(video_url)
        if not os.path.exists(SAVE_PATH):
            os.makedirs(SAVE_PATH)
        yt.streams.filter(subtype='mp4', progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(SAVE_PATH)
        caption = yt.captions.get_by_language_code('en-GB')
        subtitle = caption.generate_srt_captions()
        subfile = open("","w")
        subfile.write(subtitle)
        subfile.close()

    except ConnectionError:
        pass


def uploadToDropbox(file, filename):
    """
    :return:
    """
    accessToken = os.environ.get('DROPBOX_ACCESS_TOKEN')
    try:
        dbx = dropbox.Dropbox(accessToken)
        dbx.users_get_current_account()
        dbx.files_upload(file,'/YouTube/story.txt')
    except dropbox.ApiError as err:
        if err.error.is_path() and err.error.get_path().reason.is_insufficient_space():
            return json.dumps({"error": "ERROR: Cannot back up; insufficient space."})
            sys.exit("ERROR: Cannot back up; insufficient space.")
        elif err.user_message_text:
            return json.dumps({"error": err.user_message_text})
            sys.exit()
        else:
            return json.dumps({"error": err})
            sys.exit()


if __name__ == "__main__":
    app.run()
