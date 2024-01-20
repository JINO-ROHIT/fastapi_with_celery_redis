import logging
from torchvision.io import read_image
from torchvision.models import resnet50, ResNet50_Weights
from celery import Task
from celery.exceptions import MaxRetriesExceededError
from .app_worker import app
from loguru import logger

class PredictTask(Task):
    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        if not self.model:
            logging.info('Loading Model...')
            self.weights = ResNet50_Weights.DEFAULT
            self.model = resnet50(weights = self.weights)
            self.model.eval()

            logging.info('Model loaded')
        return self.run(*args, **kwargs)


@app.task(ignore_result=False, bind=True)
def predict_image(self, data):

    try:
        preprocess = self.weights.transforms()
        batch = preprocess(data).unsqueeze(0)

        prediction = self.model(batch).squeeze(0).softmax(0)
        class_id = prediction.argmax().item()
        score = prediction[class_id].item()
        category_name = self.weights.meta["categories"][class_id]
        #print(f"{category_name}: {100 * score:.1f}%")
        return {'status': 'SUCCESS', 'result': f"{category_name}: {100 * score:.1f}%"}
    except Exception as ex:
        print(ex)
        try:
            self.retry(countdown = 2)
        except MaxRetriesExceededError as ex:
            return {'status': 'FAIL', 'result': 'max retries limit exceeded'}