import pytesseract
import os 
import cv2
import argparse
#import tempfile
import numpy as np 
from PIL import Image
#from copy import deepcopy
from paddleocr import PPStructure,save_structure_res
from pdf2image import convert_from_path

class Demo:
    def __init__(self,
                 pdf,
                 save,
                 show_log,
                 image_orientation,
                 layout_score_threshold,
                 layout_nms_threshold,
                 image_crop,
                 image_content):

        self.pdf = pdf
        self.save = save 
        self.sl = show_log 
        self.io = image_orientation 
        self.ths = layout_score_threshold 
        self.nms = layout_nms_threshold 
        self.icr = image_crop
        self.ict = image_content
    
    def convert(self):
        if self.save == None:
            pages = convert_from_path(self.pdf)

            for i in range(len(pages)):
                array=np.array(pages[i], dtype=np.uint8)
                new_image = Image.fromarray(array)
                new_image.save('page'+ str(i) +'.jpg')
                
        else:
            os.makedirs(self.save,exist_ok=True)
            pages = convert_from_path(self.pdf)

            for i in range(len(pages)):
                array=np.array(pages[i], dtype=np.uint8)
                new_image = Image.fromarray(array)
                new_image.save(f'{self.save}/page'+ str(i) +'.jpg', 'JPEG')
        

    def OCR_Crop(self):
        gray = cv2.cvtColor(self.icr, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray,lang='vie')
        print(f"text croper:{text}")
    
    def OCR_content(self):
        # layout detector 
        table_engine = PPStructure(self.sl,self.io,self.ths,self.io)

        save_folder = './output'
        img_path = self.ict
        img = cv2.imread(img_path)
        result = table_engine(img)

        save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])
        res_cp = deepcopy(result)

        for region in res_cp:
            cv2.rectangle(img, region['bbox'], (0, 0, 255), 3)
            x1, y1, x2, y2 = region['bbox']
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            roi_img = img[y1:y2, x1:x2, :]
            #cv2.imwrite('dd.jpg', img)
        #OCR layout 
        gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray,lang='vie')
        print(f"text croper:{text}")



if __name__=="__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",'--filecv', default='Chithi.pdf', type=str,
                        help='name of pdf file')
    parser.add_argument("-s",'--savecv', default='data', type=str,
                        help='name of pdf file')
    parser.add_argument("-l",'--show_log', default='None', type=str,
                        help='name of pdf file')
    parser.add_argument("-l",'--image_orientation', default='None', type=str,
                        help='image_orientation')
    parser.add_argument("-sc",'--layout_score_threshold', default='0.9', type=float, 
                        help='layout_score_threshold')
    parser.add_argument("-nms",'--layout_nms_threshold', default='0.9', type=float, 
                        help="layout_nms_threshold")
    parser.add_argument("-icr",'--image_crop', default='cropped.jpg', type=str, 
                        help='image_crop')
    parser.add_argument("-ict",'--image_content', default='dd.jpg', type=str, 
                        help="image_content")
    
    args = parser.parse_args()
    print(args)
    
    AC=Demo(args.filecv,
            args.savecv,
            args.show_log,
            args.image_orientation,
            args.layout_score_threshold,
            args.layout_nms_threshold,
            args.image_crop,
            args.image_content)
    
    test=AC.convert()
    ocr_crop=AC.OCR_Crop()
    ocr_content=AC.OCR_content()

    