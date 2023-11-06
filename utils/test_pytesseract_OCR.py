import unittest
from PIL import Image
import pytesseract
from pytesseract_OCR import ocr_image


# A test case for the ocr_image function
class TestOCR(unittest.TestCase):
    def test_ocr_image(self):
        # You need to replace 'test_image.jpg' with a valid test image path in your test directory
        test_image_path = 'example_receipt.jpg'
        
        # Call the function with the test image
        result = ocr_image(test_image_path)
        
        # Check if the result is a string
        self.assertIsInstance(result, str, "The OCR result should be a string.")
        
        # Check if the result is not empty
        self.assertTrue(result.strip(), "The OCR result should not be an empty string.")

# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main()
