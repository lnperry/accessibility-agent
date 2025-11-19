import os
import io
import sys
import dotenv
import pyautogui
import pygetwindow as gw
import google.generativeai as genai
from accessible_output2.outputs.nvda import NVDA

# --- SCRIPT START ---
print("Agent script started.")

# Load environment variables from .env file
dotenv.load_dotenv()


def describe_screen():
    """
    Takes a screenshot, sends it to the Gemini API, and speaks the description.
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
        print("Configuring Gemini API...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-flash-latest")
        print("Gemini API configured successfully.")

        # 3. Take a screenshot of the active window
        print("Getting active window and taking screenshot...")
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                # Capture the region of the active window
                screenshot = pyautogui.screenshot(
                    region=(
                        active_window.left,
                        active_window.top,
                        active_window.width,
                        active_window.height,
                    )
                )
                print("Screenshot of active window taken successfully.")
            else:
                # Fallback to full screen if no active window
                screenshot = pyautogui.screenshot()
                print("No active window found, took full screenshot.")
        except Exception as e:
            # Fallback to full screen on any error (e.g., window minimized)
            print(f"Could not get active window ({e}), taking full screenshot.")
            screenshot = pyautogui.screenshot()

        # 4. Convert screenshot to bytes
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()
        print("Screenshot converted to bytes.")

        image_part = {"mime_type": "image/png", "data": img_byte_arr}
        prompt_part = "I am a blind user. Briefly describe the UI element or window state currently in focus. Be concise."

        # 4. Send to Gemini API
        print("Sending request to Gemini API...")
        response = model.generate_content([prompt_part, image_part])
        print("Response received from Gemini API.")

        # 5. Speak the response
        if response and response.text:
            print(f"Response text: {response.text}")
            nvda.speak(f"Gemini says: {response.text}")
        else:
            error_msg = "API call successful, but no text in response."
            print(error_msg, file=sys.stderr)
            nvda.speak(error_msg)

    except Exception as e:
        # Detailed error logging
        error_type = type(e).__name__
        error_msg = f"An error occurred in the agent script: [{error_type}] {e}"
        print(error_msg, file=sys.stderr)
        nvda.speak("An error occurred. Please check the Talon log for details.")


if __name__ == "__main__":
    describe_screen()

print("Agent script finished.")
