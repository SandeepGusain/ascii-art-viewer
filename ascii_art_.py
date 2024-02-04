import argparse
import cv2
from PIL import Image
import time


def clear_terminal():
    # Clear the terminal screen using ANSI escape code to
    # draw the next frame (in case input media is a video)
    print("\033[H\033[3J", end="")


def media_to_ascii(media_path: str, output_width: int, frame_rate: int) -> None:
    # works for reading images as well so far
    cap = cv2.VideoCapture(media_path)

    # Loop until entire video is read
    while True:
        # Read single frame
        ret, frame = cap.read()

        if ret:
            color_converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(color_converted)

            # Resize the image to adjust to desired width and scale height to aspect ratio accordingly
            aspect_ratio = img.height / img.width
            new_height = int(output_width * aspect_ratio)
            img = img.resize((output_width, new_height))

            # ASCII character (ordered in decreasing brightness/intensity)
            ascii_chars = "@%#*+=-:. "

            # Convert pixels to ASCII char
            ascii_image = ""
            for y in range(new_height):
                for x in range(output_width):
                    r, g, b = img.getpixel((x, y))
                    intensity = sum([r, g, b]) / 3 / 255.0

                    # ANSI escape codes for coloring the ascii characters based on the pixel rgb values
                    char = f"\033[38;2;{r};{g};{b}m{ascii_chars[int(intensity * (len(ascii_chars) - 1))]}!\033[0m"
                    ascii_image += char
                ascii_image += "\n"

            print(ascii_image)
            clear_terminal()

            # wait to draw the next frame based on the desired fps (frames per second)
            time.sleep(1 / frame_rate)
        else:
            break

        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    # Release the video capture object
    cap.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert media to ASCII art.")
    parser.add_argument("input_file", help="Path to the input media file")
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        default=50,
        help="Width of ASCII art",
    )
    parser.add_argument(
        "-fps",
        "--frame_rate",
        type=int,
        default=60,
        help="Frame rate of the media being played",
    )

    args = parser.parse_args()
    media_to_ascii(args.input_file, args.width, args.frame_rate)
