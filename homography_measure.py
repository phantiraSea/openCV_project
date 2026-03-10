import cv2
import numpy as np
import math

# =========================
# Config
# =========================
IMG_PATH = r"Add your file path"

BOARD_W_CM = 70.6
BOARD_H_CM = 51.2
PX_PER_CM = 10  # 10 pixels represent 1 cm in warped view

OUT_W = int(BOARD_W_CM * PX_PER_CM)
OUT_H = int(BOARD_H_CM * PX_PER_CM)

# =========================
# Globals
# =========================
src_img = cv2.imread(IMG_PATH)
if src_img is None:
    raise FileNotFoundError(f"Cannot read image: {IMG_PATH}")

stage = "BOARD"   # BOARD -> click 4 corners, MEASURE -> click 2 points
board_pts = []
measure_pts = []
homography_matrix = None
warped_img = None

win_src = "1) Click 4 board corners (TL, TR, BR, BL) "
win_warp = "2) Click 2 points to measure (warped) "


def draw_poly(img_draw, pts, closed=False, color=(0, 255, 0), thickness=2):
    if len(pts) >= 2:
        for i in range(len(pts) - 1):
            cv2.line(img_draw, pts[i], pts[i + 1], color, thickness)

    if closed and len(pts) == 4:
        cv2.polylines(img_draw, [np.array(pts, dtype=np.int32)], True, color, thickness)


def draw_points(img_draw, pts, color=(0, 255, 0)):
    for (x, y) in pts:
        cv2.circle(img_draw, (x, y), 6, color, -1)


def compute_homography_and_warp():
    global homography_matrix, warped_img

    src = np.float32(board_pts)
    dst = np.float32([
        [0, 0],
        [OUT_W - 1, 0],
        [OUT_W - 1, OUT_H - 1],
        [0, OUT_H - 1]
    ])

    homography_matrix = cv2.getPerspectiveTransform(src, dst)
    warped_img = cv2.warpPerspective(src_img, homography_matrix, (OUT_W, OUT_H))

    cv2.namedWindow(win_warp, cv2.WINDOW_NORMAL)
    cv2.imshow(win_warp, warped_img)
    cv2.setMouseCallback(win_warp, on_mouse_warp)

    print("\nHomography created.")
    print(f"Warped size: {OUT_W} x {OUT_H} px (scale = {PX_PER_CM} px/cm)")
    print("Now click 2 points in the warped window to measure distance.\n")


def distance_cm(p1, p2):
    dx_cm = (p2[0] - p1[0]) / PX_PER_CM
    dy_cm = (p2[1] - p1[1]) / PX_PER_CM
    return math.sqrt(dx_cm**2 + dy_cm**2)


def on_mouse_src(event, x, y, flags, param):
    global stage, board_pts

    if event != cv2.EVENT_LBUTTONDOWN:
        return

    if stage == "BOARD" and len(board_pts) < 4:
        board_pts.append((x, y))
        print(f"[Board click {len(board_pts)}] x={x}, y={y}")

        vis = src_img.copy()
        draw_points(vis, board_pts, (0, 255, 0))
        draw_poly(vis, board_pts, closed=False, color=(0, 255, 0))

        if len(board_pts) == 4:
            draw_poly(vis, board_pts, closed=True, color=(0, 255, 0))
            stage = "MEASURE"
            cv2.imshow(win_src, vis)
            compute_homography_and_warp()
        else:
            cv2.imshow(win_src, vis)


def on_mouse_warp(event, x, y, flags, param):
    global measure_pts, warped_img

    if event != cv2.EVENT_LBUTTONDOWN or warped_img is None:
        return

    if len(measure_pts) < 2:
        measure_pts.append((x, y))
        print(f"[Measure click {len(measure_pts)}] x={x}, y={y}")

    vis = warped_img.copy()
    draw_points(vis, measure_pts, (0, 0, 255))

    if len(measure_pts) == 2:
        cv2.line(vis, measure_pts[0], measure_pts[1], (0, 0, 255), 2)
        d = distance_cm(measure_pts[0], measure_pts[1])

        mid = (
            (measure_pts[0][0] + measure_pts[1][0]) // 2,
            (measure_pts[0][1] + measure_pts[1][1]) // 2
        )

        cv2.putText(
            vis,
            f"{d:.2f} cm",
            (mid[0] + 10, mid[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )

        print(f"==> Distance: {d:.2f} cm\n")
        measure_pts = []

    cv2.imshow(win_warp, vis)


def reset_all():
    global stage, board_pts, measure_pts, homography_matrix, warped_img

    stage = "BOARD"
    board_pts = []
    measure_pts = []
    homography_matrix = None
    warped_img = None

    try:
        cv2.destroyWindow(win_warp)
    except:
        pass

    cv2.imshow(win_src, src_img.copy())
    print("\n[Reset] Click 4 board corners again.\n")


# =========================
# Main UI
# =========================
print("Instructions:")
print("1) In SOURCE window, click 4 board corners in order: TL, TR, BR, BL")
print("2) A WARPED window will appear")
print("3) In WARPED window, click 2 points to measure distance in cm")
print("Hotkeys: r = reset, u = undo last point, q/ESC = quit\n")

cv2.namedWindow(win_src, cv2.WINDOW_NORMAL)
cv2.imshow(win_src, src_img.copy())
cv2.setMouseCallback(win_src, on_mouse_src)

while True:
    key = cv2.waitKey(20) & 0xFF

    if key in (27, ord('q')):
        break

    elif key == ord('r'):
        reset_all()

    elif key == ord('u'):
        if stage == "BOARD" and board_pts:
            removed = board_pts.pop()
            print(f"[Undo board] removed {removed}")

            vis = src_img.copy()
            draw_points(vis, board_pts, (0, 255, 0))
            draw_poly(vis, board_pts, closed=False, color=(0, 255, 0))
            cv2.imshow(win_src, vis)

        elif stage == "MEASURE" and measure_pts and warped_img is not None:
            removed = measure_pts.pop()
            print(f"[Undo measure] removed {removed}")

            vis = warped_img.copy()
            draw_points(vis, measure_pts, (0, 0, 255))
            cv2.imshow(win_warp, vis)

cv2.destroyAllWindows()
