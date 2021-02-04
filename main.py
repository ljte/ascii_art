from typing import Union, Tuple
import argparse
import pathlib

from PIL import Image
import numpy as np
import cv2 as cv


class AsciiArt:

    ASCII = ["@", "%", "#", "*", "+", "=", "-", ":", ".", " "]

    def __init__(self, image: np.ndarray):
        self._width, self._height = self._get_shape(image)
        self._image = image

    @classmethod
    def fromfile(cls, image: Union[str, pathlib.Path]) -> 'AsciiArt':
        return cls(cv.imread(image, cv.IMREAD_COLOR))

    @classmethod
    def from_PIL(cls, image: Image) -> 'AsciiArt':
        return cls(np.asarray(image))

    def _get_shape(self, image: np.ndarray) -> Tuple[int, int]:
        if len(image.shape) == 3:
            return image.shape[1], image.shape[0]
        return image.shape[0], image.shape[1]
        
    def show_image(self) -> None:
        image = Image.fromarray(self._image)
        image.show()
    
    def _convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    def _resize_image(self, image: np.ndarray, new_width: int = 50) -> np.ndarray:
        width, height = self._get_shape(image)
        ratio = height / width
        return cv.resize(image, (new_width, int(ratio * new_width)))

    def _create_ascii_art(self) -> str:
        img = self._convert_to_grayscale(
            self._resize_image(self._image)
        )
        art = ["".join([self.ASCII[pix // 26] for pix in row]) for row in img]
        return "\n".join(art)
    
    def show(self):
        print(self._create_ascii_art())

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="image to process")
    args = parser.parse_args()

    art = AsciiArt.fromfile(args.image)
    art.show()