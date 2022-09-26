import os

class unpak:
    __OFFSETS = []
    __FILE_SIZES = []

    def __init__(self, file: str) -> None:
        self.__OFFSETS = []
        self.__FILE_SIZES = []
        self.file = file

    def extract(self) -> None:
        def get_names() -> list:
            return f.read(self.__OFFSETS[0] - name_map).decode("932").split("\x00")[:-2]

        with open(self.file, "rb") as f:
            f.seek(4)
            file_count = int.from_bytes(f.read(4), "little")
            f.seek(28, 1)
            name_map = int.from_bytes(f.read(4), "little")
            for i in range(file_count):
                self.__OFFSETS.append(int.from_bytes(f.read(4), "little") * 4)
                self.__FILE_SIZES.append(int.from_bytes(f.read(4), "little"))
            
            dir = os.path.join(f"{self.file}_unpacked")
            if not os.path.exists(dir):
                os.mkdir(dir)
            for name, offset, size in zip(get_names(), self.__OFFSETS, self.__FILE_SIZES):
                with open(dir + "\\" + name, "wb") as out:
                    f.seek(offset)
                    out.write(f.read(size))