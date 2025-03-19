import pickle
import time
from datetime import datetime
from typing import Callable, List

import zmq


class Workflow:
    def __init__(
        self,
        tasks: List[Callable],
        start_time: datetime,
        name: str,
        conf: any
    ):
        """
        Initialize the workflow.

        Args:
            tasks (List[Callable]): A list of callables, each representing a task.
            start_time (datetime): The time when the workflow should start.
            name (str): The name of the workflow.
            conf (any): Initial data for the workflow.
        """
        self.tasks = tasks
        self.start_time = start_time
        self.name = name
        self.conf = conf
        self.current_task_index = 0
        self.last_result = None

class Scheduler:
    def __init__(self, workflows: List[Workflow]):
        """
        Initialize the scheduler.

        Args:
            workflows (List[Workflow]): A list of workflows to schedule.

        The scheduler will connect to the worker at localhost:5555 to send tasks.
        """
        self.workflows = workflows
        
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")

    def should_execute(self, workflow: Workflow) -> bool:
        """
        Check if a workflow should be executed.

        Args:
            workflow (Workflow): The workflow to check.

        Returns:
            bool: True if the workflow should be executed, False otherwise.
        """
        
        return datetime.now() >= workflow.start_time

    def send_task(self, func: Callable, arg: any) -> any:
        """
        Send a task to the worker.

        Args:
            func (Callable): The function to execute.
            arg (any): The argument to the function.

        Returns:
            any: The result of the task.
        """
        message = pickle.dumps((func, arg))
        self.socket.send(message)
        
        result = pickle.loads(self.socket.recv())
        return result

    def process_workflow(self, workflow: Workflow):
        """
        Process a workflow.

        Args:
            workflow (Workflow): The workflow to process.

        Returns:
            any: The final result of the workflow.
        """
        print(f"Processing workflow: {workflow.name}")
        
        while workflow.current_task_index < len(workflow.tasks):
            current_task = workflow.tasks[workflow.current_task_index]
            
            if workflow.current_task_index == 0:
                input_data = workflow.conf
            else:
                input_data = workflow.last_result

            result = self.send_task(current_task, input_data)
            workflow.last_result = result
            workflow.current_task_index += 1

        print(f"Workflow {workflow.name} completed. Final result:", workflow.last_result)
        return workflow.last_result

    def run(self):
        """
        Run the scheduler to process workflows.

        This method continuously checks and processes the workflows
        that are ready for execution. It filters out workflows that
        are not yet ready and re-checks them after a delay until all
        workflows are completed.
        """
        print("Scheduler started...")
        
        while self.workflows:
            remaining_workflows = []
            
            for workflow in self.workflows:
                if self.should_execute(workflow):
                    self.process_workflow(workflow)
                else:
                    remaining_workflows.append(workflow)
            
            self.workflows = remaining_workflows
            
            if self.workflows:
                time.sleep(1)

        print("All workflows completed")

if __name__ == "__main__":
    from datetime import datetime, timedelta

    from source import compute_average_salary, filter_departments, read_csv_file

    workflow_employee_analysis = Workflow(
        tasks=[
            read_csv_file,          # Task 1
            filter_departments,     # Task 2
            compute_average_salary  # Task 3
        ],
        start_time=datetime.now() + timedelta(seconds=2),
        name="employee_salary_analysis",
        conf="data.csv"
    )

    scheduler = Scheduler([workflow_employee_analysis])
    scheduler.run()
