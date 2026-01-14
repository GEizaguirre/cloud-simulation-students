from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from transformers import pipeline
from pydantic import BaseModel
from datetime import datetime
from jinja2 import Template

app = FastAPI()

# 1. Enable CORS (Permet peticions desde qualsevol lloc)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Load Model
print("Carregant model...")
pipe = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
print("Model carregat!")

# 3. In-Memory Database
request_log = []

class InferenceRequest(BaseModel):
    text: str

# --- PLANTILLES HTML (Traduïdes) ---

# PLANTILLA ESTUDIANT: Neta, simple, només mostra el seu resultat
student_template_str = """
<!DOCTYPE html>
<html>
<head>
    <title>Client IA</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f0f2f5; }
        .card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        input[type="text"] { width: 80%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; margin-bottom: 1rem; font-size: 16px; }
        button { background-color: #3b82f6; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; transition: 0.2s; }
        button:hover { background-color: #2563eb; }
        #result { margin-top: 20px; font-weight: bold; font-size: 1.2rem; min-height: 1.5em; }
        .POSITIVE { color: #166534; }
        .NEGATIVE { color: #991b1b; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🤖 Anàlisi de Sentiment IA</h2>
        <p>Escriu una frase (en anglès) per veure si la IA creu que és positiva o negativa.</p>
        <input type="text" id="inputText" placeholder="Escriu aquí... (ex: I love coding)">
        <br>
        <button onclick="sendPrediction()">Analitzar</button>
        <div id="result"></div>
    </div>

    <script>
        async function sendPrediction() {
            const input = document.getElementById("inputText");
            const resultDiv = document.getElementById("result");
            const text = input.value;
            
            if (!text) return;

            resultDiv.innerText = "Analitzant...";
            resultDiv.className = "";

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                const data = await response.json();
                
                // Show result to student
                resultDiv.innerText = `${data.label} (${(data.score * 100).toFixed(1)}%)`;
                resultDiv.className = data.label; // Apply color class
            } catch (error) {
                resultDiv.innerText = "Error de connexió amb el servidor.";
            }
        }
    </script>
</body>
</html>
"""

# PLANTILLA ADMIN: Taula de totes les peticions (Refresc automàtic cada 5s)
admin_template_str = """
<!DOCTYPE html>
<html>
<head>
    <title>Panell del Professor</title>
    <meta http-equiv="refresh" content="5"> 
    <style>
        body { font-family: sans-serif; max-width: 1000px; margin: 2rem auto; padding: 0 1rem; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #1f2937; color: white; }
        tr:nth-child(even) { background-color: #f9fafb; }
        .badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.9em;}
        .POSITIVE { background-color: #dcfce7; color: #166534; }
        .NEGATIVE { background-color: #fee2e2; color: #991b1b; }
    </style>
</head>
<body>
    <h1>🎓 Registre d'Activitat de la Classe</h1>
    <p>Aquesta pàgina s'actualitza automàticament cada 5 segons.</p>
    
    <table>
        <thead>
            <tr>
                <th>Temps</th>
                <th>Text d'entrada</th>
                <th>Predicció</th>
                <th>Confiança</th>
            </tr>
        </thead>
        <tbody>
            {% for log in logs|reverse %}
            <tr>
                <td>{{ log.time }}</td>
                <td>{{ log.input }}</td>
                <td><span class="badge {{ log.label }}">{{ log.label }}</span></td>
                <td>{{ "%.4f"|format(log.score) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

# --- ENDPOINTS ---

@app.get("/", response_class=HTMLResponse)
async def student_view():
    """ La interfície per als estudiants """
    return student_template_str

@app.get("/admin", response_class=HTMLResponse)
async def admin_view():
    """ La interfície per al professor """
    template = Template(admin_template_str)
    return template.render(logs=request_log)

@app.post("/predict")
async def predict(request: InferenceRequest):
    """ La lògica de l'API """
    result = pipe(request.text)[0]
    
    log_entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "input": request.text,
        "label": result['label'],
        "score": result['score']
    }
    request_log.append(log_entry)
    
    # Return the result so the student sees it too
    return log_entry