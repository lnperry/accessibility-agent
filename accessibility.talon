# Project Echo: Voice Commands

# The core voice commands for interacting with the accessibility agent.
# These commands map spoken phrases to the different interaction modes.

Echo brief: user.accessibility_describe_screen("brief")
Echo actions: user.accessibility_describe_screen("actions")
Echo read: user.accessibility_describe_screen("read")