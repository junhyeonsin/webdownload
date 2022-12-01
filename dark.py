import youtube_dl
from flask import Flask, render_template, request, send_file, redirect
import os
import asyncio

app = Flask(__name__)

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'music/%(id)s.mp3',
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


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/download', methods=["POST"])
def fileDownload():
    musicid = request.form['url'].split('/')[3]
    ytdl.download([request.form['url']])
    info = ytdl.extract_info(request.form['url'])
    return render_template('download.html', thumbnail=info['thumbnails'][-1]['url'], title=info['title'], id=musicid)


@app.route('/music')
def music():
    params = request.args.to_dict()
    musicid = params['music']
    if len(params) == 0:
        return redirect('/')
    else:
        return send_file(f'music/{musicid}.mp3', download_name='download.mp3', as_attachment=True)


@app.route('/delete')
def delete():
    musicList = os.listdir('./music')
    for i in musicList:
        os.remove(f"./music/{i}")
    return redirect('/')


if __name__ == '__main__':

    app.run(host='0.0.0.0')
