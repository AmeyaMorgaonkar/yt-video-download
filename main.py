from flask import Flask, request, render_template, send_file
from pytubefix import YouTube
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/details", methods=["GET", "POST"])
def details():
    if request.method == "POST":
        url = request.form.get("url")
        format = request.form.get("format")
        input_resolution = request.form.get("resolution")
        print("Url: "+url + "\nFormat: "+format)

        yt = YouTube(url)
        
        if format == "mp4":
            streams = yt.streams.filter(mime_type='video/mp4')
            streams = streams.order_by('resolution').desc()
        else:
            print("Stream Options are not set for mp3")

        resolutions = []
        for stream in streams:
            resolutions.append(stream.resolution)

        resolutions = set(resolutions)
        sorted_resolutions = sorted(resolutions, key=lambda x: int(x.replace("p", "")), reverse=True)

        duration = yt.length
        duration_minutes = int(duration / 60)
        duration_seonds = duration % 60

        if input_resolution:
            stream = streams.filter(res=input_resolution).first()
            buffer = BytesIO()
            stream.stream_to_buffer(buffer)
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name=yt.title)
            
    
    return render_template("results.html", url=url, format=format, resolutions=sorted_resolutions, title=yt.title, thumbnail=yt.thumbnail_url, duration_minutes=duration_minutes, duration_seonds=duration_seonds)


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True, port=5001)