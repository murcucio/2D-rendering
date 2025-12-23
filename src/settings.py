from dataclasses import dataclass

@dataclass
class AppConfig:
    monitor_index: int = 0
    target_fps: int = 60

    # 기본 처리 다운스케일 (0.5~0.8 사이가 보통 실사용 타협점)
    scale: float = 0.6

    # 초기 필터
    filter_name: str = "toon"

    # pixel filter params
    pixel_size: int = 4
    palette_levels: int = 10

    # toon filter params
    edge_strength: int = 80
    color_levels: int = 8
