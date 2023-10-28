import unittest
import cv2
import numpy as np
from image_processor import ImageProcessor

#Important Note: In order for this code to work correctly, image_processor.py must first be run and the output png files must be obtained.

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        #Create an instance of the ImageProcessor for testing with a sample image
        self.image_processor = ImageProcessor('1.jpg')

    def test_find_top_patches(self):
        #Test if top patches are correctly identified
        self.image_processor.find_top_patches()
        top_patch_centers = self.image_processor.top_patch_centers

        #Assert that the number of top patches is equal to the expected value
        self.assertEqual(len(top_patch_centers), self.image_processor.num_top_patches)

        #Assert that the patch centers are within the image dimensions
        height, width = self.image_processor.image.shape
        for center in top_patch_centers:
            x, y = center
            self.assertLessEqual(x, width)
            self.assertLessEqual(y, height)

    def test_draw_squares(self):
        #Test if squares are correctly drawn around top patches
        self.image_processor.find_top_patches()
        image_with_squares = self.image_processor.draw_squares()

        #Check if the output image has the same dimensions as the input image
        self.assertEqual(image_with_squares.shape, self.image_processor.image_rgb.shape)

        #Check if squares are drawn around all top patches with the expected color
        square_color = (0, 0, 255)  #red 
        square_thickness = 2
        for center in self.image_processor.top_patch_centers:
            x, y = center
            #Verify that the pixel colors at the four corners of the square match the expected color
            self.assertEqual(tuple(image_with_squares[y, x]), square_color)
            self.assertEqual(tuple(image_with_squares[y + square_thickness - 1, x]), square_color)
            self.assertEqual(tuple(image_with_squares[y, x + square_thickness - 1]), square_color)
            self.assertEqual(tuple(image_with_squares[y + square_thickness - 1, x + square_thickness - 1]), square_color)

    def test_draw_quadrilateral(self):
        #Test if the quadrilateral is correctly drawn on grayscale and RGB images
        self.image_processor.find_top_patches()
        self.image_processor.process_image()

        #Load the images with the drawn quadrilateral
        grayscale_image_with_quadrilateral = cv2.imread('out_with_quadrilateral_grayscale.png')
        rgb_image_with_quadrilateral = cv2.imread('out_with_quadrilateral_rgb.png')

        #Check if the loaded images are not None
        self.assertTrue(grayscale_image_with_quadrilateral is not None)
        self.assertTrue(rgb_image_with_quadrilateral is not None)

        #Check if the quadrilateral is drawn in red color
        quadrilateral_color = (0, 0, 255)  # red
        quadrilateral_thickness = 2
        
        #Calculate the coordinates of the quadrilateral vertices
        x0, y0 = self.image_processor.top_patch_centers[0]
        x1, y1 = self.image_processor.top_patch_centers[1]
        x2, y2 = self.image_processor.top_patch_centers[2]
        x3, y3 = self.image_processor.top_patch_centers[3]
        
        #Verify that the pixel colors at the four corners of the quadrilateral match the expected color
        self.assertEqual(tuple(grayscale_image_with_quadrilateral[y0, x0]), quadrilateral_color)
        self.assertEqual(tuple(grayscale_image_with_quadrilateral[y1, x1]), quadrilateral_color)
        self.assertEqual(tuple(grayscale_image_with_quadrilateral[y2, x2]), quadrilateral_color)
        self.assertEqual(tuple(grayscale_image_with_quadrilateral[y3, x3]), quadrilateral_color)

        #Repeat the same checks for the RGB image
        self.assertEqual(tuple(rgb_image_with_quadrilateral[y0, x0]), quadrilateral_color)
        self.assertEqual(tuple(rgb_image_with_quadrilateral[y1, x1]), quadrilateral_color)
        self.assertEqual(tuple(rgb_image_with_quadrilateral[y2, x2]), quadrilateral_color)
        self.assertEqual(tuple(rgb_image_with_quadrilateral[y3, x3]), quadrilateral_color)



    def test_process_image(self):
        #Test the complete image processing workflow
        self.image_processor.process_image()

if __name__ == '__main__':
    unittest.main()
