# Author: Human beings feat. ChatGPT with GitHub Copilot
from dsfuzzer import DsFuzzer
from fuzzdb import FuzzDb

def main():
    ds = {"a": 1, "b": [2, 3], "c": {"d": 4, "e": [5, 6]}}
    dsfuzzer = DsFuzzer()
    # https://github.com/fuzzdb-project/fuzzdb/blob/master/attack/all-attacks/all-attacks-xplatform.txt
    fuzzlist = FuzzDb("all-attacks-xplatform.txt").get_fuzzlist()
    for fz in fuzzlist:
        fuzzed_dss = dsfuzzer.fuzz(ds, fz)
        for fuzzed_ds, path in fuzzed_dss:
            print(f"{fuzzed_ds}")

if __name__ == "__main__":
    main()
