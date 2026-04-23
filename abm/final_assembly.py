"""
End-to-end final assembly:

  1. Run fill_manuscript.py to inject numeric results into the manuscript.
  2. Run visualize_robustness_all.py to produce all figures.
  3. Call build_pdf.py to regenerate manuscript.pdf.

Invoke after all four robustness CSVs exist in results/.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

def run(cmd, cwd):
    print(f"\n>>> {cmd}\n")
    r = subprocess.run(cmd, cwd=cwd, shell=True)
    if r.returncode != 0:
        print(f"!!! exited {r.returncode}")
        return False
    return True


def main():
    ok = True
    ok &= run(f'"{sys.executable}" fill_manuscript.py', HERE)
    ok &= run(f'"{sys.executable}" visualize_robustness_all.py', HERE)
    ok &= run(f'"{sys.executable}" bootstrap_analysis.py', HERE)
    ok &= run(f'"{sys.executable}" build_pdf.py',
              os.path.join(ROOT, "submission"))
    print("\nDONE" if ok else "\nINCOMPLETE (see errors above)")


if __name__ == "__main__":
    main()
