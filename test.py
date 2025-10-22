import os

def get_dir_size(path):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_dir_size(entry.path)
    return total

db_size_mb = get_dir_size('./chroma_db') / 1024 / 1024
print(f"ChromaDB size: {db_size_mb:.2f} MB")