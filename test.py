from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dubbing.html')

@app.route('/update_language', methods=['POST'])
def update_language():
    data = request.get_json()
    selected_language = data['language']
    print(selected_language)
    # Do something with the selected language (e.g., store it in a session)
    
    return jsonify({'message': 'Language updated successfully'})

if __name__ == '__main__':
    app.run()
