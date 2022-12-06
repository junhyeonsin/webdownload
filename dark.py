import pytube
from flask import Flask, render_template, request, send_file, redirect, make_response
import os
import asyncio
import sys
import random
import datetime
app = Flask(__name__)

#youtube_dl.utils.bug_reports_message = lambda: ''
# ytdl_format_options = {
#     'outtmpl': f'music/{cookie}.{ext}',
#     'restrictfilenames': True,
#     'noplaylist': False,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     # bind to ipv4 since ipv6 addresses cause issues sometimes
#     'source_address': '0.0.0.0',
# }
# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
# ytdl.download([request.form['url']])


@app.route('/')
def main():
    if not request.cookies.get('id'):
        res = make_response(render_template('main.html'))
        res.set_cookie('id', str(random.randint(0, sys.maxsize)))
        return res
    return render_template('main.html')


@app.route('/download', methods=["POST"])
def fileDownload():
    #musicid = request.form['url'].split('/')[3]
    cookie = request.cookies.get('id')
    ext = request.form['exts']
    resolution = request.form['res']
    start = datetime.datetime.now()
    yt = pytube.YouTube(request.form['url'])
    if ext == 'mp3':
        stream = yt.streams.filter(only_audio=True).first()
    else:
        stream = yt.streams.filter(res=resolution).first()
    stream.download('music', filename=f"{cookie}.{ext}")

    end = datetime.datetime.now()
    print(end-start)
    print('downloaded')
    return render_template('download.html', thumbnail=yt.thumbnail_url, title=yt.title, id=cookie, ext=ext)


@app.route('/music')
def music():
    params = request.args.to_dict()
    musicid = params['music']
    ext = params['ext']
    title = params['title']
    if len(params) != 3:
        return redirect('/')
    else:
        print(title)
        return send_file(f'music/{musicid}.{ext}', download_name=f"{title}.{ext}", as_attachment=True)


@app.route('/delete')
def delete():
    musicList = os.listdir('./music')
    for i in musicList:
        os.remove(f"./music/{i}")
    return redirect('/')


@app.errorhandler(404)
def error404(error):
    return redirect('/')


@app.errorhandler(504)
def error504(error):
    return '<h1>다운로드하는데 너무 오래걸려서 조금만 기다려 주세요!</h1>'


if __name__ == '__main__':

    app.run(host='0.0.0.0')
