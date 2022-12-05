import youtube_dl
from flask import Flask, render_template, request, send_file, redirect, make_response
import os
import asyncio
import random
import datetime
app = Flask(__name__)

youtube_dl.utils.bug_reports_message = lambda: ''


@app.route('/')
def main():
    if not request.cookies.get('id'):
        res = make_response()
        res.set_cookie('id', str(random.randint(0, 54632585325251)))
        return res
    return render_template('main.html')


@app.route('/download', methods=["POST"])
def fileDownload():
    #musicid = request.form['url'].split('/')[3]
    cookie = request.cookies.get('id')
    try:
        request.form['exts']
    except KeyError:
        ext = 'mp3'
    else:
        ext = request.form['exts']
    ytdl_format_options = {
        'outtmpl': f'music/{cookie}.{ext}',
        'restrictfilenames': True,
        'noplaylist': False,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        # bind to ipv4 since ipv6 addresses cause issues sometimes
        'source_address': '0.0.0.0',
    }
    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
    start = datetime.datetime.now()
    ytdl.download([request.form['url']])
    end = datetime.datetime.now()
    print(end-start)
    print('downloaded')
    info = ytdl.extract_info(request.form['url'])
    return render_template('download.html', thumbnail=info['thumbnails'][-1]['url'], title=info['title'], id=cookie, ext=ext)


@app.route('/music')
def music():
    params = request.args.to_dict()
    musicid = params['music']
    ext = params['ext']
    if len(params) == 0:
        return redirect('/')
    else:
        return send_file(f'music/{musicid}.{ext}', download_name=f'download.{ext}', as_attachment=True)


@app.route('/delete')
def delete():
    musicList = os.listdir('./music')
    for i in musicList:
        os.remove(f"./music/{i}")
    return redirect('/')


if __name__ == '__main__':

    app.run(host='0.0.0.0')
