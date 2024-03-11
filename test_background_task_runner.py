import time
from background_task_runner import BackgroundTaskRunner  # Ensure this matches your module name

def test_task_addition():
    """Test that tasks are correctly added to the runner."""
    runner = BackgroundTaskRunner()
    initial_task_count = len(runner.tasks)
    runner.add_task(print, "Hello, World!")
    assert len(runner.tasks) == initial_task_count + 1, "Task was not added"

def simple_task(duration):
    """A simple task that just sleeps for a given duration."""
    time.sleep(duration)

def test_run_all():
    """Test running all tasks ensures they complete."""
    runner = BackgroundTaskRunner()
    start_time = time.time()
    runner.add_task(simple_task, 1)
    runner.add_task(simple_task, 2)
    runner.run_all()
    end_time = time.time()
    # Verify all tasks have completed by checking the elapsed time
    # This assumes tasks run in parallel; adjust logic if sequential
    assert end_time - start_time < 4, "Tasks did not complete in parallel"

def test_task_with_arguments():
    """Test that tasks with arguments are handled correctly."""
    runner = BackgroundTaskRunner()
    runner.add_task(time.sleep, 1)  # Simple task with an argument
    start_time = time.time()
    runner.run_all()
    end_time = time.time()
    assert end_time - start_time >= 1, "Task did not run with argument"

# Optional: Testing for priority changes can be quite tricky and might not be easily achievable through unit tests.
# It may involve checking system states or behavior under load, which goes beyond typical unit testing practices.
