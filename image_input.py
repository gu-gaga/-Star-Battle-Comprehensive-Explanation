from PIL import Image, ImageDraw
import math

def get_matrix(image_path):
    img = Image.open(image_path).convert('RGB')
    draw = ImageDraw.Draw(img)
    width, height = img.size

    BORDER_COLOR = (189, 153, 243)  # #BD99F3

    # --- 调优参数 ---
    HEIGHT_ADJUST = 0.90
    COLOR_TOLERANCE = 2  # 颜色欧几里得距离容差，2能完美区分10种不同色块
    # ----------------

    x_coords, y_coords = [], []
    scan_top, scan_bottom = int(height * 0.15), int(height * 0.85)

    for y in range(scan_top, scan_bottom, 3):
        for x in range(0, width, 3):
            p = img.getpixel((x, y))
            if all(abs(p[i] - BORDER_COLOR[i]) < 30 for i in range(3)):
                x_coords.append(x)
                y_coords.append(y)

    if not x_coords:
        print("未检测到边框！")
        return None

    x_coords.sort()
    y_coords.sort()
    x_min, x_max = x_coords[int(len(x_coords) * 0.01)], x_coords[int(len(x_coords) * 0.99)]
    y_min, y_max = y_coords[int(len(y_coords) * 0.01)], y_coords[int(len(y_coords) * 0.99)]

    grid_w = (x_max - x_min) / 10
    grid_h = ((y_max - y_min) / 10) * HEIGHT_ADJUST

    # 1. 提取所有中心点的原始颜色
    raw_matrix = []
    for r in range(10):
        row = []
        for c in range(10):
            target_x = int(x_min + (c + 0.5) * grid_w)
            target_y = int(y_min + (r + 0.5) * grid_h)
            color = img.getpixel((target_x, target_y))
            row.append(color)
        raw_matrix.append(row)

    # 2. 全局色值映射逻辑 (让不同的色值对应不同的数字)
    final_matrix = []
    known_colors = []  # 用于记录出现过的新颜色

    # 计算两个颜色之间的差距 (三维空间距离)
    def color_distance(c1, c2):
        return math.sqrt(sum((c1[i] - c2[i]) ** 2 for i in range(3)))

    for r in range(10):
        row_ids = []
        for c in range(10):
            pixel_color = raw_matrix[r][c]
            matched_id = -1

            # 遍历我们已经记录的颜色，看看是不是同一种
            for i, k_color in enumerate(known_colors):
                if color_distance(pixel_color, k_color) < COLOR_TOLERANCE:
                    matched_id = i
                    break

            # 如果这是一个全新的颜色，给它分配一个新的数字 ID
            if matched_id == -1:
                known_colors.append(pixel_color)
                matched_id = len(known_colors) - 1

            row_ids.append(matched_id)
        final_matrix.append(row_ids)

    # 打印最终统计信息，正常的星之战应该刚好输出 10
    if len(known_colors) != 10:
        print("注意：颜色种类不等于 10，可能是背景杂色干扰或容差参数需要微调。")

    return final_matrix