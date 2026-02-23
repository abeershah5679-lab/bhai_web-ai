import requests
import datetime
import pyjokes
import webbrowser
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# 🔥 Talk to Ollama
def ask_ai(message):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",
                "prompt": message,
                "stream": False
            }
        )
        data = response.json()
        return data.get("response", "No response from AI.")
    except Exception as e:
        return f"Error: {str(e)}"


# 🧠 Smart Command Handler
def handle_command(message):
    message = message.lower()

    if "time" in message:
        return "Current time is " + datetime.datetime.now().strftime("%H:%M:%S")

    if "joke" in message:
        return pyjokes.get_joke()

    if "youtube" in message:
        search = message.replace("youtube", "")
        url = "https://www.youtube.com/results?search_query=" + search
        webbrowser.open(url)
        return "Opening YouTube..."

    if "spotify" in message or "play music" in message:
        webbrowser.open("https://open.spotify.com")
        return "Opening Spotify..."

    return ask_ai(message)


# 🌐 COOL GUI
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Bhai AI</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{
    height:100vh;
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    font-family:'Orbitron',sans-serif;
    display:flex;
    justify-content:center;
    align-items:center;
}
.container{
    width:95%;
    max-width:700px;
    height:90vh;
    backdrop-filter: blur(20px);
    background: rgba(255,255,255,0.05);
    border-radius:20px;
    box-shadow:0 0 40px rgba(0,255,255,0.3);
    display:flex;
    flex-direction:column;
    padding:20px;
}
h1{text-align:center;color:#00f7ff;margin-bottom:10px;}
#chat{flex:1;overflow-y:auto;padding:10px;display:flex;flex-direction:column;}
.message{margin:10px 0;padding:12px 15px;border-radius:15px;max-width:75%;}
.user{background:linear-gradient(45deg,#00c6ff,#0072ff);align-self:flex-end;color:white;}
.bot{background:rgba(0,255,255,0.15);border:1px solid #00f7ff;color:white;align-self:flex-start;}
.input-area{display:flex;margin-top:10px;}
input{flex:1;padding:12px;border:none;border-radius:10px;outline:none;font-size:16px;}
button{margin-left:10px;padding:12px 20px;border:none;border-radius:10px;background:#00f7ff;color:black;font-weight:bold;cursor:pointer;}
button:hover{background:#00c6ff;}
</style>
</head>
<body>

<div class="container">
<h1>🤖 Bhai AI</h1>
<div id="chat"></div>

<div class="input-area">
<input id="msg" placeholder="Type something...">
<button onclick="sendMsg()">Send</button>
</div>
</div>

<script>
async function sendMsg(){
    let input=document.getElementById("msg");
    let message=input.value;
    if(!message) return;

    addMessage(message,"user");
    input.value="";

    let res=await fetch("/ask",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message:message})
    });

    let data=await res.json();
    addMessage(data.response,"bot");
}

function addMessage(text,type){
    let div=document.createElement("div");
    div.className="message "+type;
    div.innerText=text;
    document.getElementById("chat").appendChild(div);
    document.getElementById("chat").scrollTop=999999;
}
</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message")
    ai_response = handle_command(user_message)
    return jsonify({"response": ai_response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)