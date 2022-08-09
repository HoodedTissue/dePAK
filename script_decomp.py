import sys

if len(sys.argv) < 2:
    print('script_decomp.py <script file>')
    exit(0)

with open(sys.argv[1], "rb") as script_file:
    print(f"decompiling {sys.argv[1]}...")
    data = script_file.read()
    res = [i for i in range(len(data)) if data.startswith(b"\x00\x1F\x03", i)]
    string_len = []
    strings = []
    for i in res:
        script_file.seek(i - 1)
        string_len.append(int.from_bytes(script_file.read(1), "little"))
    for i in range(len(res)):
        script_file.seek(res[i] + 9)
        string = script_file.read(string_len[i] - 9).decode('932', errors='ignore')
        if (string.startswith("\x60")):
            string = string[1:]
            '''string = string [:-3] 
            if (len(string) != 0):
                strings.append(string)''' #uncomment to get rid of null strings
            strings.append(string[:-3]) 
        else:
            '''string = string [:-3]
            if (len(string) != 0):
                strings.append(string)''' #uncomment to get rid of null strings
            strings.append(string[:-3]) 
    with open(sys.argv[1] + ".txt", "w", encoding="932") as output:
        print("writing data...")
        for i in strings:
            output.writelines(i + "\n")
        print("finished")
    
