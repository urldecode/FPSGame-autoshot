import numpy as np
import torch
from torch._C import device
from models.experimental import attempt_load
from utils.datasets  import letterbox
from utils.general import check_img_size, non_max_suppression, scale_coords, xyxy2xywh
import warnings

warnings.filterwarnings('ignore')

device = torch.device('cuda')
half = device.type != 'cpu'

model = attempt_load('best.pt', map_location=device)
stride = int(model.stride.max())
img_size = check_img_size(640,s=stride)
if half:
    model.half()
model.eval()

names = model.module.names if  hasattr(model, 'module') else model.names

if device.type != 'cpu':
    model(torch.zeros(1,3,img_size,img_size).to(device).type_as(next(model.parameters())))

def detect(img0):
    with torch.no_grad():
        img = letterbox(img0,img_size,stride=stride)[0]

        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        pred = model(img,augment=False)[0]
        pred = non_max_suppression(pred, 0.25, 0.45)

        detections = []
        for i , det in enumerate(pred):
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4))).view(-1).tolist()
                    xywh = [round(x) for x in xywh]
                    xywh = [xywh[0] - xywh[2] // 2, xywh[1] - xywh[3] // 2, xywh[2], xywh[3]]
                    cls = names[int(cls)]
                    conf = float(conf)
                    detections.append({'class': cls, 'conf': conf, 'position': xywh})
        return detections

