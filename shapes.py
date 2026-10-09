import pygame

# All shapes are defined in "unit" space: a point at distance 1.0 from the
# center ends up exactly on the object's radius when drawn. That way one model
# can be drawn at any size by multiplying by the radius.


# ---------------------------------------------------------------------------
# Asteroids
# ---------------------------------------------------------------------------

def _polar(points):
    # (angle in degrees, distance from center) -> Vector2
    return [pygame.Vector2(distance, 0).rotate(angle) for angle, distance in points]


def _smooth(points, passes=2):
    # Chaikin corner cutting: replaces every corner with two points close to it,
    # which rounds a jagged polygon into a lumpy, rock-like outline
    for _ in range(passes):
        smoothed = []
        for i in range(len(points)):
            a = points[i]
            b = points[(i + 1) % len(points)]
            smoothed.append(a.lerp(b, 0.25))
            smoothed.append(a.lerp(b, 0.75))
        points = smoothed
    return points


def _rock(points):
    return _smooth(_polar(points))


# Craters are (x, y, radius, has_rim). The rim is the inner crescent line.
SMALL_NOTCHED = {
    "outline": _rock([
        (0, 0.95), (35, 1.0), (70, 0.9), (100, 0.96), (140, 1.0), (180, 0.88),
        (215, 1.0), (245, 0.85), (270, 0.3), (295, 0.85), (325, 1.0),
    ]),
    "craters": [(0.0, 0.3, 0.32, True)],
}

SMALL_CHUNK = {
    "outline": _rock([
        (0, 1.0), (50, 0.82), (95, 1.0), (140, 0.78),
        (190, 1.0), (235, 0.85), (280, 0.98), (320, 0.8),
    ]),
    "craters": [(-0.1, 0.05, 0.36, True)],
}

MEDIUM_PEBBLE = {
    "outline": _rock([
        (0, 1.0), (25, 0.9), (50, 0.78), (75, 0.74), (100, 0.76), (125, 0.84),
        (150, 0.94), (175, 1.0), (200, 0.93), (225, 0.8), (250, 0.75),
        (275, 0.72), (300, 0.78), (325, 0.9), (345, 1.0),
    ]),
    "craters": [
        (0.42, 0.0, 0.26, True),
        (-0.38, 0.08, 0.28, True),
        (0.05, -0.42, 0.13, False),
    ],
}

MEDIUM_LUMPY = {
    "outline": _rock([
        (0, 0.95), (30, 0.84), (55, 1.0), (80, 0.82), (105, 0.94), (130, 1.0),
        (160, 0.8), (185, 0.96), (210, 1.0), (240, 0.82), (265, 0.95),
        (290, 1.0), (320, 0.82), (340, 0.92),
    ]),
    "craters": [
        (0.08, -0.08, 0.38, True),
        (-0.45, 0.42, 0.15, False),
        (0.45, 0.42, 0.14, False),
    ],
}

LARGE_ROUND = {
    "outline": _rock([
        (0, 0.92), (22, 1.0), (45, 0.88), (68, 0.97), (90, 0.84), (110, 0.95),
        (135, 1.0), (158, 0.86), (180, 0.96), (205, 0.85), (228, 1.0),
        (250, 0.9), (272, 0.8), (295, 0.93), (318, 1.0), (340, 0.88),
    ]),
    "craters": [
        (-0.2, -0.16, 0.36, True),
        (0.42, 0.25, 0.22, True),
        (0.36, -0.46, 0.13, False),
        (-0.42, 0.44, 0.14, False),
        (0.05, 0.58, 0.1, False),
    ],
}

LARGE_PEANUT = {
    "outline": _rock([
        (0, 0.98), (20, 1.0), (40, 0.92), (60, 0.8), (80, 0.66), (95, 0.68),
        (115, 0.85), (135, 0.97), (155, 1.0), (180, 0.95), (200, 1.0),
        (222, 0.9), (245, 0.76), (265, 0.64), (285, 0.72), (305, 0.88),
        (325, 0.97), (345, 1.0),
    ]),
    "craters": [
        (0.5, 0.04, 0.3, True),
        (-0.5, -0.06, 0.27, True),
        (-0.45, 0.45, 0.12, False),
        (0.48, -0.45, 0.12, False),
        (0.0, 0.04, 0.09, False),
    ],
}

# Two models per asteroid size (1 = small, 2 = medium, 3 = large)
ASTEROID_MODELS = {
    1: [SMALL_NOTCHED, SMALL_CHUNK],
    2: [MEDIUM_PEBBLE, MEDIUM_LUMPY],
    3: [LARGE_ROUND, LARGE_PEANUT],
}


# ---------------------------------------------------------------------------
# Ship
# ---------------------------------------------------------------------------
# Traced from the reference image in pixel coordinates (nose pointing up),
# then converted to unit space below. Only the left half is written out,
# the right half is a mirror image.

_SHIP_CENTER = (530, 495)

# Body outline: drawn filled black with a white edge
_SHIP_LEFT_BODY = [
    (530, 192),                            # nose
    (470, 300), (420, 398), (358, 468),    # leading edge
    (305, 545), (265, 595),
    (265, 672), (410, 672),                # back edge of the wing
    (410, 728), (470, 728), (478, 752),    # engine block
    (510, 752), (514, 775), (530, 775),
]

# Fins: drawn as solid white shapes, like the red fins in the reference
_SHIP_LEFT_FINS = [
    [(420, 398), (419, 290), (408, 270), (396, 292), (370, 436)],
    [(358, 468), (322, 440), (314, 406), (305, 424), (305, 545)],
    [(265, 595), (262, 512), (253, 488), (244, 512), (242, 582),
     (208, 600), (207, 568), (198, 543), (190, 568), (190, 672), (265, 672)],
]

# Thin panel lines on both sides: (points, closed)
_SHIP_LEFT_DETAILS = [
    ([(508, 240), (462, 420), (452, 662)], False),  # fuselage edge
]

# Shapes on the center line, so they are not mirrored
_SHIP_CENTER_FINS = [
    [(530, 106), (537, 160), (540, 205), (520, 205), (523, 160)],  # nose spike
]
_SHIP_CENTER_DETAILS = [
    ([(530, 205), (530, 492)], False),              # spine
    ([(508, 492), (552, 492), (578, 518), (578, 588),
      (552, 612), (508, 612), (482, 588), (482, 518)], True),  # cockpit
]


def _to_local(points):
    # Image y grows downward but the ship's nose should be +y, so flip it
    cx, cy = _SHIP_CENTER
    return [pygame.Vector2(x - cx, cy - y) for x, y in points]


def _mirror(points):
    return [pygame.Vector2(-p.x, p.y) for p in points]


def _build_ship():
    left = _to_local(_SHIP_LEFT_BODY)
    # Skip the nose and tail points (on the center line) so they aren't doubled
    right = _mirror(left[1:-1])
    right.reverse()
    body = left + right

    fins = []
    for points in _SHIP_LEFT_FINS:
        local = _to_local(points)
        fins.append(local)
        fins.append(_mirror(local))
    for points in _SHIP_CENTER_FINS:
        fins.append(_to_local(points))

    details = []
    for points, closed in _SHIP_LEFT_DETAILS:
        local = _to_local(points)
        details.append((local, closed))
        details.append((_mirror(local), closed))
    for points, closed in _SHIP_CENTER_DETAILS:
        details.append((_to_local(points), closed))

    # Scale so the farthest point of the ship sits exactly on the unit circle
    scale = max(p.length() for shape in [body] + fins for p in shape)
    body = [p / scale for p in body]
    fins = [[p / scale for p in fin] for fin in fins]
    details = [([p / scale for p in points], closed) for points, closed in details]
    return body, fins, details


SHIP_BODY, SHIP_FINS, SHIP_DETAILS = _build_ship()
