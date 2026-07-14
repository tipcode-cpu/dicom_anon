# dicom_anon

DICOM 파일 헤더의 환자정보(PHI)를 익명화하는 간단한 CLI 도구입니다.

환자 이름·ID·생년월일·기관명 등 식별 태그를 비우고, private 태그를 제거하며,
Study/Series/SOP Instance UID를 새로 발급합니다. 원본은 건드리지 않고 `_anon` 파일을 새로 만듭니다.

> ⚠️ **주의**: 헤더 태그만 익명화합니다. 픽셀 데이터에 새겨진(burned-in) 환자정보나
> 비표준 위치의 PHI는 제거하지 않습니다. 배포·공유 전 반드시 육안 검수하세요.

## 설치

```bash
pip install -r requirements.txt
```

## 사용법

```bash
# 파일 하나
python anon_dicom.py study.dcm

# 여러 파일 / 폴더(스터디) 통째로
python anon_dicom.py case1.dcm ./study_folder

# 출력 폴더 지정
python anon_dicom.py ./study_folder -o ./anon_out
```

Windows에서 exe로 빌드하면 파일을 exe 위에 **드래그&드롭**해서도 쓸 수 있습니다.

```bash
pyinstaller --onefile anon_dicom.py
```

## 익명화되는 태그

- **비움**: PatientName, PatientID, PatientBirthDate, PatientSex, 각종 Physician/Institution/Station 태그, AccessionNumber, StudyID 등
- **삭제**: PatientTelephoneNumbers, PatientMotherBirthName, MilitaryRank, 모든 private 태그
- **재발급**: StudyInstanceUID, SeriesInstanceUID, SOPInstanceUID
- **표시**: PatientIdentityRemoved = YES

## 라이선스

MIT
