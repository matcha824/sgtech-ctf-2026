import struct
import zlib

INPUT_IMAGE="mysterious-murals-no-embedded-key.png"
OUTPUT_IMAGE="mysterious-murals.png"

METADATA = {
    "Software": "Adobe Photoshop 25.5",
    "Creation Time": "2026-04-18T14:32:07Z",
    "Author": "Steve",
    "Source": "F(Jj%ATV^!Gs,YGE--5CATVTsAo(mg1,]",
    "Comment": "Urban street art photography collection"
}

def create_text_chunk(keyword: str, text: str) -> bytes:
    data = keyword.encode("latin-1") + b"\x00" + text.encode("latin-1")
    chunk_type = b"tEXt"
    chunk_length = struct.pack(">I", len(data))
    crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
    return chunk_length + chunk_type + data + crc

def embed_metadata(input_path: str, output_path: str, metadata: dict):
    with open(input_path, "rb") as f:
        png_data = f.read()
    
    png_signature = b"\x89PNG\r\n\x1a\n"
    if not png_data.startswith(png_signature):
        raise ValueError("Not a valid PNG file")
    
    pos = 8
    insert_pos = None
    while pos < len(png_data):
        length = struct.unpack(">I", png_data[pos:pos + 4])[0]
        chunk_type = png_data[pos + 4:pos + 8]
        if chunk_type in (b"IDAT", b"IEND"):
            insert_pos = pos
            break
        pos += 12 + length

    if insert_pos is None:
        raise ValueError("No IDAT or IEND chunk found")
    
    # Build text chunks
    chunks = b""
    for keyword, value in metadata.items():
        chunks += create_text_chunk(keyword, value)
    
    # Assemble PNG
    new_png = png_data[:insert_pos] + chunks + png_data[insert_pos:]

    with open(output_path, "wb") as f:
        f.write(new_png)
    
    print(f"Written: {output_path}")
    print(f"Embedded {len(metadata)} metadata fields:")
    for k, v in metadata.items():
        print(f" {k}: {v}")

def verify(filepath: str):
    with open(filepath, "rb") as f:
        data = f.read()

    pos = 8
    print(f"\n--- Verification: {filepath} ---")
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4: pos + 8].decode("ascii")
        chunk_data = data[pos + 4: pos + 8 + length]

        if chunk_type == "tEXt":
            null_idx = chunk_data.index(b"\x00")
            keyword = chunk_data[:null_idx].decode("latin-1")
            text = chunk_data[null_idx + 1:].decode("latin-1")
            print(f"[{keyword}] {text}")

        pos += 12 + length

if __name__ == "__main__":
    embed_metadata(INPUT_IMAGE, OUTPUT_IMAGE, METADATA)
    verify(OUTPUT_IMAGE)