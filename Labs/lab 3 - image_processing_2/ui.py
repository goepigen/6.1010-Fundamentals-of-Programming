import lab
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QLabel,
    QSlider,
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from pathlib import Path

image_folder = Path("./test_images")

# Next tasks
# The original image is the only image with a label.
# The images (that are larger then 100 width) are displayed in a fixed size of 300x300 pixels.
# We would like all images to expand to fill in their containers.
# Thus, the tasks are
# 1) Make the original image expand.
# 2) Add labels and add expanding behavior to the other photos.
# We also want labels for the sliders in the UI showing what they represent and the current values.
# The top dropdown has the width of the entire UI. It should be smaller.


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.image_folder = Path(image_folder)
        self.selected_image_path = None
        self.color_image = None
        self.original_image_pixmap = None
        self.greyscale_image = None
        self.greyscale_image_pixmap = None
        self.blurred_image_pixmap = None
        self.sharpened_image_pixmap = None
        self.energy = None
        self.cumulative_energy_map = None
        self.cumulative_energy_pixmap = None
        self.cumulative_energy_map_normalized = None
        self.color_image_with_highlighted_seam = None
        self.color_image_with_highlighted_seam_pixmap = None
        self.color_image_without_n_seams = None
        self.color_image_without_n_seams_pixmap = None

        self.resize(1600, 1200)
        self.setWindowTitle("w2 - Image Processing")

        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        # Layout
        self.mainVLayout = QVBoxLayout()
        self.row1Layout = QHBoxLayout()
        self.row2Layout = QHBoxLayout()
        self.row3Layout = QHBoxLayout()

        # Dropdown
        self.dropdown = QComboBox()
        self.dropdown.addItems(self.get_image_filenames())
        self.dropdown.currentIndexChanged.connect(self.load_selected_color_image)

        # Original Color Image
        self.original_image_pixmap = QLabel("Original Image")
        self.original_image_pixmap.setAlignment(Qt.AlignmentFlag.AlignCenter)

        original_image_label = QLabel("Original Image")
        original_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        original_image_panel = QVBoxLayout()
        original_image_panel.addWidget(self.original_image_pixmap, stretch=1)
        original_image_panel.addWidget(original_image_label, stretch=0)

        # Greyscale Image
        self.greyscale_image_pixmap = QLabel()
        self.greyscale_image_pixmap.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add Widgets to Row 1
        self.row1Layout.addLayout(original_image_panel)
        self.row1Layout.addWidget(self.greyscale_image_pixmap)

        # Slider to Select Kernel Size for Blur Filter
        self.blur_slider = QSlider(Qt.Orientation.Horizontal)
        self.blur_slider.setMinimum(3)
        self.blur_slider.setMaximum(10)
        self.blur_slider.setValue(3)
        self.blur_slider.valueChanged.connect(self.display_blurred_image)

        # Blurred Image
        self.blurred_image_pixmap = QLabel()
        self.blurred_image_pixmap.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # First Panel in Second Row is Slider + Blurred Image
        self.blur_panel = QVBoxLayout()
        self.blur_panel.addWidget(self.blur_slider)
        self.blur_panel.addWidget(self.blurred_image_pixmap)
        self.row2Layout.addLayout(self.blur_panel)

        # Slider to Select Kernel Size for Sharpen Filter
        self.sharpen_slider = QSlider(Qt.Orientation.Horizontal)
        self.sharpen_slider.setMinimum(3)
        self.sharpen_slider.setMaximum(10)
        self.sharpen_slider.setValue(3)
        self.sharpen_slider.valueChanged.connect(self.display_sharpened_image)

        # Sharpened Image
        self.sharpened_image_pixmap = QLabel()
        self.sharpened_image_pixmap.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Second Panel in Second Row is Slider + Sharpened Image
        self.sharpen_panel = QVBoxLayout()
        self.sharpen_panel.addWidget(self.sharpen_slider)
        self.sharpen_panel.addWidget(self.sharpened_image_pixmap)
        self.row2Layout.addLayout(self.sharpen_panel)

        # Seamcarving Images
        self.energy_image = QLabel()
        self.energy_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cumulative_energy_pixmap = QLabel()
        self.cumulative_energy_pixmap.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.color_image_with_highlighted_seam_pixmap = QLabel()
        self.color_image_with_highlighted_seam_pixmap.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.color_image_without_n_seams_pixmap = QLabel()
        self.color_image_without_n_seams_pixmap.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.row3Layout.addWidget(self.energy_image)
        self.row3Layout.addWidget(self.cumulative_energy_pixmap)
        self.row3Layout.addWidget(self.color_image_with_highlighted_seam_pixmap)

        # Slider to Select n Seams to Remove
        self.n_seams_slider = QSlider(Qt.Orientation.Horizontal)
        self.n_seams_slider.setMinimum(3)
        self.n_seams_slider.setMaximum(30)
        self.n_seams_slider.setValue(3)
        self.n_seams_slider.valueChanged.connect(self.display_n_seams_removed)

        # Fourth Panel in Third Row is Slider + Image Without n Seams
        self.n_seams_removed_panel = QVBoxLayout()
        self.n_seams_removed_panel.addWidget(self.n_seams_slider)
        self.n_seams_removed_panel.addWidget(self.color_image_without_n_seams_pixmap)
        self.row3Layout.addLayout(self.n_seams_removed_panel)

        self.mainVLayout.addWidget(self.dropdown)
        self.mainVLayout.addLayout(self.row1Layout)
        self.mainVLayout.addLayout(self.row2Layout)
        self.mainVLayout.addLayout(self.row3Layout)

        self.setLayout(self.mainVLayout)

        # Load first image in the dropdown list.
        if self.dropdown.count() > 0:
            self.load_selected_color_image(0)

    def get_image_filenames(self):
        return [
            f.name
            for f in self.image_folder.iterdir()
            if f.is_file() and f.suffix.lower() in [".jpg", ".png"]
        ]

    def create_zoomed_pixmap(self, pixmap, zoom_factor):
        if pixmap.width() < 20:
            return pixmap.scaled(
                pixmap.width() * zoom_factor,
                pixmap.height() * zoom_factor,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.FastTransformation,  # This disables smoothing
            )

        return pixmap.scaled(
            300,
            300,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def create_pixmap_from_greyscale_image(self, greyscale_image):
        width = greyscale_image["width"]
        height = greyscale_image["height"]
        pixels = greyscale_image["pixels"]

        byte_data = bytes(pixels)
        bytes_per_line = width
        q_image = QImage(
            byte_data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8
        )

        pixmap = QPixmap.fromImage(q_image)

        return self.create_zoomed_pixmap(pixmap, zoom_factor=30)

    def create_pixmap_from_color_image(self, color_image):
        width = color_image["width"]
        height = color_image["height"]
        pixels = color_image["pixels"]
        flat_bytes = bytes([channel for pixel in pixels for channel in pixel])

        bytes_per_line = width * 3
        q_image = QImage(
            flat_bytes, width, height, bytes_per_line, QImage.Format.Format_RGB888
        )

        pixmap = QPixmap.fromImage(q_image)

        return self.create_zoomed_pixmap(pixmap, zoom_factor=30)

    def load_selected_color_image(self, index):
        if index < 0:
            return

        filename = self.dropdown.itemText(index)
        image_path = image_folder / filename

        if image_path.exists():
            self.selected_image_path = image_path
            self.color_image = lab.load_color_image(str(image_path))

            scaled_pixmap = self.create_pixmap_from_color_image(self.color_image)

            self.original_image_pixmap.setPixmap(scaled_pixmap)

            self.display_greyscale_image()
            self.display_blurred_image()
            self.display_sharpened_image()
            self.display_seam_carving_images()
        else:
            print(f"Image not found.\nError: {image_path}")

    def display_greyscale_image(self):
        greyscale_image = lab.greyscale_image_from_color_image(self.color_image)
        self.greyscale_image = greyscale_image
        scaled_pixmap = self.create_pixmap_from_greyscale_image(greyscale_image)
        self.greyscale_image_pixmap.setPixmap(scaled_pixmap)

    def display_blurred_image(self):
        kernel_size = self.blur_slider.value()
        blur_filter = lab.color_filter_from_greyscale_filter(
            lab.make_blur_filter(kernel_size)
        )
        blurred_image = blur_filter(self.color_image)
        scaled_pixmap = self.create_pixmap_from_color_image(blurred_image)
        self.blurred_image_pixmap.setPixmap(scaled_pixmap)

    def display_sharpened_image(self):
        kernel_size = self.sharpen_slider.value()
        sharpen_filter = lab.color_filter_from_greyscale_filter(
            lab.make_sharpen_filter(kernel_size)
        )
        sharpened_image = sharpen_filter(self.color_image)
        scaled_pixmap = self.create_pixmap_from_color_image(sharpened_image)
        self.sharpened_image_pixmap.setPixmap(scaled_pixmap)

    def display_energy_image(self):
        self.energy = lab.compute_energy(self.greyscale_image)
        scaled_pixmap = self.create_pixmap_from_greyscale_image(self.energy)
        self.energy_image.setPixmap(scaled_pixmap)

    def normalize_cumulative_energy_map(self, cem):
        cem_values = cem["pixels"]

        min_val = min(cem_values)
        max_val = max(cem_values)

        if max_val == min_val:
            normalized_pixels = [0 for _ in len(cem_values)]
        else:
            normalized_pixels = [
                int(255 * (ce - min_val) / (max_val - min_val)) for ce in cem_values
            ]

        return {
            "width": cem["width"],
            "height": cem["height"],
            "pixels": normalized_pixels,
        }

    def display_cumulative_energy_map(self):
        self.cumulative_energy_map = lab.cumulative_energy_map(self.energy)
        self.cumulative_energy_map_normalized = self.normalize_cumulative_energy_map(
            self.cumulative_energy_map
        )
        scaled_pixmap = self.create_pixmap_from_greyscale_image(
            self.cumulative_energy_map_normalized
        )
        self.cumulative_energy_pixmap.setPixmap(scaled_pixmap)

    def display_original_image_with_highlighted_seam(self):
        self.seam = lab.minimum_energy_seam(self.cumulative_energy_map)
        original_pixels = self.color_image["pixels"]
        red_rgb = (255, 0, 0)
        self.color_image_with_highlighted_seam = {
            **self.color_image,
            "pixels": [
                (pixel if i not in self.seam else red_rgb)
                for i, pixel in enumerate(original_pixels)
            ],
        }
        scaled_pixmap = self.create_pixmap_from_color_image(
            self.color_image_with_highlighted_seam
        )

        self.color_image_with_highlighted_seam_pixmap.setPixmap(scaled_pixmap)

    def display_seam_carving_images(self):
        self.display_energy_image()
        self.display_cumulative_energy_map()
        self.display_original_image_with_highlighted_seam()
        self.display_n_seams_removed()

    def display_n_seams_removed(self):
        n_seams = self.n_seams_slider.value()
        self.color_image_without_n_seams = lab.seam_carving(self.color_image, n_seams)
        scaled_pixmap = self.create_pixmap_from_color_image(
            self.color_image_without_n_seams
        )
        self.color_image_without_n_seams_pixmap.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
