#!/usr/bin/env python3
# anon_dicom.py  —  DICOM 헤더 PHI 익명화 CLI (드래그&드롭도 지원)
import sys, os, argparse, pydicom
from pydicom.uid import generate_uid

BLANK = [
    "PatientName", "PatientID", "PatientBirthDate", "PatientSex",
    "OtherPatientIDs", "OtherPatientNames", "PatientAddress",
    "ReferringPhysicianName", "PerformingPhysicianName", "PhysiciansOfRecord",
    "OperatorsName", "InstitutionName", "InstitutionAddress",
    "StationName", "AccessionNumber", "StudyID",
    "InstitutionalDepartmentName",
]
DELETE = ["PatientTelephoneNumbers", "PatientMotherBirthName", "MilitaryRank"]


def anonymize(path, out):
    ds = pydicom.dcmread(path)
    ds.remove_private_tags()
    for kw in BLANK:
        if kw in ds:
            ds.data_element(kw).value = ""
    for kw in DELETE:
        if kw in ds:
            del ds[kw]
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()
    ds.SOPInstanceUID = generate_uid()
    ds.PatientIdentityRemoved = "YES"
    ds.DeidentificationMethod = "pydicom basic tag blanking"
    ds.save_as(out)
    return ds


def _suffix(idx):
    return "_anon" + (f"_{idx}" if idx else "")   # 여러 파일이면 번호 붙임


def out_path(path, idx=0, outdir=None):
    root, ext = os.path.splitext(path)
    if outdir:
        base = os.path.basename(root)
        return os.path.join(outdir, base + _suffix(idx) + (ext or ".dcm"))
    return root + _suffix(idx) + (ext or ".dcm")


def fallback_path(path, idx=0):
    # 원본 폴더가 읽기 전용(CD/네트워크 등)일 때 → 바탕화면\dicom_anon 으로
    desk = os.path.join(os.path.expanduser("~"), "Desktop", "dicom_anon")
    os.makedirs(desk, exist_ok=True)
    root, ext = os.path.splitext(os.path.basename(path))
    return os.path.join(desk, root + _suffix(idx) + (ext or ".dcm"))


def collect(paths):
    # 파일은 그대로, 폴더는 하위 파일 전부 펼침 (DICOM 스터디 = 폴더)
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                files.extend(os.path.join(root, n) for n in names)
        else:
            files.append(p)
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="DICOM 헤더의 환자정보(PHI)를 익명화합니다.")
    ap.add_argument("paths", nargs="*", help="DICOM 파일 또는 폴더")
    ap.add_argument("-o", "--outdir", help="출력 폴더 (기본: 원본 옆에 _anon)")
    args = ap.parse_args(argv)

    files = collect(args.paths)
    if not files:
        print("사용법: anon_dicom 파일.dcm [파일2 폴더 ...] [-o 출력폴더]")
        print("        (또는 exe 위에 DICOM 파일을 드래그해서 놓기)")
        return 0
    if args.outdir:
        os.makedirs(args.outdir, exist_ok=True)

    multi = len(files) > 1
    ok = 0
    for i, f in enumerate(files, 1):
        idx = i if multi else 0
        try:
            try:
                o = out_path(f, idx, args.outdir)
                anonymize(f, o)
            except PermissionError:
                o = fallback_path(f, idx)     # 원본 폴더 쓰기 금지 → 바탕화면
                anonymize(f, o)
            print(f"[완료] {os.path.basename(f)}  ->  {o}")
            ok += 1
        except Exception as e:
            print(f"[건너뜀] {os.path.basename(f)}: {e}")
    print(f"\n{ok}/{len(files)} 완료.")
    return 0 if ok else 1


if __name__ == "__main__":
    code = main()
    # 더블클릭/드래그로 실행됐을 땐 창이 바로 닫히지 않게
    if sys.stdin and sys.stdin.isatty() and len(sys.argv) <= 1:
        try:
            input("\nEnter 키를 누르면 닫힙니다...")
        except EOFError:
            pass
    sys.exit(code)
