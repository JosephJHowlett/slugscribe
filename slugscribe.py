from distutils.log import debug 
from fileinput import filename 
from flask import *  
from openai import OpenAI
import os

from rq import Queue
from worker import conn

app = Flask(__name__)
q = Queue(connection=conn)
 
@app.route('/')   
def main():   
    return render_template("form.html")
  
@app.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        f = request.files['file'] 
        f.save(f.filename)   
        print(os.path.exists(f.filename))
        print('\n\n')
        text = q.enqueue(transcribe_file, f.filename)
        return render_template(
            "form.html",
            text=text,
        )

def transcribe_file(fname):
    client = OpenAI()
    audio_file= open(fname, "rb")
    transcript = client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file,
      response_format='vtt'
    )
    return transcript
  
if __name__ == '__main__':   
    app.run(debug=True)

