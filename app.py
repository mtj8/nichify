from flask import Flask, render_template, request
import src.nichify as nichify

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['nichify_artist']
        
        # TODO: add regex for the query
        
        results = nichify.nichify(query)
        # print(results)
        
        return render_template('index.html', query=query, results=results)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)