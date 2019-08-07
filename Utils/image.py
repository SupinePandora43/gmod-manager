from PIL import Image
import numpy as np
import os


class AsciiImage:
    chars = ""

    def __init__(self, Img: Image.Image):
        SC = 0.36
        try:
            SC = 496 / os.get_terminal_size().columns
        finally:
            pass
        AsciiChars = np.asarray(list(" .,:;irsXA253hMHGS#9B&@"))
        S = (round(Img.size[0] * SC * 2.5), round(Img.size[1] * SC))
        Img = np.sum(np.asarray(Img.resize(S)), axis=2)
        Img -= Img.min()
        Img = (1.0 - Img / Img.max()) ** 1.75 * (AsciiChars.size - 1)
        self.chars = "\n".join(("".join(r) for r in AsciiChars[Img.astype(int)]))
