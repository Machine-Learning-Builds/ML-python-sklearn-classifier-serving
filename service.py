#!/usr/bin/python

import falcon
from sklearn.datasets import load_iris
import json
from joblib import load
import time
from sklearn.preprocessing import StandardScaler


PORT_NUMBER = 8080
start = time.time()

# load the model and scaler
clf = load("model.joblib")
scaler = StandardScaler()

# get test data
X, y, labels = load_iris().data, load_iris().target, load_iris().target_names
X_count = X.shape[0]

# scale data
X_scaled = scaler.fit_transform(X)

end = time.time()
print("Loading time: {0:f} secs)".format(end - start))


# API Handler for Iris images
class Iris(object):

    def on_get(self, req, resp, index):
        if index < X_count:
            y_pred = clf.predict(X_scaled[index].reshape(1, -1))
            payload = {'index': index, 'predicted_label': list(labels)[y_pred[0]], 'predicted': y_pred[0]}
            resp.body = json.dumps(payload)
            resp.status = falcon.HTTP_200
        else:
            raise falcon.HTTPBadRequest(
                "Index Out of Range. ",
                "The requested index must be between 0 and {:d}, inclusive.".format(X_count - 1)
            )

# API Handler for API example message
class Intro(object):

    def on_get(self, req, resp):
        resp.body = '{"message": \
                    "This service verifies a model using the Iris Test data set. Invoke using the form /Iris/<index of ' \
                    'test sample>. For example, /iris/24"}'
        resp.status = falcon.HTTP_200
