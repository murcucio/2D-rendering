# game-2d-filter (Capture-based 2D Style Viewer)

This project captures your screen in real-time and applies lightweight "2D-like" filters (toon / pixel) to reduce 3D discomfort.
It does NOT inject into game processes. It works as a separate viewer window.

## Features
- Real-time capture using dxcam (Windows Desktop Duplication)
- Filters:
  - Toon-lite (edges + color banding)
  - Pixel (pixelation + palette quantization)
- Hotkeys for filter switching and tuning

## Requirements
- Windows 10/11
- Python 3.10+

## Install
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt



---

## 7) 실행 방법 (VSCode)
1. 위 구조로 파일 생성
2. VSCode 터미널에서
   - `python -m venv .venv`
   - `.\.venv\Scripts\activate`
   - `pip install -r requirements.txt`
   - `python .\src\main.py`
3. 게임은 **Borderless / Windowed**로 실행 권장(캡처 안정성)

---

## 8) 현실적인 한계와 다음 개선(정직하게)
이 MVP는 “작동”하는 데 초점을 맞췄고, 다음이 남습니다.

- **지연**: CPU 필터(OpenCV)라서 PC 성능에 따라 체감될 수 있음  
  → 다음 단계는 **GPU 셰이더(DirectX/Metal/Vulkan)로 필터 이식**이 정석
- **UI 보호**: 미니맵/글자가 같이 뭉개질 수 있음  
  → 다음 단계는 UI 영역 마스킹(간단하게는 화면 하단/구석 영역 약적용)
- **오버레이**: “게임 위에 덮기”는 별도 단계(호환성/리스크 상승)

---

## 다음 질문 없이, 제가 제안하는 “바로 다음 버전”
당장 가족분이 플레이하기 편하도록, 제가 다음 중 하나로 코드를 확장해 드릴 수 있습니다(원하시면 그대로 이어서 드립니다).

1) **저지연 모드**: 필터를 더 가볍게(윤곽선만 / 팔레트만) + 프레임 타이밍 안정화  
2) **UI 보호**: 화면 특정 영역은 필터 약하게 적용(텍스트 깨짐 감소)  
3) **게임 창만 캡처**: 전체 화면이 아니라 특정 창 핸들만 선택(더 안정적)  

진행을 위해 딱 한 가지만 확인하겠습니다.  
가족분이 보는 화면은 **같은 PC에서 같은 모니터로 보실 건가요**, 아니면 **가족분 PC로 스트리밍(디스코드/OBS)해서 보실 건가요**?  
(같은 PC면 “별도 뷰어 창”이 가장 간단하고, 원격이면 “OBS 가상 출력”이 더 적합합니다.)
::contentReference[oaicite:0]{index=0}
