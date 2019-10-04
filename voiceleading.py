import music21
from music21 import pitch, interval, voiceLeading as m21vl
import pytest
import itertools


def get_num_parts(stream):
    return len(stream.getElementsByClass("Part"))


def get_missing_notes(chordified_stream):
    chords = chordified_stream.recurse().getElementsByClass("Chord")
    return [chord for chord in chords if len(chord.pitches) < 4]


def get_parts_out_of_range(stream):
    VOICE_RANGES = [
        {"part": "S", "min": pitch.Pitch("B3"), "max": pitch.Pitch("A5")},
        {"part": "A", "min": pitch.Pitch("G3"), "max": pitch.Pitch("D5")},
        {"part": "T", "min": pitch.Pitch("C3"), "max": pitch.Pitch("F4")},
        {"part": "B", "min": pitch.Pitch("D2"), "max": pitch.Pitch("D4")}
    ]
    parts = []
    for part in stream.getElementsByClass("Part"):
        parts.append(
            {
                "stream": part,
                "range": {"min": min(part.pitches), "max": max(part.pitches)},
            }
        )
    parts = sorted(parts, key=lambda p: p["range"]["max"], reverse=True)
    for i, (part, voice_range) in enumerate(zip(parts, VOICE_RANGES)):
        parts[i]["out_of_range"] = [
            pitch
            for pitch in part["stream"].pitches
            if (pitch < voice_range["min"] or pitch > voice_range["max"])
        ]
    return [part for part in parts if len(part["out_of_range"]) > 0]


# consider how to handle modulation
def get_doubled_leading_tones(chordified_stream):
    key = chordified_stream.analyze("key")
    bad_chords = []
    for chord in chordified_stream.recurse().getElementsByClass("Chord"):
        intervals_from_tonic = [
            interval.Interval(noteStart=key.tonic, noteEnd=pitch).simpleName
            for pitch in chord
        ]
        leading_tones = sum(
            [1 for i in intervals_from_tonic if (i == "M7" or i == "m2")]
        )
        if leading_tones >= 2:
            bad_chords.append(chord)
    return bad_chords


def get_omitted_thirds(chordified_stream):
    bad_chords = []
    for chord in chordified_stream.recurse().getElementsByClass("Chord"):
        if chord.getChordStep(3) is None:
            bad_chords.append(chord)
    return bad_chords


# No vertical intervals between adjacent voices greater than octaves, 
# excluding bass
def get_overspacing(chordified_stream):
    bad_chords = []
    for chord in chordified_stream.recurse().getElementsByClass("Chord"):
        pitches = sorted(chord.pitches, reverse=True)
        t_to_a = interval.Interval(noteStart=pitches[2], noteEnd=pitches[1])
        a_to_s = interval.Interval(noteStart=pitches[1], noteEnd=pitches[0])
        if max(t_to_a.cents, a_to_s.cents) > 1200:
            bad_chords.append(chord)
    return bad_chords


def get_melodic_aug_2(stream):
    bad_intervals = []
    for part in stream.recurse().getElementsByClass("Part"):
        part = part.flat
        notes = part.getElementsByClass("Note").notes
        for n1, n2 in zip(notes[:-1], notes[1:]):
            intvl = interval.Interval(noteStart=n1, noteEnd=n2)
            if intvl.simpleName in ("A2","A-2"):
                bad_intervals.append(intvl)
    return bad_intervals


# This function exists primarily to prefill arguments
def get_notes_at_offset(stream, offset):
    filtered_stream = stream.flat.getElementsByOffset(
        offsetStart = offset,
        offsetEnd = offset,
        includeElementsThatEndAtStart=False
    )
    return list(filtered_stream.notes)[0]


def process_vlqs(fn, stream, chordified_stream):
    bad_intervals = []
    chordified_stream = chordified_stream.flat
    offsets = [
        note.getOffsetBySite(chordified_stream)
        for note
        in chordified_stream.notes
    ]
    parts = [p.flat for p in stream.recurse().getElementsByClass("Part")]
    # should be identifying and feeding in S, A, T, B earlier
    for p1, p2 in itertools.combinations(parts, 2):
        for o1, o2 in zip(offsets[:-1], offsets[1:]):
            n1s = list(map(lambda p: get_notes_at_offset(p, o1), (p1, p2)))
            n2s = list(map(lambda p: get_notes_at_offset(p, o2), (p1, p2)))
            vlq = m21vl.VoiceLeadingQuartet(n1s[0], n2s[0], n1s[1], n2s[1])
            if fn(vlq):
                bad_intervals.append({
                    "o1": o1, 
                    "o2": o2, 
                    "p1": p1, 
                    "p2": p2
                    })
    return bad_intervals


def get_parallel_fifths(stream, chordified_stream):
    return process_vlqs(
        lambda vlq: vlq.parallelFifth(), 
        stream, 
        chordified_stream
        )


def get_d5_to_p5(stream, chordified_stream):
    def helper(vlq):
        is_d5 = vlq.vIntervals[0].simpleName in ["d5","d-5"]
        is_p5 = vlq.vIntervals[1].simpleName in ["P5","P-5"]
        return (is_d5 and is_p5)
    return process_vlqs(
        helper, 
        stream, 
        chordified_stream
        )


# Function below inclues parallel unisons
def get_parallel_octaves(stream, chordified_stream):
    return process_vlqs(
        lambda vlq: vlq.parallelOctave(), 
        stream, 
        chordified_stream
        )


def get_hidden_fifths(stream, chordified_stream):
    return process_vlqs(
        lambda vlq: vlq.hiddenFifth(), 
        stream, 
        chordified_stream
    )


def get_hidden_octaves(stream, chordified_stream):
    return process_vlqs(
        lambda vlq: vlq.hiddenOctave(), 
        stream, 
        chordified_stream
    )


def get_crossed_voices(stream, chordified_stream):
    return process_vlqs(
        lambda vlq: vlq.voiceCrossing(), 
        stream, 
        chordified_stream
    )


def check_file(fname):
    input_stream = music21.converter.parse(fname)
    chordified_stream = input_stream.chordify()
    output_stream = input_stream

    # Implement flag system once have items to pass in.
    # Note that this relies on partwise xml file construction; consider for 
    if get_num_parts(input_stream) != 4:
        # throw error rather than writing anything
        print("Oops, not four parts")

    missing_notes = get_missing_notes(chordified_stream)    
    for chord in missing_notes:
        o = chord.getOffsetBySite(chordified_stream.flat)



    output_stream.write("musicxml", "output/"+fname+"_checked.xml")
    return