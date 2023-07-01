import json
import os
from server import app
from flask import current_app

class djmObject:

    objects = {}

    def load(self):
        with open(
            os.path.abspath(
                os.path.join(
                os.environ["DIJAMS_HOME"], "objects.json"))
        ) as f:
            self.objects = json.load(f)

    def dump(self):
        with open(
            os.path.abspath(
                os.path.join(
                os.environ["DIJAMS_HOME"], "objects.json"))
        ) as f:
            json.dump(self.objects, f)
