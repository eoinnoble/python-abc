import argparse
import multiprocessing
import os
from typing import List

from joblib import Parallel, delayed

from python_abc.calculate import calculate_abc
from python_abc.output import AnalysisResult, render_json, render_text


def main():
    parser = argparse.ArgumentParser(
        prog="python-abc",
        description="""\
            A python implementation of the ABC Software metric:
            https://en.wikipedia.org/wiki/ABC_Software_Metric
        """,
    )
    parser.add_argument("path", nargs=1, type=str, help="path to directory or file")
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="display AST output for each element in the parsed tree",
    )
    parser.add_argument(
        "--cores",
        dest="cores",
        type=int,
        default=multiprocessing.cpu_count(),
        help="number of cores to use",
    )
    parser.add_argument(
        "--sort",
        dest="sort",
        action="store_true",
        help="sort files from highest to lowest magnitude",
    )
    parser.add_argument(
        "--verbose", dest="verbose", action="store_true", help="display marked-up file",
    )
    parser.add_argument(
        "--format",
        dest="format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )

    args = vars(parser.parse_args())
    if args["format"] == "json" and (args["debug"] or args["verbose"]):
        parser.error("--format json cannot be used with --debug or --verbose")

    path = args["path"][0]
    files: List[str] = []

    if os.path.isdir(path):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            files += [
                os.path.join(dirpath, file)
                for file in filenames
                if file.endswith(".py")
            ]
    else:
        files.append(path)

    def analyze_file(filename):
        with open(filename, "r") as f:
            source = f.read()

            try:
                abc_vector = calculate_abc(source, args["debug"], args["verbose"])
            except SyntaxError:
                return AnalysisResult(filename, None, 0.0)
            else:
                return AnalysisResult(
                    filename, abc_vector, abc_vector.get_magnitude_value()
                )

    output = Parallel(n_jobs=args["cores"])(
        delayed(analyze_file)(filename) for filename in files
    )

    if args["sort"] is True:
        output.sort(key=lambda result: result.sort_magnitude, reverse=True)

    if args["format"] == "json":
        print(render_json(path, output))
    else:
        print(render_text(output))


if __name__ == "__main__":
    main()
