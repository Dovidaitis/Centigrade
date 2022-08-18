from gtts import gTTS
from playsound import playsound

language = "en"

instructions = [
    {"recheck_temp":"Please recheck yuor temperature with a nurse"},
    {"normal_temp":"Your temperature is normal"},
    {"closer":"Come closer to the sensor"},
    {"scan_rfid":"Please scan your identification card"}
    ]

def generate_audio_instruction():
    for instruction in instructions:
        for key in instruction:
            print(f'file {key}.mp3 was created with text: \n{instruction[key]}')
            gTTS(text=instruction[key], lang=language, slow=False).save(f'./{key}.mp3')

# generate_audio_instruction()
# playsound("./closer.mp3")