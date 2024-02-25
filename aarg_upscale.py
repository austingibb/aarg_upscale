import argparse
import os
import subprocess

def upscale_video(input_path, output_path, height, keep_original):
    # Construct the Docker command
    docker_command = f"sudo docker run --gpus all -it --rm -v {os.path.dirname(input_path)}:/host ghcr.io/k4yt3x/video2x:5.0.0-beta6 -i {os.path.basename(input_path)} -o {os.path.basename(output_path)} -p3 upscale -h {height} -a waifu2x -n3"

    # Execute the Docker command
    print(f"Upscaling {os.path.basename(input_path)}...")
    subprocess.run(docker_command, shell=True, check=True)

    if not keep_original:
        # Remove the original file
        os.remove(input_path)
        os.rename(output_path, input_path) 
    else:
        # Rename the original file
        old_file_path = input_path + ".old" + os.path.splitext(input_path)[1]
        os.rename(input_path, old_file_path)

def process_directory(directory, height, file_format, keep_original):
    for filename in os.listdir(directory):
        if filename.endswith(file_format):
            input_path = os.path.join(directory, filename)
            temp_output_filename = filename.replace(file_format, f".temp{file_format}")
            temp_output_path = os.path.join(directory, temp_output_filename)
            upscale_video(input_path, temp_output_path, height, keep_original)

def process_file(file_path, height, keep_original):
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    file_format = os.path.splitext(file_path)[1]
    temp_output_filename = filename.replace(file_format, f".temp{file_format}")
    temp_output_path = os.path.join(directory, temp_output_filename)
    upscale_video(file_path, temp_output_path, height, keep_original)

def main():
    parser = argparse.ArgumentParser(description='Upscale video files using Docker and video2x.')
    parser.add_argument('-d', '--directory', type=str, help='Directory containing video files to process')
    parser.add_argument('-p', '--path', type=str, help='Path to a single video file to process')
    parser.add_argument('-t', '--height', type=int, default=720, help='Height of the output file')
    parser.add_argument('-f', '--format', type=str, default='.mp4', help='File format to process')
    parser.add_argument('-k', '--keep', action='store_true', help='Keep the original file with a .old extension')

    args = parser.parse_args()

    if args.directory:
        process_directory(args.directory, args.height, args.format, args.keep)
    elif args.path:
        process_file(args.path, args.height, args.keep)
    else:
        parser.error('Either a directory (-d) or a single file path (-p) must be provided.')

if __name__ == "__main__":
    main()
