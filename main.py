#!venv/bin python3
# TODO: Accept video url to curl
# TODO: Use a deep summarizer
"""
Summarizes a video with an srt track
"""

__author__ = "Josh Winton"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import subprocess
import re
import pysrt
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
LANGUAGE = "english"
SENTENCES_COUNT = 10


def make_srt(input_file, output_file):
    """
    Given a video file as input_file, output srt to oiutput_file
    """
    subprocess.call(["ffmpeg", "-y", "-i", input_file, output_file])


def srt_to_txt(input_file, output_file):
    """
    Given an srt file as input_file, write the text component to output_file
    """
    subs = pysrt.open(input_file)
    full_text = ""
    for sub in subs:
        full_text += re.sub('<[^<]+?>', ' ', sub.text).replace("\n", " ")
    with open(output_file, "w", encoding="UTF-8") as file:
        file.write(full_text)


def summarize_txt(input_file, output_file):
    """
    Given a text file, summarize it
    """
    # open txt file
    parser = PlaintextParser.from_file(input_file, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary = ""
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        summary += str(sentence)

    with open(output_file, "w", encoding="UTF-8") as file:
        file.write(summary)



def main(args):
    # Get srt from mp4 using ffmpeg
    make_srt(args.input_file, "out.srt")
    # Get txt from srt
    srt_to_txt("out.srt", "out.txt")
    # Summarize txt
    summarize_txt("out.txt", args.output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("input_file", help="Required positional argument")

    parser.add_argument("output_file")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument("-v",
                        "--verbose",
                        action="count",
                        default=0,
                        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
