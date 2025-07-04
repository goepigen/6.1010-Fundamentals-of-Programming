"""
6.101 Lab:
Audio Processing
"""

import wave
import struct

# No additional imports allowed!


def backwards(sound):
    """
    Returns a new sound containing the samples of the original in reverse
    order, without modifying the input sound.

    Args:
        sound: a dictionary representing the original mono sound

    Returns:
        A new mono sound dictionary with the samples in reversed order
    """

    samples = sound["samples"]

    reversed_samples = samples[::-1]

    return {**sound, "samples": reversed_samples}


def mix(sound1, sound2, weight_sound1):
    """
    Returns a new sound with samples being a weighted average of the samples from sound1 and sound2.

    Sampling rates must match.

    If length of samples differs, length of new sound is maximum of lengths of input samples.

    Parameters:
        sound1, sound2: Each is a dictionary representing a mono sound.
        weight_sound1 (float): number between 0 and 1 used as weight for sound1. 1 - weight_sound1 is weight on sound2.

    Returns:
        A new mono sound dictionary with samples being a mix from sound1 and sound2.
    """
    if (
        ("rate" not in sound1)
        or ("rate" not in sound2)
        or (sound1["rate"] != sound2["rate"])
    ):
        return None

    samples1 = sound1["samples"]
    samples2 = sound2["samples"]

    weighted_samples1 = [sample * weight_sound1 for sample in samples1]
    weighted_samples2 = [sample * (1 - weight_sound1) for sample in samples2]

    # Version 1: max and Iteration
    max_length = max(len(samples1), len(samples2))

    mixed_samples = [
        (weighted_samples1[i] if i < len(samples1) else 0)
        + (weighted_samples2[i] if i < len(samples2) else 0)
        for i in range(max_length)
    ]

    # Version 2: Uses if Statements
    #
    # length_diff = len(weighted_samples1) - len(weighted_samples2)
    #
    # if length_diff < 0:
    #     weighted_samples1.extend([0 for i in range(-length_diff)])
    # elif length_diff > 0:
    #     weighted_samples2.extend([0 for i in range(length_diff)])
    #
    # mixed_samples = [
    #     weighted_samples1[i] + weighted_samples2[i]
    #     for i in range(len(weighted_samples2))
    # ]

    # Version 3: Using List Comprehension with zip_longest

    # from itertools import zip_longest

    # mixed_samples = [
    #     sample1 + sample2
    #     for sample1, sample2 in zip_longest(
    #         weighted_samples1, weighted_samples2, fillvalue=0
    #     )
    # ]

    # Version 4: Using map and zip_longest
    # from itertools import zip_longest

    # mixed_samples = list(
    #     map(
    #         lambda zipped: zipped[0] + zipped[1],
    #         zip_longest(weighted_samples1, weighted_samples2, fillvalue=0),
    #     )
    # )

    # Version 5: Using zip() and Slicing
    # mixed_samples = (
    #     [
    #         sample1 + sample2
    #         for sample1, sample2 in zip(weighted_samples1, weighted_samples2)
    #     ]
    #     + weighted_samples1[len(weighted_samples2) :]
    #     + weighted_samples2[len(weighted_samples1) :]
    # )

    return {"rate": sound1["rate"], "samples": mixed_samples}  # return new sound


def convolve(sound, kernel):
    """
    Compute a new sound by convolving the given input sound with the given
    kernel.  Does not modify input sound.

    Args:
        sound: a dictionary representing the original mono sound
        kernel: list of numbers, the signal with which the sound should be
                convolved

    Returns:
        A new mono sound dictionary resulting from the convolution.
    """

    # Version 1: My Initial Version
    # samples = sound["samples"]

    # convolution = [0 for i in range(len(kernel) + len(samples) - 1)]

    # for shift, kernel_value in enumerate(kernel):
    #     scaled_samples = [sample * kernel_value for sample in samples]
    #     convolution = [
    #         convolution[i]
    #         + (
    #             scaled_samples[i - shift]
    #             if i >= shift and i < shift + len(scaled_samples)
    #             else 0
    #         )
    #         for i in range(len(convolution))
    #     ]
    #     print(convolution)

    # return {**sound, "samples": convolution}

    # Version 2: Nested loop
    # Note that version 1 also has an implicitly nested loop (in a list comprehension that is less readable
    # in particular, the shifting operation is done in a more complicated manner

    samples = sound["samples"]
    convolved = [0] * (len(samples) + len(kernel) - 1)

    # Perform convolution
    for i, k in enumerate(kernel):
        for j, sample in enumerate(samples):
            convolved[i + j] += (
                sample * k
            )  # scaling and shift are both concisely done in this step

    return {**sound, "samples": convolved}

    # Version 3: Similar to version 1: an implicitly nested for loop that requires complicated
    # logic in the list comprehension

    # samples = sound["samples"]
    # convolved = [0] * (len(samples) + len(kernel) - 1)

    # for i, k in enumerate(kernel):
    #     convolved = [
    #         sum(x)
    #         for x in zip(
    #             convolved,
    #             [0] * i
    #             + [s * k for s in samples]
    #             + [0] * (len(convolved) - len(samples) - i),
    #         )
    #     ]

    # return {**sound, "samples": convolved}

    # Version 4: Let numpy do the convolution
    # This isn't really an acceptable solution for this class since we're not doing the work, numpy is.

    # samples = np.array(sound["samples"])
    # kernel = np.array(kernel)

    # # Perform convolution using NumPy's built-in function
    # convolution = np.convolve(samples, kernel, mode="full").tolist()

    # return {**sound, "samples": convolution}


def echo(sound, num_echoes, delay, scale):
    """
    Compute a new sound consisting of several scaled-down and delayed versions
    of the input sound. Does not modify input sound.

    Args:
        sound: a dictionary representing the original mono sound
        num_echoes: int, the number of additional copies of the sound to add
        delay: float, the amount of seconds each echo should be delayed
        scale: float, the amount by which each echo's samples should be scaled

    Returns:
        A new mono sound dictionary resulting from applying the echo effect.
    """
    samples = sound["samples"]
    rate = sound["rate"]
    sample_delay = round(delay * rate)

    new_samples = samples + [0] * (num_echoes * sample_delay)

    for i in range(1, num_echoes + 1):
        echo_start = i * sample_delay
        echo_scale = scale**i

        for j, s in enumerate(samples):
            new_samples[echo_start + j] += s * echo_scale

    return {**sound, "samples": new_samples}

    # Version 2: Let numpy do the work

    # samples = np.array(sound["samples"], dtype=float)
    # rate = sound["rate"]
    # sample_delay = int(round(delay * rate))
    # total_length = len(samples) + num_echoes * sample_delay

    # new_samples = np.zeros(total_length)

    # new_samples[: len(samples)] += samples

    # for i in range(1, num_echoes + 1):å
    #     offset = i * sample_delay
    #     new_samples[offset : offset + len(samples)] += samples * (scale**i)

    # return {**sound, "samples": new_samples}


def pan(sound):
    """
    Creates the spatial effect of panning, whereby the samples in the right channel are scaled by factors that are
    equally spaced from 0 (for the first sample) and 1 (for the last sample), and the samples in the left channel are
    scaled the same factors but in reverse order.
    Args:
    sound: a dictionary representing a stereo sound.

    Returns:
    A new stereo sound resulting from applying the pan effect.
    """
    right = sound["right"]
    left = sound["left"]

    length = len(right)

    panned_right = [sample * i / (length - 1) for i, sample in enumerate(right)]

    panned_left = [sample * (1 - i / (length - 1)) for i, sample in enumerate(left)]

    return {**sound, "right": panned_right, "left": panned_left}


def remove_vocals(sound):
    """
    Assumes that vocals are recorded in mono and played equally in right and left
    channels. Tries to remove vocals by generating a mono sound that is the result of
    subtracting the samples in the right channel from the samples in the left channel.

    Args:
    sound: a dictionary representing the original mono sound

    Returns:
    A new mono sound dictionary resulting from trying to remove vocals using the
    algorithm described above.
    """
    return {
        **sound,
        "samples": [left - right for left, right in zip(sound["left"], sound["right"])],
    }


def bass_boost_kernel(n_val, scale=0):
    """
    Construct a kernel that acts as a bass-boost filter.

    We start by making a low-pass filter, whose frequency response is given by
    (1/2 + 1/2cos(Omega)) ^ n_val

    Then we scale that piece up and add a copy of the original signal back in.
    """
    # make this a fake "sound" so that we can use the convolve function
    base = {"rate": 0, "samples": [0.25, 0.5, 0.25]}
    kernel = {"rate": 0, "samples": [0.25, 0.5, 0.25]}
    for i in range(n_val):
        kernel = convolve(kernel, base["samples"])
    kernel = kernel["samples"]

    # at this point, the kernel will be acting as a low-pass filter, so we
    # scale up the values by the given scale, and add in a value in the middle
    # to get a (delayed) copy of `the original
    kernel = [i * scale for i in kernel]
    kernel[len(kernel) // 2] += 1

    return kernel


# Extra Credit
def backwards_stereo(sound):
    right = sound["right"]
    left = sound["left"]

    backwards_right = backwards({**sound, "samples": right})
    backwards_left = backwards({**sound, "samples": left})

    return {
        **sound,
        "right": backwards_right["samples"],
        "left": backwards_left["samples"],
    }


def mix_stereo(sound1, sound2, weight_sound1):
    """

    Returns a new stereo sound with right samples being a weighted average of the right samples from sound1
    and sound2, and the left samples being the equivalent weighted average for the left samples.

    Sampling rates must match.

    If length of samples differs, length of new sound is maximum of lengths of input samples.

    Parameters:
        sound1, sound2: Each is a dictionary representing a stereo sound.
        weight_sound1 (float): number between 0 and 1 used as weight for sound1. 1 - weight_sound1 is weight on sound2.

    Returns:
        A new stereo sound dictionary with right and left samples being a mix from sound1 and sound2.
    """
    if (
        ("rate" not in sound1)
        or ("rate" not in sound2)
        or (sound1["rate"] != sound2["rate"])
    ):
        return None

    right1 = sound1["right"]
    left1 = sound1["left"]

    right2 = sound2["right"]
    left2 = sound2["left"]

    mixed_right = mix(
        {**sound1, "samples": right1}, {**sound2, "samples": right2}, weight_sound1
    )
    mixed_left = mix(
        {**sound1, "samples": left1}, {**sound2, "samples": left2}, weight_sound1
    )

    return {
        "rate": sound1["rate"],
        "right": mixed_right["samples"],
        "left": mixed_left["samples"],
    }


# below are `hel`per functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds


def load_wav(filename, stereo=False):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    file = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = file.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    if stereo:
        left = []
        right = []
        for i in range(count):
            frame = file.readframes(1)
            if chan == 2:
                left.append(struct.unpack("<h", frame[:2])[0])
                right.append(struct.unpack("<h", frame[2:])[0])
            else:
                datum = struct.unpack("<h", frame)[0]
                left.append(datum)
                right.append(datum)

        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = []
        for i in range(count):
            frame = file.readframes(1)
            if chan == 2:
                left = struct.unpack("<h", frame[:2])[0]
                right = struct.unpack("<h", frame[2:])[0]
                samples.append((left + right) / 2)
            else:
                datum = struct.unpack("<h", frame)[0]
                samples.append(datum)

        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for left, right in zip(sound["left"], sound["right"]):
            left = int(max(-1, min(1, left)) * (2**15 - 1))
            right = int(max(-1, min(1, right)) * (2**15 - 1))
            out.append(left)
            out.append(right)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


if __name__ == "__main__":
    import sys

    # Testing of backwards
    # sound_name = sys.argv[1]
    # sound = load_wav("sounds/" + sound_name + ".wav")
    # backwards_sound = backwards(sound)
    # write_wav(backwards_sound, sound_name + "_reversed.wav")

    # Testing of mixed_sound
    # sound1_name = sys.argv[1]
    # sound2_name = sys.argv[2]

    # sound1 = load_wav("sounds/" + sound1_name + ".wav")
    # sound2 = load_wav("sounds/" + sound2_name + ".wav")

    # mixed_sound = mix(sound1, sound2, 0.2)

    # write_wav(mixed_sound, sound1_name + sound2_name + "_mixed.wav")

    # Testing of convolution
    # sound_name = sys.argv[1]
    # N = int(sys.argv[2])
    # scale = float(sys.argv[3])

    # sound = load_wav("sounds/" + sound_name + ".wav")

    # kernel = bass_boost_kernel(N, scale)

    # convolved_sound = convolve(sound, kernel)
    # write_wav(convolved_sound, sound_name + "_convolved.wav")

    # Testing of mix_stereo
