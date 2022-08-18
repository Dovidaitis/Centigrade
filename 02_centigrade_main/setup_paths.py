import sys

modules_to_import = [
    "apis",
    "computer_vision",
    "audio_instructions"
]

for module in modules_to_import:
    try:
        sys.path.append(f"./{module}")
    except Exception as e:
        print(e)