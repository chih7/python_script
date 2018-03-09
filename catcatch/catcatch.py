import os
import os.path

import caffe
import cv2
import numpy as np
import requests
from bs4 import BeautifulSoup
from caffe.proto import caffe_pb2

caffe.set_mode_cpu()

# Size of images
IMAGE_WIDTH = 227
IMAGE_HEIGHT = 227

'''
Image processing helper function
'''


def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):
    # Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    # Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation=cv2.INTER_CUBIC)

    return img


'''
Reading mean image, caffe model and its weights
'''
# Read mean image
mean_blob = caffe_pb2.BlobProto()
with open('../input/mean.binaryproto') as f:
    mean_blob.ParseFromString(f.read())
mean_array = np.asarray(mean_blob.data, dtype=np.float32).reshape(
    (mean_blob.channels, mean_blob.height, mean_blob.width))

# Read model architecture and trained model's weights
net = caffe.Net('../caffe_models/caffe_model_2/caffenet_deploy_2.prototxt',
                '../caffe_models/caffe_model_2/caffe_model_2_iter_500.caffemodel',
                caffe.TEST)

# Define image transformers
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_mean('data', mean_array)
transformer.set_transpose('data', (2, 0, 1))


def isCat(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)

    net.blobs['data'].data[...] = transformer.preprocess('data', img)
    out = net.forward()
    pred_probas = out['prob']

    return pred_probas.argmax()


class Zhihu():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)',
                        'Host': 'www.zhihu.com'}
        self.session = requests.session()
        self.title = ''

    def getImage(self, pageUrl):
        response = self.session.get(pageUrl, headers=self.headers)
        html = BeautifulSoup(response.text, 'lxml')
        self.title = html.find('span', class_='zm-editable-content').string
        answers = html.find_all('div', class_='zm-item-answer')
        for answer in answers:
            if answer.find('img', class_='origin_image zh-lightbox-thumb lazy'):
                self.parse(answer, self.title)
            else:
                pass

    def parse(self, item, title):
        author = item.find('a', class_='author-link').string
        images = item.find_all('img', class_='origin_image zh-lightbox-thumb lazy')
        image_list = [n.get('data-actualsrc') for n in images]
        self.Download(image_list, author, title)

    def Download(self, list, author, title):
        num = 0
        for i in list:
            num = num + 1
            temp = i.split('/')
            content = self.session.get(i)
            if not os.path.exists("img"):
                os.mkdir("img")
            with open("img/" + str(temp[3]), 'wb+') as file:
                file.write(content.content)

            if isCat("img/" + str(temp[3])) == 0:
                if not os.path.exists("cat"):
                    os.mkdir("cat")
            with open("cat/" + str(temp[3]), 'wb+') as file:
                file.write(content.content)


if __name__ == "__main__":
    answer = input('输入问题编号：')
    url = 'https://www.zhihu.com/question/' + str(answer)
    image = Zhihu()
    image.getImage(url)
