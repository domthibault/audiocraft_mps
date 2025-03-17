import threading
import queue
import time
import os
import re
import unicodedata
import torch  # Remis ici
from audiocraft.models import AudioGen
from audiocraft.data.audio import audio_write
from SimpleOSC import SimpleOSC

# Setup device
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print("Torch will be running on " + device)

# Default model and parameters
current_model_name = 'facebook/audiogen-medium'
current_duration = 5

# Load the model
model = AudioGen.get_pretrained(current_model_name, device=device)
model.set_generation_params(duration=current_duration)

# Setup OSC
osc = SimpleOSC(send_ip="127.0.0.1", send_port=9000, receive_port=8000)

# Queue for handling incoming requests
request_queue = queue.Queue()
cancel_event = threading.Event()  # Event for cancelling the current generation


def sanitize_filename(text):
    """
    Nettoyer le texte pour en faire un nom de fichier sûr en ASCII.
    - Supprime les accents.
    - Remplace les espaces et ponctuations par des underscores.
    - Conserve uniquement les lettres, chiffres, tirets et underscores.
    """
    # Convertir en ASCII (supprime les accents)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    
    # Remplacer les espaces et caractères spéciaux par des underscores
    text = re.sub(r'[^a-zA-Z0-9_-]', '_', text)
    
    # Supprimer les multiples underscores consécutifs
    text = re.sub(r'_+', '_', text).strip('_')
    
    return text


def generate_audio(descriptions, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    filepaths = []

    for description in descriptions:
        if cancel_event.is_set():
            print("Generation cancelled!")
            break  # Annule la génération si l'événement est activé

        print(f"Generating audio for: '{description}'")

        # Générer le fichier audio
        wav = model.generate([description])

        # Nettoyer le nom du fichier
        safe_filename = sanitize_filename(description)
        filepath = os.path.join(output_dir, safe_filename)

        # Sauvegarder l'audio
        audio_write(filepath, wav[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
        absolute_path = os.path.abspath(filepath + ".wav")
        filepaths.append(absolute_path)

    return filepaths


def process_request():
    """Process the requests from the queue in FIFO order."""
    while True:
        description, duration, model_name = request_queue.get()  # Wait for new requests
        if description is None:  # Stop the thread when None is received
            break
        
        global current_duration, current_model_name, model

        # Log the request
        print(f'Received request: "{description}" | Duration: {duration}s | Model: {model_name}')

        # Update duration if needed
        if duration != current_duration:
            current_duration = duration
            model.set_generation_params(duration=current_duration)

        # Update model if necessary
        if model_name != current_model_name:
            try:
                model = AudioGen.get_pretrained(model_name, device=device)
                model.set_generation_params(duration=current_duration)
                current_model_name = model_name
            except Exception as e:
                print(f'Failed to load model {model_name}: {e}')

        # Generate audio
        output_dir = "generated_audio"
        start_time = time.time()
        filepaths = generate_audio([description], output_dir)
        elapsed_time = round(time.time() - start_time, 2)

        # Send OSC response
        for filepath in filepaths:
            osc.send("/audio_generated", filepath)
            print(f'File generated: {filepath} | Time to generate: {elapsed_time}s')

        # Mark the task as done
        request_queue.task_done()


def handle_generate(address, *args):
    if len(args) < 3:
        print("Insufficient arguments. Expected: description, duration, model_name")
        return

    description = args[0]
    duration = float(args[1])
    model_name = args[2]

    # Add request to the queue
    request_queue.put((description, duration, model_name))
    print(f"Request added to queue: {description} | Duration: {duration} | Model: {model_name}")


def handle_cancel(address, *args):
    """Handle cancellation of the current audio generation."""
    print("Received cancel request.")
    cancel_event.set()  # Signal to cancel the current generation

    # Reset the cancel event after stopping
    cancel_event.clear()


# Setup OSC Handlers
osc.on("/generate", handle_generate)
osc.on("/cancel", handle_cancel)

# Start OSC server
osc.start()

# Start the processing thread
processing_thread = threading.Thread(target=process_request, daemon=True)
processing_thread.start()

print("Waiting for OSC messages... Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping OSC server.")
    osc.stop()

# When done, gracefully shutdown the processing thread
request_queue.put(None)  # Stop the thread
processing_thread.join()
