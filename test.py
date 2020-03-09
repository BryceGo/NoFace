import ffmpeg
import numpy as np
import sys
import os

def main(filename, output_filename):
# https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#tensorflow-streaming
# https://kkroening.github.io/ffmpeg-python/
    try:
        base_path = sys._MEIPASS + "\\"
    except:
        base_path = os.path.abspath(".") + "\\"


    probe = ffmpeg.probe(filename, cmd=base_path + "ffprobe")
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    width = int(video_info['width'])
    height = int(video_info['height'])
    num_frames = int(video_info['nb_frames'])
    dimensions = 3

    process1 = (
        ffmpeg
        .input(filename)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run_async(pipe_stdout=True, cmd=base_path + "ffmpeg")
    )

    process2 = (
    ffmpeg
    .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
    .output(output_filename, pix_fmt='yuv420p')
    .overwrite_output()
    .run_async(pipe_stdin=True, cmd=base_path + "ffmpeg")
    )

    while True:
        in_bytes = process1.stdout.read(width*height*dimensions)

        if not in_bytes:
            break

        in_frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([height, width, dimensions])
            )

        # Process in_frame here

        # ------

        process2.stdin.write(
            in_frame
            .astype(np.uint8)
            .tobytes()
            )

    process2.stdin.close()
    process1.wait()
    process2.wait()


    audio = ffmpeg.input(filename)
    video = ffmpeg.input(output_filename)

    # audio = audio.audio.filter()

    (
        ffmpeg
        .output(video.video, audio.audio, "output.mp4", shortest=None, vcodec='copy')
        .overwrite_output()
        .run()
    )


    return
    


if __name__ == '__main__':
    main(sys.argv[1])