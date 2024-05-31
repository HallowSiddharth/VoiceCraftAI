from flask import Flask, render_template, request
# from test import transcribe, translate

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dub')
def dub():
    return render_template('dub.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/clone")
def clone():
    return render_template("clone.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    print
    if 'file' not in request.files:
        return 'No file part'
    
    voice_model = request.form.get('voice_model')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')

    print(f"Voice Model: {voice_model}")
    print(f"Start Time: {start_time}")
    print(f"End Time: {end_time}")
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    print('/home/a/voicecraft/demo/VoiceCraftAI/' + file.filename)
    file.save('/home/a/voicecraft/demo/VoiceCraftAI/' + "demo.mp4")
    import test, voice_cloning, trimming, vtt_to_srt
    trimming.trim_video('/home/a/voicecraft/demo/VoiceCraftAI/' + file.filename, start_time, end_time)
    test.transcribe(languages=lst)
    voice_cloning.clone_voice(languages=lst)
    vtt_to_srt.main(languages=lst)

    return 'SUCCESS'


if __name__ == "__main__":
    #import shutil
    #shutil.rmtree("/home/a/voicecraft/AICoverGen/song_output/")
    
    lst =  ["kannada"]
    app.run(debug=True)

# ["kannada","malayalam","telugu","tamil","bengali","urdu","hindi","gujarati","marathi"]