# randomAttack.py
import os, tempfile, time, random, string, shutil, pathlib

NOTE_NAMES = [
    "README_TO_DECRYPT.txt",
    "HOW_TO_DECRYPT_FILES.txt",
    "RECOVER_FILES.txt"
]

def make_dummy_files(root, n=60):
    exts = [".docx", ".xlsx", ".pdf", ".txt", ".jpg", ".png"]
    data = b"This is harmless dummy data for detection testing.\n"
    for i in range(n):
        fname = "file_{:03d}{}".format(i, random.choice(exts))
        p = os.path.join(root, fname)
        with open(p, "wb") as f:
            f.write(data * random.randint(1, 10))

def fake_encrypt_rename(root):
    # Simulate speed of ransomware by renaming quickly
    for p in pathlib.Path(root).glob("*.*"):
        if p.is_file():
            p.rename(p.with_suffix(p.suffix + ".encrypted"))
            # tiny delay to generate multiple rapid events
            time.sleep(0.02)

def drop_ransom_note(root):
    note = os.path.join(root, random.choice(NOTE_NAMES))
    with open(note, "w", encoding="utf-8") as f:
        f.write(
            "Your files are (fake) encrypted for detection testing ONLY.\n"
            "No real encryption occurred. This is a harmless simulator."
        )

def main():
    # Use an isolated temp folder
    lab_root = tempfile.mkdtemp(prefix="ransomware-sim-")
    print("Simulator folder:", lab_root)
    make_dummy_files(lab_root, n=80)
    time.sleep(0.5)
    fake_encrypt_rename(lab_root)
    drop_ransom_note(lab_root)
    print("Done. Review your Wazuh/Sysmon alerts. When finished, delete:", lab_root)

if __name__ == "__main__":
    main()
