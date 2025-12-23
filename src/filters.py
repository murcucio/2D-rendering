import cv2
import numpy as np

def _resize_for_speed(frame_bgr: np.ndarray, scale: float) -> np.ndarray:
    if scale >= 0.999:
        return frame_bgr
    h, w = frame_bgr.shape[:2]
    nh, nw = max(1, int(h * scale)), max(1, int(w * scale))
    return cv2.resize(frame_bgr, (nw, nh), interpolation=cv2.INTER_AREA)

def _resize_back(frame_bgr: np.ndarray, target_shape) -> np.ndarray:
    th, tw = target_shape[:2]
    return cv2.resize(frame_bgr, (tw, th), interpolation=cv2.INTER_NEAREST)

def filter_none(frame_bgr: np.ndarray, scale: float = 1.0) -> np.ndarray:
    small = _resize_for_speed(frame_bgr, scale)
    if small.shape[:2] != frame_bgr.shape[:2]:
        return _resize_back(small, frame_bgr.shape)
    return small

def filter_pixel(frame_bgr: np.ndarray, scale: float = 0.6, pixel_size: int = 4, palette_levels: int = 10) -> np.ndarray:
    """
    픽셀화 + 팔레트 제한(양자화).
    - scale: 처리 해상도 다운스케일(지연 감소)
    - pixel_size: 픽셀 블록 크기
    - palette_levels: 채널별 양자화 단계(작을수록 더 '2D/레트로' 느낌)
    """
    small = _resize_for_speed(frame_bgr, scale)
    h, w = small.shape[:2]

    # 1) Pixelation: 축소 후 최근접 확대
    pw = max(1, w // pixel_size)
    ph = max(1, h // pixel_size)
    tiny = cv2.resize(small, (pw, ph), interpolation=cv2.INTER_AREA)
    pix = cv2.resize(tiny, (w, h), interpolation=cv2.INTER_NEAREST)

    # 2) Palette quantization
    levels = max(2, int(palette_levels))
    step = 256 // levels
    q = (pix // step) * step
    q = np.clip(q, 0, 255).astype(np.uint8)

    # 원래 해상도로 복원
    if q.shape[:2] != frame_bgr.shape[:2]:
        q = _resize_back(q, frame_bgr.shape)
    return q

def filter_toon(frame_bgr: np.ndarray, scale: float = 0.6, edge_strength: int = 80, color_levels: int = 8) -> np.ndarray:
    """
    간단 토ゥーン 느낌:
    - bilateral로 평탄화
    - 에지(윤곽) 추출 후 합성
    - 색 단계 제한
    """
    small = _resize_for_speed(frame_bgr, scale)

    # 1) Smooth / flatten
    smooth = cv2.bilateralFilter(small, d=7, sigmaColor=60, sigmaSpace=60)

    # 2) Edge detection
    gray = cv2.cvtColor(smooth, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(gray, threshold1=edge_strength, threshold2=edge_strength * 2)

    # Edge를 두껍게
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    # 3) Color quantization (banding)
    levels = max(2, int(color_levels))
    step = 256 // levels
    quant = (smooth // step) * step
    quant = np.clip(quant, 0, 255).astype(np.uint8)

    # 4) Composite edges (검은 윤곽)
    edges_inv = cv2.bitwise_not(edges)
    edges_inv_bgr = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)
    toon = cv2.bitwise_and(quant, edges_inv_bgr)

    if toon.shape[:2] != frame_bgr.shape[:2]:
        toon = _resize_back(toon, frame_bgr.shape)
    return toon

FILTERS = {
    "none": filter_none,
    "pixel": filter_pixel,
    "toon": filter_toon,
}
