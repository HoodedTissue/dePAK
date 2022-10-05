from repak import repak
from unpak import unpak
import sys

def main() -> None:
    if len(sys.argv) == 1:
        print_usage()
    
    try:
        operation = sys.argv[1]
        if operation == "unpack":
            unpack(sys.argv)
        elif operation == "repack":
            repack(sys.argv)
        else:
            print(f"Unknown operation: {operation}")
            print_usage()
    except Exception as e:
        print(e)
        exit(1)

def unpack(args: list) -> None:
    if (len(args) != 3):
        print_usage()
        return()
    print(f"Unpacking {args[2]} to {args[2]}_unpacked...")
    unpack = unpak(args[2])
    unpack.extract()
    print("Finished")

def repack(args: list) -> None:
    if (len(args) != 5):
        print_usage()
        return()

    print(f"Repacking {args[2]} to {args[3]}...")
    repacker = repak(args[4])
    repacker.repack(args[2], args[3])
    print("Finished")

def print_usage() -> None:
    print("Usage:")
    print("    main.py unpack <in_file>")
    print("    main.py repack <dir> <out_file> <orig_file>")
    exit(0)

if __name__ == "__main__":
    main()