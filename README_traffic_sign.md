# Traffic Sign Alert Application

## 개발 목적
교통약자 보호구역에서의 사고를 예방하기 위해 도로 표지판을 실시간으로 인식하여 운전자에게 경고하는 애플리케이션입니다. 이 프로그램은 컴퓨터 비전 기술을 활용하여 도로 영상을 분석하고, 교통약자 보호구역 표지판을 탐지 및 표시합니다.

## 구체적 구현 내용
1. **표지판 등록**
   - `child.png`, `elder.png`, `disabled.png` 등 미리 정의된 표지판 이미지를 불러옵니다.
   - 표지판 이미지는 프로그램 내에서 키포인트 및 기술자를 추출하여 저장됩니다.

2. **도로 영상 입력**
   - 도로 영상 파일을 사용자가 선택하여 불러옵니다.
   - 입력된 영상은 SIFT 알고리즘으로 분석됩니다.

3. **표지판 인식**
   - SIFT 알고리즘으로 도로 영상에서 키포인트를 감지하고 등록된 표지판과 매칭합니다.
   - FLANN 기반 매칭을 활용하여 좋은 매칭을 추출합니다.
   - 호모그래피를 통해 도로 영상 위에 표지판 위치를 투영합니다.

4. **결과 시각화 및 경고**
   - 매칭 결과를 도로 영상에 표시하고, 경고음으로 운전자에게 알립니다.

## 개발 환경
- **프로그래밍 언어**: Python 3.11
- **GUI 프레임워크**: PyQt6
- **컴퓨터 비전 라이브러리**: OpenCV
- **경고음 처리**: winsound (Windows 전용)
- **의존성 관리**: pip

## 프로젝트 구조
```
traffic_sign_alert/
├── traffic_sign_alert.py      # 메인 애플리케이션 소스 코드
├── child.png                  # 어린이 보호구역 표지판 이미지
├── elder.png                  # 노인 보호구역 표지판 이미지
├── disabled.png               # 장애인 보호구역 표지판 이미지
├── README.md                  # 문서 파일
├── pyproject.toml             # 종속성과 설정 파일
```

## 터미널 명령어

### 사전 준비
1. Python 3.11 설치
2. 필수 라이브러리 설치:
   ```bash
   pip install pyqt6 opencv-python-headless winsound
   ```
3. `child.png`, `elder.png`, `disabled.png` 파일을 프로젝트 디렉터리에 배치

### 프로그램 실행
#### Python 스크립트 실행
1. 프로젝트 디렉터리로 이동:
   ```bash
   cd /path/to/traffic-sign-alert
   ```
2. 애플리케이션 실행:
   ```bash
   python traffic_sign_alert.py
   ```

#### EXE 파일 빌드 및 실행
1. PyInstaller 설치:
   ```bash
   pip install pyinstaller
   ```
2. EXE 파일 생성:
   ```bash
   pyinstaller --onefile --noconsole traffic_sign_alert.py
   ```
3. EXE 파일 실행:
   ```bash
   ./dist/traffic_sign_alert.exe
   ```

---