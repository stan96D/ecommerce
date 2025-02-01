import time


class ProgressManager:
    def __init__(self):
        self.logs = []
        self.status = {}
        self.start_times = {}
        self.reports = {}

    def log(self, level, message, context=None):
        """
        Log a message with a specified level and optional context.
        :param level: Log level (e.g., INFO, WARNING, ERROR).
        :param message: Log message.
        :param context: Optional dictionary with additional context information.
        """
        entry = {"level": level, "message": message,
                 "context": context, "timestamp": time.time()}
        self.logs.append(entry)
        print(f"[{level}] {message}" +
              (f" | Context: {context}" if context else ""))

    def start_task(self, task_name, total_steps=None):
        """
        Initialize tracking for a new task.
        :param task_name: Name of the task to track.
        :param total_steps: Optional total number of steps for the task.
        """
        self.status[task_name] = {
            "completed_steps": 0,
            "total_steps": total_steps,
            "status": "in_progress",
            "estimated_time_remaining": None,
        }
        self.start_times[task_name] = time.time()
        self.log("INFO", f"Task '{task_name}' started.", {
                 "total_steps": total_steps})

    def update_task(self, task_name, steps=1):
        """
        Update the progress of a task and calculate the estimated time remaining.
        :param task_name: Name of the task to update.
        :param steps: Number of steps completed since the last update.
        """
        if task_name in self.status:
            task_status = self.status[task_name]
            task_status["completed_steps"] += steps

            total = task_status["total_steps"]
            elapsed_time = time.time() - self.start_times[task_name]

            if total:
                percentage = (task_status["completed_steps"] / total) * 100
                remaining_steps = total - task_status["completed_steps"]

                if task_status["completed_steps"] > 0:
                    average_time_per_step = elapsed_time / \
                        task_status["completed_steps"]
                    estimated_time_remaining = remaining_steps * average_time_per_step
                    task_status["estimated_time_remaining"] = estimated_time_remaining

                    self.log("INFO", f"Task '{task_name}' progress: {percentage:.2f}% complete.", {
                        "steps_completed": steps,
                        "elapsed_time": elapsed_time,
                        "estimated_time_remaining": estimated_time_remaining,
                    })
                else:
                    self.log("INFO", f"Task '{task_name}' progress updated.", {
                             "steps_completed": steps})
            else:
                self.log("INFO", f"Task '{task_name}' progress updated.", {
                         "steps_completed": steps})

    def complete_task(self, task_name):
        """
        Mark a task as completed.
        :param task_name: Name of the task to complete.
        """
        if task_name in self.status:
            self.status[task_name]["status"] = "completed"
            self.status[task_name]["estimated_time_remaining"] = 0
            total_time = time.time() - self.start_times[task_name]
            self.log("INFO", f"Task '{task_name}' completed.", {
                     "total_time": total_time})

    def fail_task(self, task_name, error):
        """
        Mark a task as failed with an error message.
        :param task_name: Name of the task to fail.
        :param error: Error message or exception details.
        """
        if task_name in self.status:
            self.status[task_name]["status"] = "failed"
            total_time = time.time() - self.start_times[task_name]
            self.log("ERROR", f"Task '{task_name}' failed.", {
                     "error": str(error), "elapsed_time": total_time})

    def generate_report(self):
        """
        Generate a summary report of all tasks and logs.
        :return: Dictionary summarizing tasks and logs.
        """
        self.reports = {"tasks": self.status, "logs": self.logs}
        return self.reports
