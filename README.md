# Image Resaver

A lightweight PyQt5 app for resaving and optimizing images with drag-and-drop functionality. Supports JPG, JPEG, and PNG formats, optimizing images in batches of up to 50 files with a clean dark-themed interface.

## Features

- Drag and drop images directly into the window.
- Automatically optimizes and resaves images with high quality.
- Supports up to **50 images** per batch.
- Dark-themed interface for a comfortable user experience.
- Checks for the presence of the `Roboto` font and defaults to `Arial` if unavailable.

## Requirements

- Python 3.8 or later
- The following Python libraries:
  - [PyQt5](https://pypi.org/project/PyQt5/)
  - [Pillow](https://pypi.org/project/Pillow/)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/baslie/image-resaver.git
   cd image-resaver
   ```

2. Install the required dependencies manually:

   ```bash
   pip install PyQt5 Pillow
   ```

3. Place an icon file named `app_icon.ico` in the project directory (optional).

## Usage

1. Run the application:

   ```bash
   python image_resaver.py
   ```

2. Drag and drop your images (`JPG`, `JPEG`, or `PNG`) into the application window.

3. The application will automatically optimize and resave your images in their original location.

## Notes

- The application supports up to 50 images in a single operation. Additional images will be ignored without a warning.
- Unsupported file formats are ignored without any messages.

## License

This project is licensed under the MIT License.

## Contribution

Feel free to open issues or submit pull requests to improve the application!

---
Happy coding!
