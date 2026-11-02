from pathlib import Path
OUTPUT_DIR = (Path(__file__).parent / "output").resolve()

def write_gherkin(filename: str, content:str) -> str :
    """Simpan test case dalam format Gherkin ke file .md.
    nama_file: nama file saja tanpa folder, misalnya 'login.md'.
    isi: teks Gherkin lengkap"""
    try :
        OUTPUT_DIR.mkdir(exist_ok=True)
        name = filename
        if not name.endswith(".md"):
            name = name + ".md"

        destination = (OUTPUT_DIR/name).resolve()

        if OUTPUT_DIR not in destination.parents:
            return "Ditolak"
        destination.write_text(content,encoding="utf-8")

        return f"Berhasil tersimpan ke {destination}"
    except Exception as e:
        print(f"error gherkin tool :{e}") 
        raise e