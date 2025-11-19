"""
Project Echo: The Brain (agent.py)

This script is the core of the accessibility agent. It is executed by the
Talon Voice trigger and performs the following actions:
1.  Parses a --mode argument to determine the user's intent.
2.  Captures a screenshot of the currently active window.
3.  Selects a specialized system prompt based on the chosen mode.
4.  Sends the image and prompt to the Google Gemini API.
5.  Speaks the AI's response back to the user via NVDA.
"""

import os
import io
import sys
import argparse
import dotenv
import pyautogui
import pygetwindow as gw
import google.generativeai as genai
from accessible_output2.outputs.nvda import NVDA


def get_prompt_for_mode(mode):
    """Returns the specialized system prompt for the given interaction mode."""
    prompts = {
        "brief": (
            "I am a blind user. Briefly describe the current window's purpose and "
            "state in a single sentence (max 30 words)."
        ),
        "actions": (
            "You are an expert accessibility assistant. Analyze this screenshot for a "
            "blind user. Provide a numbered list of all actionable UI elements "
            "(buttons, links, text inputs, menus, tabs). For each item, give its "
            "precise text label."
        ),
        "read": (
            "You are an expert OCR assistant for a blind user. Extract and read "
            "only the main body of text from this screenshot. Ignore UI elements "
            "like buttons and menus. If there is an error message, read that instead."
        ),
    }
    return prompts.get(mode, prompts["brief"])


def describe_screen(mode):
    """
    Takes a screenshot of the active window, sends it to the Gemini API with a
    mode-specific prompt, and speaks the description.
    """
    nvda = NVDA()

    # 1. Get API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        error_msg = "ERROR: Gemini API key not found in .env file."
        print(error_msg, file=sys.stderr)
        nvda.speak(error_msg)
        return

    try:
        # 2. Configure the Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-flash-latest")

        # 3. Take a screenshot of the active window
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                screenshot = pyautogui.screenshot(
                    region=(
                        active_window.left,
                        active_window.top,
                        active_window.width,
                        active_window.height,
                    )
                )
            else:
                screenshot = pyautogui.screenshot()
        except Exception:
            screenshot = pyautogui.screenshot()

        # 4. Convert screenshot to bytes
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

        image_part = {"mime_type": "image/png", "data": img_byte_arr}
        prompt_part = get_prompt_for_mode(mode)

        # 5. Send to Gemini API
        response = model.generate_content([prompt_part, image_part])

        # 6. Speak the response
        if response and response.text:
            nvda.speak(f"Gemini says: {response.text}")
        else:
            nvda.speak("API call successful, but no text in response.")

    except Exception as e:
        error_type = type(e).__name__
        error_msg = f"An error occurred: [{error_type}] {e}"
        print(error_msg, file=sys.stderr)
        nvda.speak("An error occurred. Please check the Talon log for details.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Project Echo Accessibility Agent"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["brief", "actions", "read"],
        default="brief",
        help="The interaction mode for the screen description.",
    )
    args = parser.parse_args()

    # Load environment variables from .env file located relative to this script
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    dotenv.load_dotenv(dotenv_path=dotenv_path)

    describe_screen(args.mode)