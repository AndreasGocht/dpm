from __future__ import annotations
import shutil


def yes_no():
    answer = ""
    while answer == "":
        answer = input("Is this okay? (y/N): ")
        if answer in {"y", "n"}:
            break
        print(f"Unknown: {answer}. please select y or n")
        answer = ""
    return answer == "y"


def select_helper(msg: str, options: list[str]) -> int:
    print(msg)
    for num, option in enumerate(options):
        print(f"\t{num + 1}. {option}")
    i = None
    while i is None:
        try:
            i = int(input("Select one:"))
        except ValueError:
            print("Not a Number!")
            continue
        if i < 1 or i > len(options):
            print("Invalid input!")
            i = None
    return i - 1


class ProgressBar:
    def __init__(self, total_num):
        self.total_num = total_num

    def update(self, string, amount):
        print("\r", end="")
        width_term = shutil.get_terminal_size()[0]
        len_string = len(string) + 3
        max_bar_width = max(width_term - len_string, 0)
        len_bar = int(max_bar_width * amount / self.total_num)
        len_spaces = width_term - len_bar - len_string
        spaces = " " * len_spaces
        hashes = "#" * len_bar
        print(f"{string} [{hashes}{spaces}]", end="", flush=True)


BYTE_IN_KIB = 1024


class UrlretrieveProgressHelper:
    def __init__(self):
        self.progress_bar = None

    def __call__(self, count, blockSize, totalSize):
        if totalSize == -1:
            print("\r", end="")
            print(self.string_helper(count, blockSize, totalSize), end="")
            return
        if self.progress_bar is None:
            self.progress_bar = ProgressBar(totalSize)
        string = self.string_helper(count, blockSize, totalSize)
        self.progress_bar.update(string, count * blockSize)

    def string_helper(self, count, blockSize, totalSize):
        if totalSize < BYTE_IN_KIB:
            return f"{count * blockSize}/{totalSize} Bytes"
        elif totalSize < BYTE_IN_KIB * BYTE_IN_KIB:
            blockSize = blockSize / BYTE_IN_KIB
            totalSize = totalSize / BYTE_IN_KIB
            return f"{count * blockSize}/{totalSize} KiB"
        elif totalSize < BYTE_IN_KIB * BYTE_IN_KIB * BYTE_IN_KIB:
            blockSize = blockSize / BYTE_IN_KIB / BYTE_IN_KIB
            totalSize = totalSize / BYTE_IN_KIB / BYTE_IN_KIB
            return f"{count * blockSize:.2f}/{totalSize:.2f} MiB"
