import subprocess
import ffmpeg
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--video', type=str, help="Input file directory")
parser.add_argument('--output', type=str, help="Output Folder Directory", default="./output/")
parser.add_argument('--whisper', type=str, default="../build/bin/whisper-cli", help="Whisper-cpp executable directory")
parser.add_argument('--model', type=str, help="model directory", default="../models/ggml-large-v3.bin")
parser.add_argument('--wav_name', type=str, default="output", help="Output File Name")
parser.add_argument('--language', type=str, default='', help="Force Language setting")

args = parser.parse_args()

file_name = args.output + args.wav_name + "_16k.wav"

def video_to_wav16k():
    (
        ffmpeg
        .input(args.video)
        .output(file_name, ac=1, ar=16000)
        .run(overwrite_output = True)
    )
    

def whisper_transcribe():
    whisper_cli = args.whisper
    model = args.model
    wav_dir = file_name
    print("Running Transcribe Command!")
    if args.language == '':
        cmd = [
            whisper_cli, '-m', model, '-f', wav_dir, '-osrt'
        ]
    else:
        cmd = [
                whisper_cli, '-m', model, '-f', wav_dir, '-osrt', '-l', args.language
            ]
    res = subprocess.run(
        cmd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return res.stdout


def main():
    if not args.video:
        print("No input file specified. Use -i to specify input file.")
        exit(1)
        
    print("Video to .wav")
    tqdm(video_to_wav16k())
    tqdm(whisper_transcribe())
    print("Finished outputting .srt")

if __name__ == "__main__":
    main()