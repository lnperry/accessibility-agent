"""
Project Echo: The Talon Integration (accessibility.py)

This script acts as the bridge between Talon Voice commands and the core
agent. It defines the Python actions that are called by voice commands.
"""

from talon import Module, actions, app
import subprocess
import os
import sys

mod = Module()


@mod.action_class
class AccessibilityActions:
    def accessibility_describe_screen(mode: str):
        """
        Triggers the agent.py script to describe the screen using a specific
        interaction mode.
        """
        # Use os.path.expanduser to dynamically find the user's home directory
        # This makes the script portable across different machines.
        base_dir = os.path.join(os.path.expanduser("~"), "AccessibilityAgent")
        python_executable = os.path.join(base_dir, "venv", "Scripts", "python.exe")
        script_path = os.path.join(base_dir, "agent.py")

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
            # Note: We pass the --mode argument to the agent script
            proc = subprocess.Popen(
                [python_executable, script_path, "--mode", mode],
                cwd=base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            stdout, stderr = proc.communicate()
            if stdout:
                print(f"Agent STDOUT: {stdout.decode(errors='ignore')}")
            if stderr:
                print(
                    f"Agent STDERR: {stderr.decode(errors='ignore')}", file=sys.stderr
                )
                except Exception as e:
                    app.notify("ERROR: Failed to run script", f"Subprocess error: {e}")
        
            def accessibility_test():
                """A simple test command to confirm the script is working."""
                app.notify("Talon Test Successful!", "The test command was executed correctly.")
        
            def accessibility_test_output():
                """A test command to confirm output to NVDA."""
                base_dir = os.path.join(os.path.expanduser("~"), "AccessibilityAgent")
                python_executable = os.path.join(base_dir, "venv", "Scripts", "python.exe")
                script_path = os.path.join(base_dir, "nvda_test.py")
        
                if not os.path.exists(python_executable):
                    app.notify(
                        "ERROR: Python executable not found",
                        f"Path does not exist: {python_executable}",
                    )
                    return
        
                if not os.path.exists(script_path):
                    app.notify(
                        "ERROR: NVDA test script not found",
                        f"Path does not exist: {script_path}",
                    )
                    return
        
                try:
                    proc = subprocess.Popen(
                        [python_executable, script_path],
                        cwd=base_dir,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )
                    stdout, stderr = proc.communicate()
                    if stdout:
                        print(f"NVDA Test STDOUT: {stdout.decode(errors='ignore')}")
                    if stderr:
                        print(
                            f"NVDA Test STDERR: {stderr.decode(errors='ignore')}",
                            file=sys.stderr,
                        )
                except Exception as e:
                    app.notify(
                        "ERROR: Failed to run NVDA test script", f"Subprocess error: {e}"
                    )
        