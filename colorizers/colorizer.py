from colorizers import *
import matplotlib.pyplot as plt
from os import listdir
import io

class Colorizer:
    def __init__(self, greyscale_image):
        self.greyscale_image = greyscale_image

    def colorize(self):
        # load colorizers
        colorizer_eccv16 = eccv16(pretrained=True).eval()
        colorizer_siggraph17 = siggraph17(pretrained=True).eval()
        # if (opt.use_gpu):
        #     colorizer_eccv16.cuda()
        #     colorizer_siggraph17.cuda()

        # default size to process images is 256x256
        # grab L channel in both original ("orig") and resized ("rs") resolutions
        img = load_img(self.greyscale_image)
        (tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256, 256))
        # if (opt.use_gpu):
        #     tens_l_rs = tens_l_rs.cuda()

        # colorizer outputs 256x256 ab map
        # resize and concatenate to original L channel
        img_bw = postprocess_tens(tens_l_orig, torch.cat((0 * tens_l_orig, 0 * tens_l_orig), dim=1))
        out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
        out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())

        # Convert the processed tensor to a PIL image and generate base64 String
        color_image = self.generateBase64String(out_img_eccv16)

        # plt.imsave('%s_eccv16.png' % "new_eccv", out_img_eccv16)
        # plt.imsave('%s_siggraph17.png' % "new_siggraph", out_img_siggraph17)
#Below is the sample to check which image holds good
        # plt.figure(figsize=(12, 8))
        # plt.subplot(2, 2, 1)
        # plt.imshow(img)
        # plt.title('Original')
        # plt.axis('off')

        # plt.subplot(2, 2, 2)
        # plt.imshow(img_bw)
        # plt.title('Input')
        # plt.axis('off')

        # plt.subplot(2, 2, 3)
        # plt.imshow(out_img_eccv16)
        # plt.title('Output (ECCV 16)')
        # plt.axis('off')

        # plt.subplot(2, 2, 4)
        # plt.imshow(out_img_siggraph17)
        # plt.title('Output (SIGGRAPH 17)')
        # plt.axis('off')
        # plt.show()

        return color_image

    def train_model(self):
        progress = 0

        for file in listdir('image_store/train'):
            img_path = 'image_store/train' + file
            img = load_img(img_path)

    def generateBase64String(self, img_rgb):
        # Convert to PIL Image
        img_pil = Image.fromarray((img_rgb * 255).astype(np.uint8))

        # Save image to a bytes buffer in JPEG format
        buffer = io.BytesIO()
        img_pil.save(buffer, format="JPEG")  # Save as JPEG
        img_str = base64.b64encode(buffer.getvalue()).decode()

        # Add prefix to JPEG base64 string
        img_str = "data:image/jpeg;base64," + img_str

        return img_str

