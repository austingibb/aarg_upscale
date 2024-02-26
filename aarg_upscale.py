import argparse
import os
import subprocess

def quote_path(path):
    """Encloses the path in quotes to handle spaces."""
    return f'"{path}"'

def upscale_video(input_path, height, keep_original, output_format):
    directory = os.path.dirname(input_path)
    filename = os.path.basename(input_path)
    file_root, file_extension = os.path.splitext(filename)
    output_path = os.path.join(directory, file_root + ".temp" + file_extension)  # Temp output path
    original_file_output_path = os.path.join(directory, file_root + ".old" + file_extension)

    # Correctly quote the input and output paths to handle spaces
    quoted_input_path = quote_path(os.path.basename(input_path))
    quoted_output_path = quote_path(os.path.basename(output_path))

    # Construct the Docker command without /host/ prefix and with quoted paths
    docker_command = f'docker run --gpus all -it --rm -v {quote_path(directory)}:/host ghcr.io/k4yt3x/video2x:5.0.0-beta6 -i {quoted_input_path} -o {quoted_output_path} -p3 upscale -h {height} -a waifu2x -n3'

    # Execute the Docker command
    print(f"Upscaling {os.path.basename(input_path)} to {height}p...")
    subprocess.run(docker_command, shell=True, check=True)

    if keep_original:
        # Rename the original file with a .old extension
        os.rename(input_path, original_file_output_path)
        # Rename the upscaled (temp) file to the original file name
        os.rename(output_path, input_path)
    else:
        # Remove the original file
        os.remove(input_path)
        # Rename the upscaled (temp) file to the original file name
        os.rename(output_path, input_path)

def process_directory(directory, height, input_format, output_format, keep_original):
    for filename in os.listdir(directory):
        if filename.endswith(input_format):
            input_path = os.path.join(directory, filename)
            upscale_video(input_path, height, keep_original, output_format)

def process_file(file_path, height, output_format, keep_original):
    upscale_video(file_path, height, keep_original, output_format)

def main():
    parser = argparse.ArgumentParser(description='Upscale video files using Docker and video2x.')
    parser.add_argument('-d', '--directory', type=str, help='Directory containing video files to process')
    parser.add_argument('-p', '--path', type=str, help='Path to a single video file to process')
    parser.add_argument('-t', '--height', type=int, default=720, help='Height of the output file')
    parser.add_argument('-i', '--inputformat', type=str, help='Input file format to process (required with -d)')
    parser.add_argument('-o', '--outputformat', type=str, help='Desired output file format (defaults to same as input format if not specified)')
    parser.add_argument('-k', '--keep', action='store_true', help='Keep the original file, renamed with .temp extension')

    args = parser.parse_args()

    # Validate argument combinations
    if args.path and args.inputformat:
        parser.error("The -i/--inputformat option cannot be used with -p/--path.")
    if args.directory and not args.inputformat:
        parser.error("The -i/--inputformat option is required when using -d/--directory.")

    # If output format is not specified, infer it from input format or file path
    if not args.outputformat:
        if args.inputformat:
            args.outputformat = args.inputformat
        elif args.path:
            args.outputformat = '.' + args.path.rsplit('.', 1)[1]

    if args.directory:
        process_directory(args.directory, args.height, args.inputformat, args.outputformat, args.keep)
    elif args.path:
        process_file(args.path, args.height, args.outputformat, args.keep)
    else:
        parser.error('Either a directory (-d) or a single file path (-p) must be provided.')

if __name__ == "__main__":
    main()
