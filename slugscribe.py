from distutils.log import debug 
from fileinput import filename 
from flask import *  
from openai import OpenAI
app = Flask(__name__)   
  
@app.route('/')   
def main():   
    return render_template("form.html")   
  
@app.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        f = request.files['file'] 
        f.save(f.filename)   
        return render_template(
            "acknowledge.html",
            name=f.filename,
            text=transcribe_file(f.filename)
        )

def transcribe_file(fname):
    client = OpenAI()
    audio_file= open(fname, "rb")
    transcript = client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file
    )
    return transcript.text
  
if __name__ == '__main__':   
    app.run(debug=True)

