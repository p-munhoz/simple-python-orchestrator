import zmq
import pickle
from typing import Callable, Any

class Worker:
    def __init__(self):
        """
        Initialize the worker.

        This method initializes the worker and binds it to listen for requests
        on TCP port 5555.
        """
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")

    def execute_task(self, task: Callable, arg: Any) -> Any:
        """
        Execute a task with the given argument.

        This method executes the task with the given argument and returns the
        result of the task. If an exception occurs during the execution of the
        task, an error message is returned.

        Parameters
        ----------
        task : Callable
            The task to execute.
        arg : Any
            The argument to the task.

        Returns
        -------
        Any
            The result of the task or an error message if an exception occurred.
        """
        try:
            result = task(arg)
            return result
        except Exception as e:
            return f"Error executing task: {str(e)}"

    def run(self):
        """
        Start the worker and listen for tasks.

        This method will block until it receives a message. It will then
        execute the task with the given argument and return the result of the
        task. If an exception occurs during the execution of the task, an error
        message is returned.

        """
        print("Worker started, waiting for tasks...")
        
        while True:
            message = self.socket.recv()
            
            task, arg = pickle.loads(message)
            
            print(f"Executing task: {task.__name__}")
            result = self.execute_task(task, arg)
            
            self.socket.send(pickle.dumps(result))

if __name__ == "__main__":
    worker = Worker()
    worker.run()