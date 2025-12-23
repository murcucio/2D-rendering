import time
import cv2
import numpy as np

import dxcam

from filters import FILTERS
from settings import AppConfig

def _clamp(v, lo, hi):
    return max(lo, min(hi, v))

def main():
    cfg = AppConfig()

    # DXCAM 초기화
    camera = dxcam.create(output_idx=cfg.monitor_index)
    if camera is None:
        raise RuntimeError("dxcam.create() failed. Monitor index를 확인하세요.")

    # 캡처 시작
    camera.start(target_fps=cfg.target_fps, video_mode=True)

    win_name = "2D Filter Viewer (ESC: quit | 1:none 2:pixel 3:toon | +/- scale | [ ] pixel_size | ; ' palette | , . edge | k l color_levels)"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win_name, 1280, 720)

    last = time.time()
    frames = 0
    fps = 0.0

    try:
        while True:
            frame = camera.get_latest_frame()
            if frame is None:
                time.sleep(0.001)
                continue

            # dxcam은 BGRA로 주는 경우가 많음
            if frame.shape[2] == 4:
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            else:
                frame_bgr = frame

            # 필터 적용
            fname = cfg.filter_name
            f = FILTERS.get(fname, FILTERS["none"])

            if fname == "pixel":
                out = f(frame_bgr, scale=cfg.scale, pixel_size=cfg.pixel_size, palette_levels=cfg.palette_levels)
            elif fname == "toon":
                out = f(frame_bgr, scale=cfg.scale, edge_strength=cfg.edge_strength, color_levels=cfg.color_levels)
            else:
                out = f(frame_bgr, scale=cfg.scale)

            # HUD 텍스트
            frames += 1
            now = time.time()
            if now - last >= 1.0:
                fps = frames / (now - last)
                frames = 0
                last = now

            hud = out.copy()
            cv2.putText(hud, f"filter={cfg.filter_name}  scale={cfg.scale:.2f}  fps={fps:.1f}",
                        (18, 36), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2, cv2.LINE_AA)

            if cfg.filter_name == "pixel":
                cv2.putText(hud, f"pixel_size={cfg.pixel_size}  palette_levels={cfg.palette_levels}",
                            (18, 72), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2, cv2.LINE_AA)

            if cfg.filter_name == "toon":
                cv2.putText(hud, f"edge={cfg.edge_strength}  color_levels={cfg.color_levels}",
                            (18, 72), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2, cv2.LINE_AA)

            cv2.imshow(win_name, hud)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break

            # 필터 전환
            if key == ord('1'):
                cfg.filter_name = "none"
            elif key == ord('2'):
                cfg.filter_name = "pixel"
            elif key == ord('3'):
                cfg.filter_name = "toon"

            # scale 조절 (+/-)
            elif key == ord('=') or key == ord('+'):
                cfg.scale = _clamp(cfg.scale + 0.05, 0.25, 1.0)
            elif key == ord('-') or key == ord('_'):
                cfg.scale = _clamp(cfg.scale - 0.05, 0.25, 1.0)

            # pixel_size 조절 [ ]
            elif key == ord('['):
                cfg.pixel_size = _clamp(cfg.pixel_size - 1, 1, 32)
            elif key == ord(']'):
                cfg.pixel_size = _clamp(cfg.pixel_size + 1, 1, 32)

            # palette_levels 조절 ; '
            elif key == ord(';'):
                cfg.palette_levels = _clamp(cfg.palette_levels - 1, 2, 32)
            elif key == ord("'"):
                cfg.palette_levels = _clamp(cfg.palette_levels + 1, 2, 32)

            # toon edge 조절 , .
            elif key == ord(','):
                cfg.edge_strength = _clamp(cfg.edge_strength - 5, 10, 200)
            elif key == ord('.'):
                cfg.edge_strength = _clamp(cfg.edge_strength + 5, 10, 200)

            # toon color_levels 조절 k l
            elif key == ord('k'):
                cfg.color_levels = _clamp(cfg.color_levels - 1, 2, 16)
            elif key == ord('l'):
                cfg.color_levels = _clamp(cfg.color_levels + 1, 2, 16)

    finally:
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
