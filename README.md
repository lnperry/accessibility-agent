# Accessibility Agent

This project is a prototype for a multimodal accessibility assistant for Windows, designed to replace traditional screen readers like JAWS and Dragon with a more interactive, AI-powered experience.

## How It Works

The agent uses the Talon Voice toolkit to capture voice commands. When a command is given, a Python script is triggered which can perform various actions, such as taking a screenshot of the screen. This screenshot is then sent to a multimodal AI model (Google's Gemini) to get a description of the current UI, which is then spoken back to the user via the NVDA screen reader.

This architecture uses a "Subprocess Pattern", meaning the heavy lifting (like API calls) is done in a standalone Python script, keeping the Talon environment lightweight.

## Setup

1.  **Clone the repository.**
2.  **Create and activate a Python virtual environment:**
    ```shell
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```shell
    pip install -r requirements.txt
    ```
    *(Note: We will create the `requirements.txt` file in a later step.)*
4.  **Create a `.env` file** in the root of the project and add your Gemini API key:
    ```
    GEMINI_API_KEY=AIzaSy...
    ```
5.  **Place Talon Scripts:** Copy the `accessibility.py` and `accessibility.talon` files from this project into your Talon user scripts folder (`%APPDATA%\talon\user`).

## Usage

With Talon and NVDA running, you can use the following voice commands:

*   **`describe`**: Takes a screenshot and has the Gemini model describe what's on screen.
*   **`test output`**: A simple test to confirm that the script can speak through NVDA.
*   **`test`**: A simple test to confirm that the Talon commands are being recognized.
