from repak import repak
from unpak import unpak
import sys

def main() -> None:
    if len(sys.argv) == 1:
        print_usage()
    
    try:
        operation = sys.argv[1]
        if operation == "unpack":
            unpack(sys.argv[2])
        elif operation == "repack":
            repack(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("Unknown operation: %s" % operation)
            print_usage()
    except Exception as e:
        print(e)
        exit(1)

def unpack(file: str) -> None:
    print(f"Unpacking {file} to {file}_unpacked...")
    unpack = unpak(file)
    unpack.extract()
    print("Finished")

def repack(dir: str, out_file: str, orig_file: str) -> None:
    print(f"Repacking {dir} to {out_file}...")
    repacker = repak(orig_file)
    repacker.repack(dir, out_file)
    print("Finished")

def print_usage() -> None:
    print("Usage:")
    print("    main.py unpack <in_file>")
    print("    main.py repack <dir> <out_file> <orig_file>")
    exit(0)

if __name__ == "__main__":
    main()
