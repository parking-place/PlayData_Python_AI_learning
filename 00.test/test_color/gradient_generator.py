def get_gradient_generator(start_color, end_color, n):
    import colorsys
    def hex_to_rgb(hex_code):
        return int(hex_code[1:3], 16), int(hex_code[3:5], 16), int(hex_code[5:7], 16)

    def rgb_to_hex(rgb):
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    start_r, start_g, start_b = hex_to_rgb(start_color)
    end_r, end_g, end_b = hex_to_rgb(end_color)

    start_h, start_s, start_v = colorsys.rgb_to_hsv(start_r, start_g, start_b)
    end_h, end_s, end_v = colorsys.rgb_to_hsv(end_r, end_g, end_b)

    # HUE 값 간 거리 계산 후 가까운 방향으로 변경
    hue_difference = end_h - start_h
    if abs(hue_difference) > 0.5:
        if hue_difference > 0:
            end_h -= 1
        else:
            end_h += 1

    def color_generator():
        for i in range(n):
            h = (start_h + (end_h - start_h) * (i / (n - 1))) % 1
            s = start_s + (end_s - start_s) * (i / (n - 1))
            v = start_v + (end_v - start_v) * (i / (n - 1))
            rgb = colorsys.hsv_to_rgb(h, s, v)
            rgb = tuple([int(x) for x in rgb])
            yield rgb

    return color_generator()
