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
    __DATA_OFFSET = 0
    __FILE_NAMES = []
    __NAME_MAP_START = 0

    def __init__(self, orig_file: str) -> None:
        self.__DATA_OFFSET = 0
        self.__FILE_NAMES = []
        self.__NAME_MAP_START = 0
        self.read_orig_file(orig_file)

    def read_orig_file(self, file: str) -> list:
        with open(file, "rb") as f:
            self.__DATA_OFFSET = int.from_bytes(f.read(4), "little")
            f.seek(36)
            self.__NAME_TBL_START = int.from_bytes(f.read(4), "little")
            f.seek(self.__NAME_TBL_START, 0)
            self.__FILE_NAMES = f.read(self.__DATA_OFFSET - self.__NAME_TBL_START).decode("932").split("\x00")[:-2]

    def unk(self, offset: int) -> int:
        if offset % 4 == 0:
            return offset
        else:
            return offset + (offset % 4)
    
    def repack(self, dir: str, out_file: str) -> None:
        with open(out_file, "wb") as out:
            offset = self.__DATA_OFFSET

            #write header info
            out.write(struct.pack("<IIII16xII", self.__DATA_OFFSET, len(os.listdir(dir)), 1, 4, 512, self.__NAME_TBL_START))

            #write file table
            for file in self.__FILE_NAMES:
                file_size = os.path.getsize(os.path.join(dir, file))
                out.write(struct.pack("<II", int(self.unk(offset)/4), file_size))
                offset += self.unk(file_size)

            #write name table
            for file in self.__FILE_NAMES:
                out.write(struct.pack("<%dsx" % len(file), bytes(file, "932")))
            out.write(struct.pack("<%dx" % (self.__DATA_OFFSET - out.tell())))

            #start writing file data
            for file in self.__FILE_NAMES:
                with open(os.path.join(dir, file), "rb") as f:
                    out.write(f.read())
                    if out.tell() % 4 != 0:
                        out.write(struct.pack("<%dx" % ((out.tell() % 4))))