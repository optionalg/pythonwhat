#import dill
#from .output import NoOutput, CaptureExecOutput, OutputManager
from . import utils
import os
import dill
from pythonwhat.State import State

class TaskIsDefined(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell, original_ns_keys):
        return self.name in shell.user_ns

class TaskGetStream(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell, original_ns_keys):
        try:
            return dill.dumps(shell.user_ns[self.name])
        except:
            return None

class TaskGetClass(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, shell, original_ns_keys):
        obj = shell.user_ns[self.name]

        if hasattr(obj, '__module__'):
            typestr = obj.__module__ + "."
        else:
            typestr = ""
        return typestr + obj.__class__.__name__

class TaskConvert(object):
    def __init__(self, name, converter):
        self.name = name
        self.converter = converter

    def __call__(self, shell, original_ns_keys):
        return dill.loads(self.converter)(shell.user_ns[self.name])

class TaskEvalCodeClass(object):
    def __init__(self, code, name):
        self.code = name + " = " + code

    def __call__(self, shell, original_ns_keys):
        try:
            shell.run_cell(self.code)
            return True
        except:
            return None
        # task = TaskGetClass("theobject")
        # return task(shell, original_ns_keys)

def isDefined(name, process):
    return process.executeTask(TaskIsDefined(name))

def getStream(name, process):
    return process.executeTask(TaskGetStream(name))

def getRepresentation(name, process):
    obj_class = process.executeTask(TaskGetClass(name))
    state = State.active_state
    converters = state.get_converters()
    if obj_class in converters:
        stream = process.executeTask(TaskConvert(name, dill.dumps(converters[obj_class])))
        if isinstance(stream, list) and 'backend-error' in str(stream):
            stream = None
    else:
        stream = getStream(name, process)

    return stream

def evalInProcess(code, process):
    res = process.executeTask(TaskEvalCodeClass(code, "_evaluation_object_"))
    if not res:
        return None
    else:
        return getRepresentation("_evaluation_object_", process)




