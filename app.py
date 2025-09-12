from flask import Flask, render_template, request
from washman import washmans_reply

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        reply = washmans_reply(query)
        return render_template('reply.html', query=query, reply=reply)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)