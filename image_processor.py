import cv2
import numpy as np

class ImageProcessor:
    def __init__(self, image_path, patch_size=(5, 5), num_top_patches=4):
        #Initialize the image processor with the provided image file path,
        #patch size, and number of top patches to find.
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.image_rgb = cv2.imread(image_path)
        self.patch_size = patch_size
        self.num_top_patches = num_top_patches
        self.top_patch_centers = []

    def find_top_patches(self):
        #Find the top patches in the grayscale image based on average brightness
        height, width = self.image.shape
        patch_scores = []

        for y in range(0, height, self.patch_size[0]):
            for x in range(0, width, self.patch_size[1]):
                patch = self.image[y:y+self.patch_size[0], x:x+self.patch_size[1]]
                average_brightness = np.mean(patch)
                patch_scores.append((average_brightness, (x, y)))

        #Sort patches by average brightness in descending order
        patch_scores.sort(reverse=True)

        self.top_patch_centers = [patch[1] for patch in patch_scores[:self.num_top_patches]]

    def draw_squares(self):
        #Draw squares around the top patches on a grayscale image
        image_with_squares = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
        for center in self.top_patch_centers:
            x, y = center
            top_left = (x, y)
            bottom_right = (x + self.patch_size[1], y + self.patch_size[0])
            cv2.rectangle(image_with_squares, top_left, bottom_right, (0, 0, 255), 2)
        return image_with_squares

    def calculate_quadrilateral_area(self):
        #Calculate the area of the quadrilateral formed by patch centers
        if len(self.top_patch_centers) != 4:
            raise ValueError("Image does not have enough non-overlapping patches for a quadrilateral.")

        return 0.5 * abs(
            (self.top_patch_centers[0][0] * self.top_patch_centers[1][1] +
             self.top_patch_centers[1][0] * self.top_patch_centers[2][1] +
             self.top_patch_centers[2][0] * self.top_patch_centers[3][1] +
             self.top_patch_centers[3][0] * self.top_patch_centers[0][1]) -
            (self.top_patch_centers[1][0] * self.top_patch_centers[0][1] +
             self.top_patch_centers[2][0] * self.top_patch_centers[1][1] +
             self.top_patch_centers[3][0] * self.top_patch_centers[2][1] +
             self.top_patch_centers[0][0] * self.top_patch_centers[3][1])
        )

    def process_image(self):
        #Process the image: find top patches, draw squares, and calculate quadrilateral area
        self.find_top_patches()
        image_with_squares = self.draw_squares()

        #Save the image with squares around the top patches
        cv2.imwrite('out_with_patches.png', image_with_squares)

        #Calculate the area of the quadrilateral formed by patch centers
        area = self.calculate_quadrilateral_area()

        #Create copies of the original image for drawing the quadrilateral
        image_with_quadrilateral_grayscale = self.image.copy()
        image_with_quadrilateral_grayscale = cv2.cvtColor(image_with_quadrilateral_grayscale, cv2.COLOR_GRAY2BGR)
        image_with_quadrilateral_rgb = self.image_rgb.copy()

        #Draw the quadrilateral on the grayscale image in red
        cv2.polylines(image_with_quadrilateral_grayscale, [np.int32(self.top_patch_centers)], isClosed=True, color=(0, 0, 255), thickness=2)

        #Draw the quadrilateral on the RGB image in red
        cv2.polylines(image_with_quadrilateral_rgb, [np.int32(self.top_patch_centers)], isClosed=True, color=(0, 0, 255), thickness=2)

        #Save the grayscale image with the quadrilateral
        cv2.imwrite('out_with_quadrilateral_grayscale.png', image_with_quadrilateral_grayscale)

        #Save the RGB image with the quadrilateral
        cv2.imwrite('out_with_quadrilateral_rgb.png', image_with_quadrilateral_rgb)

        #Display the area of the quadrilateral
        print("Area of the quadrilateral:", area)

def main():
    #Create an ImageProcessor instance with the image file '1.jpg' and process the image
    image_processor = ImageProcessor('1.jpg')
    image_processor.process_image()

if __name__ == "__main__":
    main()
