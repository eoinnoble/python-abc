import argparse
import os
from typing import List, Optional, Tuple

from python_abc.calculate import calculate_abc
from python_abc.vector import Vector


def main():
    parser = argparse.ArgumentParser(
        prog="python-abc",
        description="""\
            A python implementation of the ABC Sofware metric:
            https://en.wikipedia.org/wiki/ABC_Software_Metric
        """,
    )
    parser.add_argument(
        "path", nargs=1, type=str, help="path to directory or file"
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        type=bool,
        default=False,
        help="display AST output for each element in the parsed tree",
    )
    parser.add_argument(
        "--sort",
        dest="sort",
        type=bool,
        default=False,
        help="sort files from highest to lowest magnitude",
    )
    parser.add_argument(
        "--verbose",
        dest="verbose",
        type=bool,
        default=False,
        help="display marked-up file",
    )

    args = vars(parser.parse_args())
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

    max_path_length = max(len(file) for file in files)

    output: List[Tuple[str, Optional[Vector], float]] = []
    for filename in files:
        with open(filename, "r") as f:
            source = f.read()

            try:
                abc_vector = calculate_abc(source, args["debug"], args["verbose"])
            except SyntaxError:
                output.append((filename, None, 0.0))
            else:
                output.append((filename, abc_vector, abc_vector.get_magnitude_value()))

    if args["sort"] is True:
        output.sort(key=lambda x: x[2], reverse=True)

    for filename, vector, _ in output:
        if vector is None:
            print(f"{filename:<{max_path_length}} {'Unable to parse AST':>26}")
        else:
            print(f"{filename:<{max_path_length}} {vector.magnitude:>26}")


if __name__ == "__main__":
    main()
