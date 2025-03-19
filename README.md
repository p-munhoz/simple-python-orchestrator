# Simple Python Workflow Orchestrator

A practical and minimalistic Python-based workflow orchestrator demonstrating the principles of data pipeline management, scheduling, and task orchestration. This project serves as an educational resource to illustrate core orchestration concepts similar to those found in popular tools like Apache Airflow.

Read the full beginner guide to dbt-core here: [🔗 Article](https://p-munhoz.github.io/blog/python/simple-python-orchestrator)

## Project Overview

This workflow orchestrator consists of two primary components that communicate using ZeroMQ:

- **Scheduler**: Manages the timing and sequencing of workflows.
- **Worker**: Executes tasks received from the Scheduler and returns the results.

The orchestrator allows for sequential data processing tasks, where the output from one task seamlessly serves as the input for the next.

## Architecture

The orchestrator architecture is designed to clearly separate concerns:

- The **Scheduler** maintains workflows, scheduling them based on their configured execution time.
- Each **Workflow** consists of sequential tasks defined by Python callables.
- The **Worker** listens for tasks sent by the Scheduler, executes them, and returns results.

## Key Features

- **Sequential Task Execution**: Ensures tasks are processed in the correct order.
- **Communication via ZeroMQ**: Reliable and efficient inter-process communication.
- **Fault Isolation**: The Scheduler remains stable even if the Worker encounters errors.
- **Human-in-the-loop Capability**: Example provided for manual validation tasks.

## Project Structure

```
.
├── scheduler.py       # Manages workflow scheduling and task sequencing
├── worker.py          # Receives and executes tasks
├── fake_data.py       # Generates sample employee data for workflow
├── source.py          # Contains definitions of processing tasks
├── data.csv           # Example input data for processing
├── average_salary.csv # Example output data from processing workflow
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- ZeroMQ

### Installation

1. Clone the repository:

```bash
git clone https://github.com/p-munhoz/simple-python-orchestrator.git
cd simple-python-orchestrator
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Orchestrator

Run the Worker in one terminal:

```bash
python worker.py
```

Run the Scheduler in another terminal:

```bash
python scheduler.py
```

## Example Workflow

The provided workflow example processes employee data (`data.csv`) by:

1. Reading employee data from a CSV file.
2. Filtering employees by specific departments (e.g., 'IT', 'Finance').
3. Calculating the average salary per department.

To customize tasks or create new workflows, define new Python callables in `source.py` and update the Scheduler accordingly.

## Dependencies

Major Python libraries used:

- `pandas`
- `pyzmq`
- `numpy`
- `pickle`

(Full dependency list available in `requirements.txt`)

## Future Enhancements

Potential improvements for production usage include:

- Persistent workflow states in a database
- Task retries with exponential backoff
- Enhanced logging and monitoring
- Parallel task execution
- Security through authentication
- Web-based workflow management UI

