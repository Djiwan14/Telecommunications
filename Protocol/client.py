import sys
import struct

def unpack_and_print(filename, struct_format):
    with open(filename, 'rb') as file:
        data = file.read(struct.calcsize(struct_format))
        unpacked_data = struct.unpack(struct_format, data)
        print(unpacked_data)

def pack_and_print(data, struct_format):
    packed_data = struct.pack(struct_format, *data)
    print(packed_data)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Error: Please provide 4 file paths as arguments.")
        sys.exit(1)

    # Task 1 - Read and unpack binary files
    unpack_and_print(sys.argv[1], "9s i f")
    unpack_and_print(sys.argv[2], "f ? c")
    unpack_and_print(sys.argv[3], "c i 9s")
    unpack_and_print(sys.argv[4], "f 9s ?")

    # Task 2 - Pack values in binary format
    pack_and_print(("elso".encode().ljust(12, b'\x00'), 80, True), "12s i ?")
    pack_and_print((83.5, False, bytes('X', 'ascii')), "f ? c")
    pack_and_print((71, "masodik".encode().ljust(10, b'\x00'), 90.9), "i 10s f")
    pack_and_print((bytes('Z', 'ascii'), 102, "harmadik".encode().ljust(13, b'\x00')), "c i 13s")
