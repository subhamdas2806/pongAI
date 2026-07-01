import pygame
import random

BG = (5, 5, 12)
PHOSPHOR = (160, 170, 255)
PHOSPHOR_BRIGHT = (210, 215, 255)
PHOSPHOR_DIM = (70, 75, 130)
GLOW = (90, 100, 220)
ACCENT = (130, 140, 255)
RED = (220, 70, 90)

_FONT_CACHE = {}
_SCANLINE_CACHE = {}
_VIGNETTE_CACHE = {}


def get_font(size, bold=False):
    key = (size, bold)
    if key not in _FONT_CACHE:
        font = None
        for name in ("Courier New", "Consolas", "Lucida Console", "monospace"):
            try:
                font = pygame.font.SysFont(name, size, bold=bold)
                if font:
                    break
            except Exception:
                continue
        if font is None:
            font = pygame.font.SysFont(None, size, bold=bold)
        _FONT_CACHE[key] = font
    return _FONT_CACHE[key]


def draw_glow_text(surface, text, size, pos, color=PHOSPHOR_BRIGHT, center=False, bold=False, glow_strength=3):
    font = get_font(size, bold=bold)
    glow_color = tuple(min(255, c) for c in GLOW)

    base = font.render(text, True, color)
    rect = base.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos

    glow_surf = font.render(text, True, glow_color)
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)):
        offset_rect = rect.copy()
        offset_rect.x += dx
        offset_rect.y += dy
        glow_surf_alpha = glow_surf.copy()
        glow_surf_alpha.set_alpha(35)
        surface.blit(glow_surf_alpha, offset_rect)

    surface.blit(base, rect)
    return rect


def draw_bracket_frame(surface, rect, color=PHOSPHOR, thickness=2, corner_len=18):
    x, y, w, h = rect
    pts = [
        ((x, y + corner_len), (x, y), (x + corner_len, y)),
        ((x + w - corner_len, y), (x + w, y), (x + w, y + corner_len)),
        ((x, y + h - corner_len), (x, y + h), (x + corner_len, y + h)),
        ((x + w - corner_len, y + h), (x + w, y + h), (x + w, y + h - corner_len)),
    ]
    for p1, p2, p3 in pts:
        pygame.draw.lines(surface, color, False, [p1, p2, p3], thickness)


def draw_dotted_line(surface, start, end, color=PHOSPHOR_DIM, dash=4, gap=4, width=1):
    x1, y1 = start
    x2, y2 = end
    length = max(1, int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5))
    dx = (x2 - x1) / length
    dy = (y2 - y1) / length
    pos = 0
    drawing = True
    while pos < length:
        seg = dash if drawing else gap
        if drawing:
            sx, sy = x1 + dx * pos, y1 + dy * pos
            ex, ey = x1 + dx * min(pos + dash, length), y1 + dy * min(pos + dash, length)
            pygame.draw.line(surface, color, (sx, sy), (ex, ey), width)
        pos += seg
        drawing = not drawing


def _get_scanline_overlay(width, height):
    key = (width, height)
    if key not in _SCANLINE_CACHE:
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        for y in range(0, height, 2):
            pygame.draw.line(overlay, (0, 0, 0, 90), (0, y), (width, y))
        for y in range(0, height, 7):
            pygame.draw.line(overlay, (140, 150, 255, 18), (0, y), (width, y))
        _SCANLINE_CACHE[key] = overlay
    return _SCANLINE_CACHE[key]


def _get_vignette(width, height):
    key = (width, height)
    if key not in _VIGNETTE_CACHE:
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        max_dist = ((width / 2) ** 2 + (height / 2) ** 2) ** 0.5
        steps = 10
        for i in range(steps):
            t = i / steps
            alpha = int(140 * (t ** 2))
            rect_w = int(width * (1 - t * 0.5))
            rect_h = int(height * (1 - t * 0.5))
            rect = pygame.Rect(0, 0, rect_w, rect_h)
            rect.center = (width // 2, height // 2)
            pygame.draw.rect(overlay, (0, 0, 0, max(0, alpha - 120)), rect, 0,
                              border_radius=max(rect_w, rect_h) // 2)
        corner = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(corner, (0, 0, 0, 120), corner.get_rect())
        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(mask, (255, 255, 255, 255),
                             (-width * 0.3, -height * 0.3, width * 1.6, height * 1.6))
        corner.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        overlay.blit(corner, (0, 0))
        _VIGNETTE_CACHE[key] = overlay
    return _VIGNETTE_CACHE[key]


def apply_crt_overlay(surface, noise_strength=6):

    width, height = surface.get_size()

    surface.blit(_get_scanline_overlay(width, height), (0, 0))
    surface.blit(_get_vignette(width, height), (0, 0))

    if noise_strength > 0:
        noise = pygame.Surface((width, height), pygame.SRCALPHA)
        for _ in range(int(width * height * 0.0015)):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            shade = random.randint(0, 60)
            noise.set_at((x, y), (shade, shade, shade + 20, random.randint(15, 50)))
        surface.blit(noise, (0, 0))

    if random.random() < 0.04:
        flicker = pygame.Surface((width, height), pygame.SRCALPHA)
        flicker.fill((150, 160, 255, random.randint(4, 12)))
        surface.blit(flicker, (0, 0))