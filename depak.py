import os
import sys

if len(sys.argv) < 2:
    print("dePAK.py <PAK file>")
    exit(0)

with open(sys.argv[1], 'rb') as pak_file:
    print(f"decompiling {sys.argv[1]}...")
    offset = int.from_bytes(pak_file.read(4), "little")
    file_count = int.from_bytes(pak_file.read(4), "little")
    pak_file.seek(28, 1)
    name_start_offset = int.from_bytes(pak_file.read(4), "little") #not too sure if this is correct, may just be coincidence with test file
    pak_file.seek(4, 1)
    offsets = [offset]
    sizes = []
    names = []
    for i in range(file_count):
        size = int.from_bytes(pak_file.read(4), "little")
        pak_file.seek(4, 1)
        sizes.append(size)
        offset = offset + size
        if (offset % 4 != 0): #add padding if offset is not divisible by 4
            offset += offset % 4
        offsets.append(offset)
    offsets = offsets[:-1] #extra value exists because initial offset is already added to array
    pak_file.seek(name_start_offset) # go to name start offset and start reading all file names
    file_names = pak_file.read(offsets[0] - name_start_offset).decode('932')
    names = file_names.split("\x00")

    if (len(names) != file_count): #make sure no trailing bytes are left behind
        names = names[:-(len(names) - file_count)] 
    
    #start writing data
    print("writing data...")
    dir = os.path.join(f"{sys.argv[1]}_unpacked")
    if not os.path.exists("dir"):
        os.mkdir(dir)
    for name, offset, size in zip(names, offsets, sizes):
        pak_file.seek(offset)
        data = pak_file.read(size)
        with open(dir + "/" + name, "wb") as output_file:
            output_file.write(data)
    print("finished")