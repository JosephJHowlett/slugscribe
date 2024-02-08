from distutils.log import debug 
from fileinput import filename 
from flask import *  
import whisper
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
    model = whisper.load_model("base")
    result = model.transcribe(fname, verbose=True)
    return result["text"]
  
if __name__ == '__main__':   
    app.run(debug=True)

