import os
import json
from src.transcriber import transcribe_audio

def main():
    """
    # The main function of the subtitles generator program.
    """
    # Loading the configuration from CONFIG.json.
    with open("CONFIG.json", "r") as f:
        config = json.load(f)

    # Creating the input and output directories if they don't exist.
    os.makedirs("input_files", exist_ok=True)
    os.makedirs("output_files", exist_ok=True)

    # Processing each file in the input directory.
    for filename in os.listdir("input_files"):
        if filename.lower().endswith(tuple(config["input_extensions"])):
            input_path = os.path.join("input_files", filename)
            output_filename = os.path.splitext(filename)[0] + f".{config['output_format']}"
            output_path = os.path.join("output_files", output_filename)

            print(f"Processing {filename}...")
            transcribe_audio(input_path, output_path, config)
            print(f"Finished processing {filename}.")

if __name__ == "__main__":
    main()
