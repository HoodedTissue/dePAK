import struct, os

class repak:
    '''
    header
    DataStart   uint32
    FileCount   uint32
    IDStart     uint32
    BlockSize   uint32
    Padding (?) uint32[4] 
    Unk1        uint32
    NameMap     uint32

    file entry
    Ukn1        uint32 (offset / 4)
    FileSize    uint32
    '''
    __data_offset = 0
    __file_names = []
    __name_map_start = 0

    def __init__(self, orig_file: str) -> None:
        self.__data_offset = 0
        self.__file_names = []
        self.__name_map_start = 0
        self.read_orig_file(orig_file)

    def read_orig_file(self, file: str) -> list:
        with open(file, "rb") as f:
            self.__data_offset = int.from_bytes(f.read(4), "little")
            f.seek(36)
            self.__name_map_start = int.from_bytes(f.read(4), "little")
            f.seek(self.__name_map_start, 0)
            self.__file_names = f.read(self.__data_offset - self.__name_map_start).decode("932").split("\x00")[:-2]

    def unk(self, offset: int) -> int:
        if offset % 4 == 0:
            return offset
        else:
            return offset + (offset % 4)
    
    def repack(self, dir: str, out_file: str) -> None:
        with open(out_file, "wb") as out:
            offset = self.__data_offset

            #write header info
            out.write(struct.pack("<IIII16xII", self.__data_offset, len(os.listdir(dir)), 1, 4, 512, self.__name_map_start))

            #write file table
            for file in self.__file_names:
                file_size = os.path.getsize(os.path.join(dir, file))
                out.write(struct.pack("<II", int(self.unk(offset)/4), file_size))
                offset += self.unk(file_size)

            #write name table
            for file in self.__file_names:
                out.write(struct.pack("<%dsx" % len(file), bytes(file, "932")))
            out.write(struct.pack("<%dx" % (self.__data_offset - out.tell())))

            #start writing file data
            for file in self.__file_names:
                with open(os.path.join(dir, file), "rb") as f:
                    out.write(f.read())
                    if out.tell() % 4 != 0:
                        out.write(struct.pack("<%dx" % ((out.tell() % 4))))