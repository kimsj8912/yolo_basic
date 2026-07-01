from ultralytics import YOLO

model = YOLO('yolo26n.pt')
results = model.train(
    data='dataset/data.yaml',
    epochs=100,
    imgsz=[640,640],
    batch=64,
    workers=4,
)

print(f'Results: {results.results_dict}')