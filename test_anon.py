# 셀프체크: 합성 DICOM 하나 만들어 익명화 후 PHI가 지워졌는지 확인
import os, tempfile, pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
from anon_dicom import anonymize


def _make_dcm(path):
    ds = Dataset()
    ds.PatientName = "홍길동"
    ds.PatientID = "12345"
    ds.PatientBirthDate = "19700101"
    ds.InstitutionName = "영남대병원"
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()
    ds.SOPInstanceUID = generate_uid()
    ds.add_new(0x00090010, "LO", "PRIVATE_VENDOR")  # private tag
    fm = FileMetaDataset()
    fm.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.7"
    fm.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
    fm.TransferSyntaxUID = ExplicitVRLittleEndian
    ds.file_meta = fm
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    ds.save_as(path, write_like_original=False)


def test_anonymize_blanks_phi():
    with tempfile.TemporaryDirectory() as d:
        src, out = os.path.join(d, "in.dcm"), os.path.join(d, "out.dcm")
        _make_dcm(src)
        orig_uid = pydicom.dcmread(src).StudyInstanceUID
        anonymize(src, out)
        r = pydicom.dcmread(out)
        assert r.PatientName == ""
        assert r.PatientID == ""
        assert r.InstitutionName == ""
        assert r.PatientIdentityRemoved == "YES"
        assert r.StudyInstanceUID != orig_uid          # UID 재발급
        assert 0x00090010 not in r                      # private 제거
    print("OK")


if __name__ == "__main__":
    test_anonymize_blanks_phi()
