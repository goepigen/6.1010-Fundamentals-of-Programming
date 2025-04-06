# 6.101 recitation: lab 0 wrapup


############### Data representation

# sound is a dictionary, with keys
#    rate: int, the sampling rate, in samples per second
#    samples: a list of floats, the samples
sound = {"rate": 8000, "samples": [1, 2, 3]}
sound["rate"]
sound["samples"]

# OR:
# sound is a list whose first element is the rate and second is a sublist
# containing the samples
sound = [8000, [1, 2, 3]]
sound[0]
sound[1]

# OR:
# sound is a list whose first element is the rate, and remaining elements the
# samples
sound = [8000, 1, 2, 3]
sound[0]
sound[1:]

# what are pros and cons of each of these representations?


# OR: (coming later in semester)
# class Sound:
#    ...
# sound = Sound(8000, [1,2,3])
# sound.rate
# sound.samples
# isinstance(sound, Sound) ==> True


############### backwards

# what's good about this solution to backwards()?
# what could be improved?
# what might be buggy?


def backwards(sound):
    new_samples = sound["samples"]
    new_samples.reverse()
    return {
        "rate": sound["rate"],
        "samples": new_samples,
    }


############### mix

# what's good about this solution to mix?
# what could be improved?
# what might be buggy?


def mix(sound1, sound2, p):
    # initialize a new sound
    new_sound = {}

    # scale the input sounds by p and 1-p
    sound1_scaled = []
    for s in sound1["samples"]:
        sound1_scaled.append(s * p)
    sound2_scaled = []
    for s in sound1["samples"]:
        sound2_scaled.append(s * 1 - p)

    # combine the scaled sounds
    new_samples = []
    if len(sound1_scaled) < len(sound2_scaled):
        new_length = len(sound2_scaled)
    else:
        new_length = len(sound1_scaled)
    new_samples = [0] * new_length
    for i in range(new_length):
        new_samples[i] = sound1_scaled[i] + sound2_scaled[i]

    # fill in the new sound with the new samples
    new_sound["rate"] = sound["rate"]
    new_sound["samples"] = []
    for sample in new_samples:
        new_sound["samples"].append(sample)

    # return the mixed sound
    return new_sound



############ convolve


def convolve(sound, kernel):
    results = []
    for ix in range(len(kernel)):
        results.append([0] * ix + [kernel[ix] * val for val in sound["samples"]])
    out_samples = [0] * (len(sound["samples"]) + len(kernel) - 1)
    for result in results:
        for ix in range(len(result)):
            out_samples[ix] += result[ix]
    return {
        "rate": sound["rate"],
        "samples": out_samples,
    }


# this works, but it is very slow (and kind of hard to read!)
# opportunities for improvement?



######## echo

# two different approaches:

def echo(sound, num_echoes, delay, scale):
    inp_samples = sound["samples"]
    sample_delay = round(delay * sound["rate"])
    out = inp_samples + [0] * (num_echoes * sample_delay)
    for i in range(num_echoes):
        offset = (i + 1) * sample_delay
        this_scale = scale ** (i + 1)
        for j in range(len(inp_samples)):
            out[offset + j] += inp_samples[j] * this_scale
    return {
        "rate": sound["rate"],
        "samples": out,
    }


def echo(sound, num_echoes, delay, scale):
    delay_n = round(delay * sound["rate"])

    filter_ = [0] * (delay_n * num_echoes + 1)
    for i in range(num_echoes + 1):
        offset = i * delay_n
        filter_[offset] = scale**i

    return convolve(sound, filter_)

# pros and cons of each?
