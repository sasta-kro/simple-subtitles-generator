from faster_whisper import WhisperModel
from pydub import AudioSegment
import os
import platform
from .utils import format_timestamp

def transcribe_audio(
    input_path: str,
    output_path: str,
    config: dict,
):
    """
    # transcribing the audio file and creating the subtitle file.

    Args:
        input_path: The path to the input audio/video file.
        output_path: The path to save the output subtitle file.
        config: The configuration dictionary.
    """
    # Announcing the model download for the first run.
    print("Loading the transcription model...")
    print("If this is the first run, it will download the model files. This may take a few minutes.")

    # Loading the transcription model.
    model = WhisperModel(config["model_size"], device=config["device"], compute_type="int8")

    # Setting the ffmpeg/ffprobe paths based on the operating system.
    if platform.system() == "Windows":
        ffmpeg_path = os.path.join("tools", "ffmpeg.exe")
        ffprobe_path = os.path.join("tools", "ffprobe.exe")
    else:
        # Assuming ffmpeg and ffprobe are in the system's PATH for macOS/Linux.
        ffmpeg_path = "ffmpeg"
        ffprobe_path = "ffprobe"

    # Extracting audio from the input file.
    audio = AudioSegment.from_file(
        input_path,
        ffmpeg=ffmpeg_path,
        ffprobe=ffprobe_path,
    )
    # The audio is exported to a temporary mono WAV file for transcription.
    temp_audio_path = "temp_audio.wav"
    audio.export(temp_audio_path, format="wav")

    # Transcribing the audio file.
    print(f"Transcribing {os.path.basename(input_path)}... This may take a while.")
    segments, _ = model.transcribe(
        temp_audio_path,
        language=config["language"],
        word_timestamps=False, # Using segment-level timestamps is more readable.
    )

    # Generating the subtitle file content from segments.
    srt_content = ""
    segment_id = 1
    for segment in segments:
        start_time = format_timestamp(segment.start)
        end_time = format_timestamp(segment.end)
        text = segment.text.strip()
        
        # Creating a subtitle block for the entire segment.
        srt_content += f"{segment_id}\n"
        srt_content += f"{start_time} --> {end_time}\n"
        srt_content += f"{text}\n\n"
        segment_id += 1

    # Writing the subtitle file.
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

    # Removing the temporary audio file.
    os.remove(temp_audio_path)

    print(f"Subtitle file saved to {output_path}")
