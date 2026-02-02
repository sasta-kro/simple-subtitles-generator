from faster_whisper import WhisperModel
import os
import platform
import subprocess
from .utils import format_timestamp

def transcribe_audio(
    input_path: str,
    output_path: str,
    config: dict,
):
    """
    # Transcribes the audio from a video or audio file and saves it as a subtitle file.
    # This function uses a direct subprocess call to FFmpeg for audio extraction,
    # which is more efficient and removes the need for the pydub library.
    """
    # Determining the correct path for the ffmpeg executable based on the operating system.
    # On Windows, it's expected to be in the 'tools' folder; on macOS/Linux, it's in the system PATH.
    if platform.system() == "Windows":
        ffmpeg_executable_path = os.path.join(os.getcwd(), "tools", "ffmpeg.exe")
    else:
        ffmpeg_executable_path = "ffmpeg"

    # Announcing the model download for the first run.
    print("Loading the transcription model...")
    print("If this is the first run, it will download the model files. This may take a few minutes.")
    
    # Loading the transcription model from faster-whisper.
    # Using 'int8' compute_type for better performance on CPUs.
    model = WhisperModel(config["model_size"], device=config["device"], compute_type="int8")

    # Defining the path for the temporary audio file that will be created.
    temporary_audio_output_path = "temp_audio.wav"
    print(f"Extracting audio from {os.path.basename(input_path)}...")
    
    # Constructing the FFmpeg command to extract and convert the audio.
    # The audio is converted to a 16kHz, single-channel (mono) WAV file,
    # which is the optimal format for the Whisper model.
    ffmpeg_command = [
        ffmpeg_executable_path,
        "-i", input_path,
        "-ar", "16000",       # Setting the audio sample rate to 16kHz.
        "-ac", "1",           # Setting the audio to a single (mono) channel.
        "-c:a", "pcm_s16le",  # Specifying the standard WAV audio codec.
        temporary_audio_output_path,
        "-y",                 # Overwriting the output file if it already exists.
        "-hide_banner",       # Suppressing the ffmpeg banner for cleaner output.
        "-loglevel", "error"  # Restricting ffmpeg output to only show errors.
    ]

    try:
        # Executing the FFmpeg command as a subprocess.
        subprocess.run(ffmpeg_command, check=True)
    except FileNotFoundError:
        print("[ERROR] ffmpeg.exe not found! Please ensure it is in the 'tools' folder for Windows, or installed on your system for macOS/Linux.")
        return
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to extract audio. The input file may be corrupted or in an unsupported format.")
        return

    # Transcribing the extracted audio file.
    print(f"Transcribing the audio... This may take a while depending on the file size.")
    segments, _ = model.transcribe(
        temporary_audio_output_path,
        language=config["language"],
        word_timestamps=False, # We are using segment-level timestamps for better readability.
    )

    # Generating the content for the SRT subtitle file.
    srt_content = ""
    segment_id = 1
    for segment in segments:
        # Formatting the start and end times for the subtitle block.
        start_time = format_timestamp(segment.start)
        end_time = format_timestamp(segment.end)
        # Getting the transcribed text and removing any leading/trailing whitespace.
        text = segment.text.strip()
        
        # Appending the formatted subtitle block to the SRT content.
        srt_content += f"{segment_id}\n"
        srt_content += f"{start_time} --> {end_time}\n"
        srt_content += f"{text}\n\n"
        segment_id += 1

    # Writing the generated SRT content to the output file.
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

    # Cleaning up by removing the temporary audio file.
    if os.path.exists(temporary_audio_output_path):
        os.remove(temporary_audio_output_path)
        
    print(f"Subtitle file has been successfully saved to {output_path}")
