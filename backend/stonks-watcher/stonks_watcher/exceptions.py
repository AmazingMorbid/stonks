
class TaskFailed(BaseException):
    def __init__(self, msg):
        super(TaskFailed, self).__init__(msg)
