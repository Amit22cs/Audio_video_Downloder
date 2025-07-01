from flask import Flask, render_template, request, send_file, after_this_request
import yt_dlp
import os
import uuid
import tempfile

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        format_type = request.form['format']
        quality_type = request.form['quality']
        out_id = str(uuid.uuid4())
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(
            temp_dir, f"{out_id}.mp3" if format_type == "audio" else f"{out_id}.mp4")

        ffmpeg_path = r'C:\ffmpeg\ffmpeg-2025-06-23-git-e6298e0759-full_build\bin'

        # Format options based on type
        if format_type == "audio":
            if request.form.get('audio_format') == 'mp3':
                output_path = os.path.join(temp_dir, f"{out_id}.mp3")
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': output_path,
                    'ffmpeg_location': ffmpeg_path,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
            else:  # default to m4a
                output_path = os.path.join(temp_dir, f"{out_id}.m4a")
                ydl_opts = {
                    'format': 'bestaudio[ext=m4a]',
                    'outtmpl': output_path,
                }

        else:
            if quality_type == "fast":
                format_str = 'best[ext=mp4]'
            else:  # high quality
                format_str = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'

            ydl_opts = {
                'format': format_str,
                'outtmpl': output_path,
                'merge_output_format': 'mp4',
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            @after_this_request
            def remove_file(response):
                try:
                    os.remove(output_path)
                except Exception as e:
                    print(f"Failed to delete file: {e}")
                return response

            return send_file(output_path, as_attachment=True)

        except Exception as e:
            return f"<h3>Download failed:</h3><pre>{e}</pre>"

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
