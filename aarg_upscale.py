import argparse
import os
import subprocess

def quote_path(path):
    """Encloses the path in quotes to handle spaces, normalizing for Docker on Windows."""
    path = path.replace('\\', '/').rstrip('/')
    return f'"{path}"'

def upscale_video(input_path, height, keep_original, output_format, algorithm, model, output_dir=None):
    input_directory = os.path.dirname(input_path)
    filename = os.path.basename(input_path)
    file_root, file_extension = os.path.splitext(filename)

    if output_dir:
        # Write to a separate output directory; don't touch the input file
        temp_name = file_root + ".temp" + file_extension
        final_path = os.path.join(output_dir, filename)

        docker_command = (
            f'docker run --gpus all --rm'
            f' -v {quote_path(input_directory)}:/input:ro'
            f' -v {quote_path(output_dir)}:/output'
            f' ghcr.io/k4yt3x/video2x:6.4.0'
            f' -i {quote_path("/input/" + filename)}'
            f' -o {quote_path("/output/" + temp_name)}'
            f' -p {algorithm} -m {model} -h {height}'
        )

        print(f"Upscaling {filename} to {height}p with {algorithm} ({model})...")
        subprocess.run(docker_command, shell=True, check=True)

        # Rename temp file to final name in output directory
        os.rename(os.path.join(output_dir, temp_name), final_path)
    else:
        # Original behavior: write alongside input file
        output_path = os.path.join(input_directory, file_root + ".temp" + file_extension)
        original_file_output_path = os.path.join(input_directory, file_root + ".old" + file_extension)

        quoted_input_path = quote_path(os.path.basename(input_path))
        quoted_output_path = quote_path(os.path.basename(output_path))

        docker_command = f'docker run --gpus all --rm -v {quote_path(input_directory)}:/host ghcr.io/k4yt3x/video2x:6.4.0 -i {quoted_input_path} -o {quoted_output_path} -p {algorithm} -m {model} -h {height}'

        print(f"Upscaling {filename} to {height}p with {algorithm} ({model})...")
        subprocess.run(docker_command, shell=True, check=True)

        if keep_original:
            os.rename(input_path, original_file_output_path)
            os.rename(output_path, input_path)
        else:
            os.remove(input_path)
            os.rename(output_path, input_path)

def process_directory(directory, height, input_format, output_format, keep_original, algorithm, model, output_dir=None):
    for filename in os.listdir(directory):
        if filename.endswith(input_format):
            input_path = os.path.join(directory, filename)
            upscale_video(input_path, height, keep_original, output_format, algorithm, model, output_dir)

def process_file(file_path, height, output_format, keep_original, algorithm, model, output_dir=None):
    upscale_video(file_path, height, keep_original, output_format, algorithm, model, output_dir)

def main():
    parser = argparse.ArgumentParser(description='Upscale video files using Docker and video2x.')
    parser.add_argument('-d', '--directory', type=str, help='Directory containing video files to process')
    parser.add_argument('-p', '--path', type=str, help='Path to a single video file to process')
    parser.add_argument('-t', '--height', type=int, default=720, help='Height of the output file')
    parser.add_argument('-i', '--inputformat', type=str, help='Input file format to process (required with -d)')
    parser.add_argument('-o', '--outputformat', type=str, help='Desired output file format (defaults to same as input format if not specified)')
    parser.add_argument('-k', '--keep', action='store_true', help='Keep the original file, renamed with .temp extension')
    parser.add_argument('-a', '--algorithm', type=str, choices=['realesrgan', 'realcugan'], default=None, help='Upscaling algorithm/processor (default: realesrgan)')
    parser.add_argument('-m', '--model', type=str, default=None, help='Model name for the algorithm (default: realesr-animevideov3 for realesrgan, models-se for realcugan)')
    parser.add_argument('-O', '--output-dir', type=str, help='Output directory for upscaled files (default: same directory as input)')

    args = parser.parse_args()

    # Validate argument combinations
    if args.path and args.inputformat:
        parser.error("The -i/--inputformat option cannot be used with -p/--path.")
    if args.directory and not args.inputformat:
        parser.error("The -i/--inputformat option is required when using -d/--directory.")

    # Resolve algorithm and model defaults/validation
    model_to_algorithm = {
        'realesr-animevideov3': 'realesrgan',
        'realesrgan-x4plus': 'realesrgan',
        'realesrgan-x4plus-anime': 'realesrgan',
        'models-se': 'realcugan',
        'models-pro': 'realcugan',
        'models-nose': 'realcugan',
    }
    if args.algorithm and args.model:
        expected = model_to_algorithm.get(args.model)
        if expected and expected != args.algorithm:
            parser.error(f"Model '{args.model}' is not compatible with algorithm '{args.algorithm}' (expected '{expected}').")
    elif args.model and not args.algorithm:
        inferred = model_to_algorithm.get(args.model)
        if inferred:
            args.algorithm = inferred
        else:
            parser.error(f"Cannot infer algorithm from model '{args.model}'. Please specify -a/--algorithm.")
    if not args.algorithm:
        args.algorithm = 'realesrgan'
    if not args.model:
        args.model = 'realesr-animevideov3' if args.algorithm == 'realesrgan' else 'models-se'

    # If output format is not specified, infer it from input format or file path
    if not args.outputformat:
        if args.inputformat:
            args.outputformat = args.inputformat
        elif args.path:
            args.outputformat = '.' + args.path.rsplit('.', 1)[1]

    if args.output_dir and not os.path.isdir(args.output_dir):
        parser.error(f"Output directory does not exist: {args.output_dir}")

    if args.directory:
        process_directory(args.directory, args.height, args.inputformat, args.outputformat, args.keep, args.algorithm, args.model, args.output_dir)
    elif args.path:
        process_file(args.path, args.height, args.outputformat, args.keep, args.algorithm, args.model, args.output_dir)
    else:
        parser.error('Either a directory (-d) or a single file path (-p) must be provided.')

if __name__ == "__main__":
    main()
