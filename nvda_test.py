from accessible_output2.outputs.nvda import NVDA


def speak_test_message():
    nvda = NVDA()
    nvda.speak("NVDA Test: NVDA test successful")


if __name__ == "__main__":
    speak_test_message()
