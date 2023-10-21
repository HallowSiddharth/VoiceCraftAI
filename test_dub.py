from flask import Flask, render_template, url_for, request, redirect
import demo

app = Flask(__name__)
global url

# https://youtu.be/MeBt-1F9nZo?si=cak78p186KVbo8xg

@app.route('/')
def dubbing():
    return render_template('dubbing2.html')

@app.route('/dubbing', methods=['GET','POST'])
def dubbing2():
    if request.method == "POST":
        url = request.form.get("youtubeUrl")
        a = demo.transcribe(url)
        print(a)
        b = demo.translate(a)
        print(b)
    return render_template('dubbing2.html', content = a)

if __name__ == "__main__":
    app.run()
