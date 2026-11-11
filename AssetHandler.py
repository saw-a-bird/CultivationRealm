
import re
import colorsys
from pathlib import Path
import io
import sys

from PIL import Image, ImageTk, ImageFilter, ImageColor
import resvg_py

class StarIconColors:
    GOLD   = "#FFC45E"
    DEEP_GOLD   = "#CE5F34"
    PURPLE = "#B77EF0"
    GREEN  = "#2DCB52"
    MUTED = "#A9A2C7"

class ASSET_TYPES:
    ICONS = "icons"
    FONTS = "fonts"

class AssetHandler:
    def make_star_svg_hollow(
        color=StarIconColors.GOLD,
        fill_color=None,
        glow_strength=0.8,
        glow_radius=4.0,
        reflective=True,
        reflection_strength=0.5,
        outline_thickness=3.5,
        light_direction="top-left"
    ):
        """
        Generate the original hollow metallic sparkle SVG.

        color:
            Glow color.

        fill_color:
            Outline gradient base color.
            Defaults to color.

        glow_strength:
            Original outer glow opacity: 0.8.
            Inner glow automatically maintains the original 0.8 ratio.

        glow_radius:
            Outer blur radius.
            Inner blur maintains the original 1.4 / 4.0 ratio.

        reflective:
            Enable or disable the original white reflection.

        reflection_strength:
            Original reflection opacity: 0.325.
            Scaled relative to the original value.

        light_direction:
            "top-left" or "top-right".
        """

        # --------------------------------------------------
        # Helpers
        # --------------------------------------------------

        def clamp(value, minimum, maximum):
            return max(minimum, min(maximum, float(value)))

        def validate_color(value):
            if not isinstance(value, str) or not re.fullmatch(
                r"#[0-9a-fA-F]{6}", value
            ):
                raise ValueError(
                    f"Invalid color: {value!r}. Use #RRGGBB format."
                )
            return value.upper()

        def rgb(hex_color):
            return tuple(
                int(hex_color[i:i + 2], 16) / 255
                for i in (1, 3, 5)
            )

        def to_hex(values):
            return "#{:02X}{:02X}{:02X}".format(
                *(round(clamp(v, 0, 1) * 255) for v in values)
            )

        def mix(a, b, amount):
            return tuple(
                x + (y - x) * amount
                for x, y in zip(a, b)
            )

        def lighten(hex_color, amount):
            return to_hex(mix(rgb(hex_color), (1, 1, 1), amount))

        def darken(hex_color, amount):
            return to_hex(mix(rgb(hex_color), (0, 0, 0), amount))

        # --------------------------------------------------
        # Parameters
        # --------------------------------------------------

        color = validate_color(color)
        fill_color = validate_color(fill_color or color)

        glow_strength = clamp(glow_strength, 0, 1)
        glow_radius = clamp(glow_radius, 0, 20)
        reflection_strength = clamp(reflection_strength, 0, 1)

        if light_direction not in ("top-left", "top-right"):
            raise ValueError(
                "light_direction must be 'top-left' or 'top-right'"
            )

        # --------------------------------------------------
        # Original outline gradient
        # --------------------------------------------------

        # Preserve the exact original golden palette when
        # using the original default color.
        if fill_color == "#FFC45E":

            outline_stops = """
                <stop offset="0%" stop-color="#FFFBE8"/>
                <stop offset="25%" stop-color="#FFE9AE"/>
                <stop offset="55%" stop-color="#FFC45E"/>
                <stop offset="100%" stop-color="#F5A936"/>
            """

        else:
            # Adapt the original gradient proportions to
            # the selected outline color.
            outline_stops = f"""
                <stop offset="0%"
                    stop-color="{lighten(fill_color, 0.92)}"/>

                <stop offset="25%"
                    stop-color="{lighten(fill_color, 0.72)}"/>

                <stop offset="55%"
                    stop-color="{fill_color}"/>

                <stop offset="100%"
                    stop-color="{darken(fill_color, 0.12)}"/>
            """

        # --------------------------------------------------
        # Light direction
        # --------------------------------------------------

        if light_direction == "top-left":
            gradient_x1 = "0%"
            gradient_x2 = "85%"

            reflection_path = """
                M31 7
                C27 20 21 27 7 35
            """

        else:
            gradient_x1 = "100%"
            gradient_x2 = "15%"

            reflection_path = """
                M33 7
                C37 20 43 27 57 35
            """

        # --------------------------------------------------
        # Original glow proportions
        # --------------------------------------------------

        outer_blur = glow_radius
        inner_blur = glow_radius * (1.4 / 4.0)

        outer_opacity = glow_strength
        inner_opacity = glow_strength * 0.8

        # --------------------------------------------------
        # Original reflection
        # --------------------------------------------------

        if reflective:
            reflection_layer = f"""
            <path
                d="{reflection_path}"
                fill="none"
                stroke="#FFFFFF"
                stroke-width="0.9"
                stroke-linecap="round"
                opacity="{0.325 * (reflection_strength / 0.5):.4f}"
            />
            """
        else:
            reflection_layer = ""

        # --------------------------------------------------
        # SVG
        # --------------------------------------------------

        svg = f"""
        <svg xmlns="http://www.w3.org/2000/svg"
            width="64" height="72"
            viewBox="0 0 64 72">

            <defs>

                <!-- Hollow outline gradient -->

                <linearGradient id="outlineGradient"
                    x1="{gradient_x1}" y1="0%"
                    x2="{gradient_x2}" y2="100%">

                    {outline_stops}

                </linearGradient>

                <!-- Original star clipping -->

                <clipPath id="starClip">
                    <path d="
                        M32 4
                        C36.5 21 42 27 60 36
                        C42 43 36.5 49 32 68
                        C27.5 49 22 43 4 36
                        C22 27 27.5 21 32 4
                        Z"/>
                </clipPath>

                <!-- Original glow filter -->

                <filter id="glow"
                    x="-100%" y="-100%"
                    width="300%" height="300%"
                    color-interpolation-filters="sRGB">

                    <feGaussianBlur
                        in="SourceAlpha"
                        stdDeviation="{outer_blur:.3f}"
                        result="outerBlur"/>

                    <feFlood
                        flood-color="{color}"
                        flood-opacity="{outer_opacity:.4f}"
                        result="outerColor"/>

                    <feComposite
                        in="outerColor"
                        in2="outerBlur"
                        operator="in"
                        result="outerGlow"/>

                    <feGaussianBlur
                        in="SourceAlpha"
                        stdDeviation="{inner_blur:.3f}"
                        result="innerBlur"/>

                    <feFlood
                        flood-color="{color}"
                        flood-opacity="{inner_opacity:.4f}"
                        result="innerColor"/>

                    <feComposite
                        in="innerColor"
                        in2="innerBlur"
                        operator="in"
                        result="innerGlow"/>

                    <feMerge>
                        <feMergeNode in="outerGlow"/>
                        <feMergeNode in="innerGlow"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>

                </filter>

            </defs>

            <!-- Main hollow star -->

            <g filter="url(#glow)">

                <path
                    d="
                        M32 4
                        C36.5 21 42 27 60 36
                        C42 43 36.5 49 32 68
                        C27.5 49 22 43 4 36
                        C22 27 27.5 21 32 4
                        Z"
                    fill="none"
                    stroke="url(#outlineGradient)"
                    stroke-width="{outline_thickness}"
                    stroke-linejoin="round"
                    filter="url(#glow)"
                />

            </g>

            <!-- Original white reflection -->

            {reflection_layer}

        </svg>
        """

        return svg.strip()

    def make_star_svg(
    color=StarIconColors.GOLD,
    fill_color=None,
    glow_strength=0.8,
    glow_radius=4.0,
    reflective=True,
    reflection_strength=0.85,
    light_direction="top-left"
):
        """
        Generate a metallic four-point sparkle SVG.

        color:
            Glow color.

        fill_color:
            Main star color. Defaults to color.

        glow_strength:
            Glow opacity (0.0 - 1.0).

        glow_radius:
            Controls outer and inner glow blur.

        reflective:
            Enable surface illumination.

        reflection_strength:
            Reflection opacity (0.0 - 1.0).

        light_direction:
            "top-left" or "top-right".
        """

        # --------------------------------------------------
        # Helpers
        # --------------------------------------------------

        def clamp(value, low=0.0, high=1.0):
            return max(low, min(high, float(value)))

        def parse_color(hex_color):
            if not re.fullmatch(r"#[0-9a-fA-F]{6}", hex_color):
                raise ValueError(
                    f"Expected a 6-digit hex color, got {hex_color!r}"
                )

            return tuple(
                int(hex_color[i:i + 2], 16) / 255
                for i in (1, 3, 5)
            )

        def to_hex(rgb):
            return "#{:02X}{:02X}{:02X}".format(
                *(round(clamp(c) * 255) for c in rgb)
            )

        def mix(color_a, color_b, amount):
            return tuple(
                a + (b - a) * amount
                for a, b in zip(color_a, color_b)
            )

        def lighten(hex_color, amount):
            rgb = parse_color(hex_color)
            return to_hex(mix(rgb, (1, 1, 1), amount))

        def darken(hex_color, amount):
            rgb = parse_color(hex_color)
            return to_hex(mix(rgb, (0, 0, 0), amount))

        def make_highlight(hex_color, amount):
            """
            Create a soft, slightly desaturated highlight
            while retaining the original hue.
            """
            rgb = parse_color(hex_color)
            h, s, v = colorsys.rgb_to_hsv(*rgb)

            s *= 0.48
            v += (1.0 - v) * amount

            return to_hex(colorsys.hsv_to_rgb(h, s, min(v, 1.0)))

        # --------------------------------------------------
        # Validate and normalize parameters
        # --------------------------------------------------

        glow_strength = clamp(glow_strength)
        reflection_strength = clamp(reflection_strength)
        glow_radius = clamp(glow_radius, 0, 20)

        if light_direction not in ("top-left", "top-right"):
            raise ValueError(
                "light_direction must be 'top-left' or 'top-right'"
            )

        fill_color = fill_color or color

        # --------------------------------------------------
        # Dynamic metallic palette
        # --------------------------------------------------

        base = parse_color(fill_color)

        highlight_1 = lighten(fill_color, 0.90)
        highlight_2 = lighten(fill_color, 0.70)
        highlight_3 = lighten(fill_color, 0.42)

        mid_color = fill_color
        shadow_color = darken(fill_color, 0.12)

        # Soft reflection colors derived from the fill
        reflection_color_1 = make_highlight(fill_color, 0.88)
        reflection_color_2 = make_highlight(fill_color, 0.58)

        # --------------------------------------------------
        # Light direction
        # --------------------------------------------------

        if light_direction == "top-left":
            gx1, gx2 = "15%", "85%"
            specular_x = "25%"
        else:
            gx1, gx2 = "85%", "15%"
            specular_x = "75%"

        # --------------------------------------------------
        # Reflection
        # --------------------------------------------------

        if reflective:
            reflection_gradient = f"""
            <radialGradient id="specularGradient"
                cx="{specular_x}" cy="18%" r="75%">

                <stop offset="0%"
                    stop-color="{reflection_color_1}"
                    stop-opacity="{0.95 * reflection_strength:.3f}"/>

                <stop offset="35%"
                    stop-color="{reflection_color_2}"
                    stop-opacity="{0.45 * reflection_strength:.3f}"/>

                <stop offset="100%"
                    stop-color="{fill_color}"
                    stop-opacity="0"/>

            </radialGradient>
            """

            reflection_layer = """
            <g clip-path="url(#starClip)">
                <rect x="0" y="0"
                    width="64" height="72"
                    fill="url(#specularGradient)"/>
            </g>
            """
        else:
            reflection_gradient = ""
            reflection_layer = ""

        # --------------------------------------------------
        # SVG
        # --------------------------------------------------

        svg = f"""
        <svg xmlns="http://www.w3.org/2000/svg"
            width="64" height="72"
            viewBox="0 0 64 72">

            <defs>

                <!-- Dynamic metallic gradient -->

                <linearGradient id="metalGradient"
                    x1="{gx1}" y1="5%"
                    x2="{gx2}" y2="100%">

                    <stop offset="0%"
                        stop-color="{highlight_1}"/>

                    <stop offset="20%"
                        stop-color="{highlight_2}"/>

                    <stop offset="42%"
                        stop-color="{highlight_3}"/>

                    <stop offset="70%"
                        stop-color="{mid_color}"/>

                    <stop offset="100%"
                        stop-color="{shadow_color}"/>

                </linearGradient>

                {reflection_gradient}

                <!-- Star clipping -->

                <clipPath id="starClip">
                    <path d="
                        M32 4
                        C36.5 21 42 27 60 36
                        C42 43 36.5 49 32 68
                        C27.5 49 22 43 4 36
                        C22 27 27.5 21 32 4
                        Z"/>
                </clipPath>

                <!-- Soft colored glow -->

                <filter id="glow"
                    x="-100%" y="-100%"
                    width="300%" height="300%"
                    color-interpolation-filters="sRGB">

                    <feGaussianBlur in="SourceAlpha"
                        stdDeviation="{glow_radius * 0.875:.2f}"
                        result="outerBlur"/>

                    <feFlood flood-color="{color}"
                        flood-opacity="{glow_strength:.3f}"
                        result="outerColor"/>

                    <feComposite in="outerColor"
                        in2="outerBlur"
                        operator="in"
                        result="outerGlow"/>

                    <feGaussianBlur in="SourceAlpha"
                        stdDeviation="{glow_radius * 0.375:.2f}"
                        result="innerBlur"/>

                    <feFlood flood-color="{color}"
                        flood-opacity="{glow_strength:.3f}"
                        result="innerColor"/>

                    <feComposite in="innerColor"
                        in2="innerBlur"
                        operator="in"
                        result="innerGlow"/>

                    <feMerge>
                        <feMergeNode in="outerGlow"/>
                        <feMergeNode in="innerGlow"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>

                </filter>

            </defs>

            <!-- Main metallic sparkle -->

            <g filter="url(#glow)">
                <path id="star"
                    d="
                        M32 4
                        C36.5 21 42 27 60 36
                        C42 43 36.5 49 32 68
                        C27.5 49 22 43 4 36
                        C22 27 27.5 21 32 4
                        Z"
                    fill="url(#metalGradient)"
                    stroke="none"/>
            </g>

            <!-- Surface illumination -->

            {reflection_layer}

        </svg>
        """

        return svg.strip()

    def chevrons_down_svg():
        return f"""
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                width="16" height="16" fill="none"
                stroke="{StarIconColors.MUTED}" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round">
                <path d="m7 6 5 5 5-5"/>
                <path d="m7 13 5 5 5-5"/>
            </svg>
        """
    
    def _get_assets_path(folder):
        if getattr(sys, "frozen", False):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent

        return base_dir / "assets" / folder

    @staticmethod
    def svg_to_photo(
        icon,
        size=(32, 32),
        glow=False,
        glow_color="#FFC45E",
        glow_radius=4,
        glow_strength=0.65
    ):
        if icon.endswith(".svg"):
            icon_name = icon
            icons_dir = AssetHandler._get_assets_path(ASSET_TYPES.ICONS)
            svg_path = icons_dir / icon_name

            if not svg_path.exists():
                raise FileNotFoundError(f"Icon not found: {svg_path}")

            # Read SVG
            svg_string = svg_path.read_text(encoding="utf-8")
        else:
            svg_string = icon
            
        # Render SVG
        png_data = resvg_py.svg_to_bytes(
            svg_string,
            width=size[0],
            height=size[1]
        )

        image = Image.open(io.BytesIO(png_data)).convert("RGBA")
        if glow:
            alpha = image.getchannel("A")

            # More visible, soft golden halo
            blurred = alpha.filter(
                ImageFilter.GaussianBlur(radius=3)
            )

            blurred = blurred.point(
                lambda p: int(p * 1.5)
            )

            glow_image = Image.new(
                "RGBA",
                image.size,
                ImageColor.getcolor(glow_color, "RGBA")
            )
            glow_image.putalpha(blurred)

            # Preserve the crisp original icon
            glow_image.alpha_composite(image)

            image = glow_image
        return ImageTk.PhotoImage(image)

# Example
if __name__ == "__main__":
    print(AssetHandler.make_star_svg_hollow(
        color=StarIconColors.PURPLE,
        fill_color=None,
        glow_radius=10,
        glow_strength=5,
        reflective=False,
        reflection_strength=0.5,
        light_direction="top-left"
    ))