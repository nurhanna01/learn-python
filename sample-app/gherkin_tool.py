from pathlib import Path
OUTPUT_DIR = (Path(__file__).parent / "output").resolve()

def write_gherkin(filename: str, content:str) -> str :
    """Simpan test case dalam format Gherkin ke file .md.
    nama_file: nama file saja tanpa folder, misalnya 'login.md'.
    isi: teks Gherkin lengkap"""
    try :
        print(f"checkkk file pertama:{OUTPUT_DIR}")
        OUTPUT_DIR.mkdir(exist_ok=True)
        print(f"checkkk file kedua:{OUTPUT_DIR}")
        name = Path(filename).name
        print(f"checkkk name:{name}")
        if not name.endswith(".md"):
            name = name + ".md"

        destination = (OUTPUT_DIR/name).resolve()
        print(f"destination name:{destination}")

        if OUTPUT_DIR not in destination.parents:
            return "Ditolak"
        destination.write_text(content,encoding="utf-8")

        print("ghrekin tersimpan")

        return f"Berhasil tersimpan ke {destination}"
    except Exception as e:
        print(f"error gherkin tool :{e}") 