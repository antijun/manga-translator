import os
import cv2
import tempfile
from tqdm import tqdm

class TextBounding:
    def __init__(self):
        pass

    def detect_text_regions(self, img_path, contour_size=0.01):
        """Detect text regions and return bounding boxes."""
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Edge detection and thresholding
        edges = cv2.Sobel(gray, cv2.CV_8U, 1, 0)
        _, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Morphological operations
        ele_size = (int(img.shape[0] * contour_size), int(img.shape[0] * contour_size))
        element = cv2.getStructuringElement(cv2.MORPH_RECT, ele_size)
        morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, element)

        # Find contours
        contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        noise_size_param = int(ele_size[0] / 3)
        contours = [cnt for cnt in contours if cnt.shape[0] > noise_size_param ** 2]

        # Bounding boxes
        bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
        return bounding_boxes

    def crop_regions(self, img, bounding_boxes):
        """Crop bounding regions and return them as in-memory images."""
        cropped_images = []
        for (x, y, w, h) in bounding_boxes:
            cropped = img[y:y + h, x:x + w]
            cropped_images.append(cropped)
        return cropped_images

    def process_text_regions(self, img_path):
        """Detect and process text regions without saving cropped regions."""
        img = cv2.imread(img_path)
        bounding_boxes = self.detect_text_regions(img_path)
        cropped_images = self.crop_regions(img, bounding_boxes)
        return cropped_images

    def draw_boxes(self, img_path, output_dir):
        """Draw bounding boxes on the image and save it."""
        img = cv2.imread(img_path)
        bounding_boxes = self.detect_text_regions(img_path)

        for (x, y, w, h) in bounding_boxes:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        boxed_image_path = os.path.join(output_dir, os.path.basename(img_path))
        cv2.imwrite(boxed_image_path, img)
        print(f"Image with bounding boxes saved to {boxed_image_path}")
        return boxed_image_path
