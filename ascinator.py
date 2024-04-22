import subprocess

import cv2
import os


class Ascinator:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    @staticmethod
    def convert_row_to_ascii(row):
        # 17-long
        ORDER = (' ', '.', "'", ',', ':', ';', 'c', 'l',
                 'x', 'o', 'k', 'X', 'd', 'O', '0', 'K', 'N')
        return tuple(ORDER[int(x / (255 / 16))] for x in row)[::-1]

    def convert_to_ascii(self, input_grays):
        return tuple(self.convert_row_to_ascii(row) for row in input_grays)

    @staticmethod
    def print_array(input_ascii_array):
        os.system("clear")
        print('\n'.join((''.join(row) for row in input_ascii_array)), end='')

    @staticmethod
    def rescale_frame(frame, percent=75):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    def main(self):
        while self.cap.isOpened():
            sub = ['stty', 'size']
            out = subprocess.run(sub, shell=False, capture_output=True)
            out = out.stdout.decode('utf-8').split()
            ret, image = self.cap.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            reduced = cv2.resize(gray, (int(out[1]), int(out[0])))

            converted = self.convert_to_ascii(reduced)
            self.print_array(converted)

            cv2.imshow('frame', self.rescale_frame(cv2.flip(image, 1), percent=50))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    Ascinator().main()
