from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

# Change to your KataGo executable path, configuration path, and model path
KATAGO_PATH = "katago.exe"
CONFIG_PATH = "default_gtp.cfg"
MODEL_PATH = "kata1-b18c384nbt-s9937771520-d4300882049.bin.gz"

def run_katago(gtp_command):
    # Run KataGo as a subprocess with the configuration file and model
    result = subprocess.run(
        [KATAGO_PATH, "gtp", "-config", CONFIG_PATH, "-model", MODEL_PATH],
        input=gtp_command.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    gtp_input = data.get("gtp_command")
    
    if not gtp_input:
        return jsonify({"error": "No GTP command provided"}), 400

    responses = []

    # Initialize the board with size 19 and clear it
    board_size_response = run_katago("1 boardsize 19")
    responses.append(board_size_response)

    clear_board_response = run_katago("2 clear")
    responses.append(clear_board_response)

    # Play the move
    play_move_response = run_katago(f"3 {gtp_input}")
    responses.append(play_move_response)

    return jsonify({"responses": responses})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
