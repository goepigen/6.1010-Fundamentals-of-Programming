import sounddevice as sd
import soundfile as sf
import lab


def record():
    duration = 6
    rate = 44100

    print("Recording...")
    audio = sd.rec(int(duration * rate), samplerate=rate, channels=2)
    sd.wait()
    sf.write("my_voice2.wav", audio, rate)
    print("Saved as my_voice2.wav")


if __name__ == "__main__":
    # record()
    sound1 = lab.load_wav("my_voice.wav", stereo=True)
    sound2 = lab.load_wav("my_voice2.wav", stereo=True)
    mixed = lab.mix_stereo(sound1, sound2, 0.5)
    backwards = lab.backwards_stereo(sound1)
    lab.write_wav(backwards, "my_backwards_voice.wav")
    lab.write_wav(mixed, "my_mixed_voice.wav")
