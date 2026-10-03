from ultralytics import YOLO

model = YOLO("C:\\Users\\thiba\\Desktop\\Belote Score\\runs\\obb\\first-gpu-test\\weights\\best.pt")
model.export(format="onnx")