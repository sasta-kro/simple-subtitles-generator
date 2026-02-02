from faster_whisper import WhisperModel
from pydub import AudioSegment
import os
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

    # Extracting audio from the input file.
    # The ffmpeg and ffprobe executables are expected to be in the 'tools' directory.
    audio = AudioSegment.from_file(
        input_path,
        ffmpeg=os.path.join("tools", "ffmpeg.exe"),
        ffprobe=os.path.join("tools", "ffprobe.exe"),
    )
    # The audio is exported to a temporary mono WAV file for transcription.
    temp_audio_path = "temp_audio.wav"
    audio.export(temp_audio_path, format="wav")

    # Transcribing the audio file.
    print(f"Transcribing {os.path.basename(input_path)}... This may take a while.")
    segments, _ = model.transcribe(
        temp_audio_path,
        language=config["language"],
        word_timestamps=True,
    )

    # Generating the subtitle file content.
    srt_content = ""
    segment_id = 1
    for segment in segments:
        for word in segment.words:
            start_time = format_timestamp(word.start)
            end_time = format_timestamp(word.end)
            srt_content += f"{segment_id}\n"
            srt_content += f"{start_time} --> {end_time}\n"
            srt_content += f"{word.word.strip()}\n\n"
            segment_id += 1

    # Writing the subtitle file.
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

    # Removing the temporary audio file.
    os.remove(temp_audio_path)

    print(f"Subtitle file saved to {output_path}")
