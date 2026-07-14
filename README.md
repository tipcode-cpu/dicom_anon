# dicom-anon

DICOM 파일 헤더의 환자정보(PHI)를 익명화하는 CLI 도구입니다.

환자 이름·ID·생년월일·기관명 등 식별 태그를 비우고, private 태그를 제거하며,
Study/Series/SOP Instance UID를 새로 발급합니다.
**원본은 건드리지 않고 `_anon` 복사본을 새로 만듭니다.**

> ⚠️ **주의**: 헤더 태그만 익명화합니다. 픽셀(영상)에 새겨진(burned-in) 환자정보는
> 제거하지 못하니, 공유·발표 전 반드시 육안으로 확인하세요.

## 설치

```bash
pip install git+https://github.com/tipcode-cpu/dicom_anon.git
```

설치하면 `dicom-anon` 명령이 생깁니다. (격리 설치를 원하면 `pipx install git+...`)

## 사용법

```bash
# 파일 하나
dicom-anon study.dcm

# 여러 파일 / 폴더(스터디) 통째로
dicom-anon case1.dcm ./study_folder

# 출력 폴더 지정
dicom-anon ./study_folder -o ./anon_out
```

- 원본 옆에 `이름_anon.dcm` 이 생깁니다. `-o` 를 주면 그 폴더로 모읍니다.
- 원본 폴더가 읽기 전용(CD 등)이면 자동으로 `~/Desktop/dicom_anon` 에 저장됩니다.

## 클론해서 바로 실행 (설치 없이)

```bash
git clone https://github.com/tipcode-cpu/dicom_anon.git
cd dicom_anon
pip install -r requirements.txt
python anon_dicom.py study.dcm
```

## 익명화되는 태그

- **비움**: PatientName, PatientID, PatientBirthDate, PatientSex, 각종 Physician/Institution/Station 태그, AccessionNumber, StudyID 등
- **삭제**: PatientTelephoneNumbers, PatientMotherBirthName, MilitaryRank, 모든 private 태그
- **재발급**: StudyInstanceUID, SeriesInstanceUID, SOPInstanceUID
- **표시**: PatientIdentityRemoved = YES

## 라이선스

MIT
