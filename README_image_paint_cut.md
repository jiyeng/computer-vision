# Image Paint & Cut Tool

## 개발 목적
이미지를 불러와 특정 영역을 페인팅하고, GrabCut 알고리즘을 사용하여 이미지를 오림(crop)하는 도구입니다. 사용자 친화적인 GUI를 통해 간단하게 이미지를 편집할 수 있습니다.

## 구체적 구현 내용
1. **이미지 불러오기**
   - 사용자가 이미지를 선택하여 GUI에 로드합니다.

2. **페인팅 기능**
   - 마우스 좌클릭으로 전경(Foreground) 영역을, 우클릭으로 배경(Background) 영역을 지정합니다.
   - 브러시 크기를 조정하여 세밀한 작업이 가능합니다.

3. **오림 기능**
   - GrabCut 알고리즘을 사용하여 전경과 배경을 분리합니다.
   - 지정된 영역에 따라 이미지를 크롭하고 결과를 표시합니다.

4. **결과 저장**
   - 편집된 이미지를 사용자가 지정한 경로에 저장할 수 있습니다.

## 개발 환경
- **프로그래밍 언어**: Python 3.11
- **GUI 프레임워크**: PyQt6
- **컴퓨터 비전 라이브러리**: OpenCV
- **의존성 관리**: pip

## 프로젝트 구조
```
image_paint_cut_tool/
├── image_paint_cut_tool.py    # 메인 애플리케이션 소스 코드
├── README.md                  # 문서 파일
```

## 터미널 명령어

### 사전 준비
1. Python 3.11 설치
2. 필수 라이브러리 설치:
   ```bash
   pip install pyqt6 opencv-python-headless
   ```

### 프로그램 실행
#### Python 스크립트 실행
1. 프로젝트 디렉터리로 이동:
   ```bash
   cd /path/to/image-paint-cut-tool
   ```
2. 애플리케이션 실행:
   ```bash
   python image_paint_cut_tool.py
   ```

#### EXE 파일 빌드 및 실행
1. PyInstaller 설치:
   ```bash
   pip install pyinstaller
   ```
2. EXE 파일 생성:
   ```bash
   pyinstaller --onefile --noconsole image_paint_cut_tool.py
   ```
3. EXE 파일 실행:
   ```bash
   ./dist/image_paint_cut_tool.exe
   ```
