import os


class AbstractGestureController:
    def __init__(self):
        pass

    def process_gestures(self):
        NotImplementedError("process_gestures")
