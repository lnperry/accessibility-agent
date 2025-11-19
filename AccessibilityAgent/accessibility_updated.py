from talon import Module, actions, app
import subprocess
import os

mod = Module()


@mod.action_class
class AccessibilityActions:
    def accessibility_describe_screen():
        """Triggers the agent.py script to describe the screen."""
        app.notify(
            "Describe command recognized!",
            "Attempting to run screen description script.",
        )

        python_executable = r"C:\AccessibilityAgent\venv\Scripts\python.exe"
        script_dir = r"C:\AccessibilityAgent"
        script_path = os.path.join(script_dir, "agent.py")

        if not os.path.exists(python_executable):
            app.notify(
                "ERROR: Python executable not found",
                f"Path does not exist: {python_executable}",
            )
            return

        if not os.path.exists(script_path):
            app.notify(
                "ERROR: Agent script not found", f"Path does not exist: {script_path}"
            )
            return

        try:
            subprocess.Popen([python_executable, script_path], cwd=script_dir)
        except Exception as e:
            app.notify("ERROR: Failed to run script", f"Subprocess error: {e}")

    def accessibility_test():
        """A simple test command to confirm the script is working."""
        app.notify("Talon Test Successful!", "The test command was executed correctly.")
