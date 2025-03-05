from audiocraft.models import AudioGen
from audiocraft.data.audio import audio_write
import argparse
import time
from tqdm import tqdm
import re
import os

model = AudioGen.get_pretrained('facebook/audiogen-medium', device='mps')
model.set_generation_params(duration=5)  # generate [duration] seconds.

start = time.time()


def generate_audio(descriptions, output_dir):
    """
    Generate audio based on descriptions and save each file using the prompt as filename.

    Parameters:
    - descriptions (list of str): List of descriptions for audio generation.
    - output_dir (str): Directory where the generated files will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
    wavs = model.generate(descriptions)  # generates samples for all descriptions in array.

    for prompt, one_wav in zip(descriptions, wavs):
        filename = re.sub(r'\s+', '_', prompt) + ".wav"  # Replace spaces with underscores
        filepath = os.path.join(output_dir, filename)
        audio_write(filepath, one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
        print(f'Generated {filepath}.')
        print(f'Elapsed time: {round(time.time() - start, 2)}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate audio based on descriptions.")
    parser.add_argument("descriptions", nargs='+', help="List of descriptions for audio generation")
    parser.add_argument("--output", required=True, help="Output directory where audio files will be saved")
    args = parser.parse_args()

    generate_audio(args.descriptions, args.output)