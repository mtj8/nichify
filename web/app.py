from flask import Flask, render_template, request
import src.nichify as nichify

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['nichify_artist']
        
        results = nichify.nichify(query)
        # print(results)
        
        return render_template('index.html', query=query, results=results)
    return render_template('index.html')

from waitress import serve
if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=10000, debug=True)
    serve(app, host='0.0.0.0', port=10000)