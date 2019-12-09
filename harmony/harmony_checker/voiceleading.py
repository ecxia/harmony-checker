import music21
from music21 import pitch, interval, voiceLeading as m21vl
import pytest
import itertools
from os import path


def get_num_parts(stream, **kwargs):
    parts = stream.getElementsByClass("Part")
    if len(parts) < 4:
        return [{
            "offset": 0, "part": parts[len(parts)-1].partAbbreviation, "msg": "Not enough parts"
        }]
    if len(parts) > 4:
        return [{
            "offset": 0, "part": parts[len(parts)-1].partAbbreviation, "msg": "Too many parts"
        }]
    return []


# Helper function
def get_note_at_offset(stream, offset):
    filtered_stream = stream.flat.getElementsByOffset(
        offsetStart=offset, offsetEnd=offset, includeElementsThatEndAtStart=False
    )
    notes = list(filtered_stream.notes)
    if len(notes) == 0:
        return []
    return list(filtered_stream.notes)[0]


def get_missing_notes(stream, **kwargs):
    chordified_stream = kwargs['chordified_stream']
    parts = stream.getElementsByClass("Part")
    chords = chordified_stream.recurse().getElementsByClass("Chord")
    missing_note_offsets = [
        chord.getOffsetBySite(chordified_stream.flat) 
        for chord in chords if len(chord.pitches) < 4
    ]
    missing_notes = []
    for offset in missing_note_offsets:
        for part in parts:
            if get_note_at_offset(part, offset) == []:
                missing_notes.append({
                    'offset': offset,
                    'part': part.partAbbreviation,
                    'msg': "Missing Note"
                })
    return missing_notes


def get_parts_out_of_range(stream, **kwargs):
    VOICE_RANGES = {
        "S.": {"min": pitch.Pitch("B3"), "max": pitch.Pitch("A5")},
        "A.": {"min": pitch.Pitch("G3"), "max": pitch.Pitch("D5")},
        "T.": {"min": pitch.Pitch("C3"), "max": pitch.Pitch("F4")},
        "B.": {"min": pitch.Pitch("D2"), "max": pitch.Pitch("D4")},
    }
    parts = []
    for part in stream.getElementsByClass("Part"):
        parts.append({
            "stream": part,
            "range": {"min": min(part.pitches), "max": max(part.pitches)},
        })
    parts = sorted(parts, key=lambda p: p["range"]["max"], reverse=True)
    problems = []
    for part in parts:
        voice_range = VOICE_RANGES[part["stream"].partAbbreviation]
        for note in part["stream"].flat.notes:
            if (note.pitch < voice_range["min"] or note.pitch > voice_range["max"]):
                problems.append({
                    "offset": note.getOffsetBySite(stream.flat),
                    "part": part["stream"].partAbbreviation,
                    "msg": "Part out of range"
                })
    return problems


# consider how to handle modulation
def get_doubled_leading_tones(stream, **kwargs):
    parts = stream.getElementsByClass("Part")
    chordified_stream = kwargs['chordified_stream']
    key = chordified_stream.analyze("key")
    bad_notes = []
    for chord in chordified_stream.recurse().getElementsByClass("Chord"):
        offset = chord.getOffsetBySite(chordified_stream.flat)
        intervals_from_tonic = [
            interval.Interval(noteStart=key.tonic, noteEnd=pitch) for pitch in chord
        ]
        leading_tones = [
            intvl.noteEnd
            for intvl in intervals_from_tonic
            if (intvl.simpleName == "M7" or intvl.simpleName == "m2")
        ]

        if len(leading_tones) >= 2:
            for part in parts:
                if get_note_at_offset(part, offset) in leading_tones:
                    bad_notes.append({
                        "offset": offset,
                        "part": part.partAbbreviation,
                        "msg": "Doubled Leading Tone"
                    })
    return bad_notes


def get_omitted_thirds(stream, **kwargs):
    parts = stream.getElementsByClass("Part")
    bottom_part = parts[len(parts)-1]
    chordified_stream = kwargs['chordified_stream']
    bad_chords = []
    for chord in chordified_stream.recurse().getElementsByClass("Chord"):
        offset = chord.getOffsetBySite(chordified_stream.flat)
        if chord.getChordStep(3) is None:
            bad_chords.append({
                "offset": offset,
                "part": bottom_part.partAbbreviation,
                "msg": "Omitted Third"
            })
    return bad_chords


# No vertical intervals between adjacent voices greater than octaves,
# excluding bass
def get_overspacing(stream, **kwargs):
    chordified_stream = kwargs['chordified_stream']
    parts = stream.getElementsByClass("Part")
    bad_chords = []
    for chord in chordified_stream.recurse().getElementsByClass("Chord"):
        offset = chord.getOffsetBySite(chordified_stream.flat)
        pitches = {
            part.partAbbreviation: get_note_at_offset(part, offset).pitch 
            for part in parts
        }
        bad_parts = set()
        t_to_a = interval.Interval(noteStart=pitches["T."], noteEnd=pitches["A."])
        if t_to_a.cents > 1200:
            bad_parts.add("T.")
            bad_parts.add("A.")            
        a_to_s = interval.Interval(noteStart=pitches["A."], noteEnd=pitches["S."])
        if a_to_s.cents > 1200:
            bad_parts.add("A.")
            bad_parts.add("S.")
        for part in parts:
            if part.partAbbreviation in bad_parts:
                bad_chords.append({
                    "offset": offset,
                    "part": part.partAbbreviation,
                    "msg": "Overspaced Chord"
                })
    return bad_chords


def get_melodic_aug_2(stream, **kwargs):
    bad_intervals = []
    for part in stream.recurse().getElementsByClass("Part"):
        part = part.flat
        notes = part.getElementsByClass("Note").notes
        for n1, n2 in zip(notes[:-1], notes[1:]):
            intvl = interval.Interval(noteStart=n1, noteEnd=n2)
            if intvl.simpleName in ("A2", "A-2"):
                bad_intervals.append({ 
                    'offsets': (
                        n1.getOffsetBySite(part.flat),
                        n2.getOffsetBySite(part.flat)
                    ),
                    'part': part.partAbbreviation,
                    'msg': "Aug 2 ->"
                })
    return bad_intervals


def process_vlqs(fn, stream, chordified_stream, msg):
    bad_intervals = []
    chordified_stream = chordified_stream.flat
    offsets = [
        note.getOffsetBySite(chordified_stream) for note in chordified_stream.notes
    ]
    parts = [p.flat for p in stream.recurse().getElementsByClass("Part")]
    # should be identifying and feeding in S, A, T, B earlier
    for p1, p2 in itertools.combinations(parts, 2):
        for o1, o2 in zip(offsets[:-1], offsets[1:]):
            n1s = list(map(lambda p: get_note_at_offset(p, o1), (p1, p2)))
            n2s = list(map(lambda p: get_note_at_offset(p, o2), (p1, p2)))
            vlq = m21vl.VoiceLeadingQuartet(n1s[0], n2s[0], n1s[1], n2s[1])
            if fn(vlq):
                bad_intervals.extend([
                    {"offsets": (o1, o2), "part": p1.partAbbreviation, "msg": msg},
                    {"offsets": (o1, o2), "part": p2.partAbbreviation, "msg": msg}
                ])
    return bad_intervals


def get_parallel_fifths(stream, **kwargs):
    chordified_stream = kwargs['chordified_stream']
    return process_vlqs(
        lambda vlq: vlq.parallelFifth(), 
        stream, 
        chordified_stream, 
        "Parallel 5ths ->"
    )


def get_d5_to_p5(stream, **kwargs):
    chordified_stream = kwargs['chordified_stream']
    def helper(vlq):
        is_d5 = vlq.vIntervals[0].simpleName in ["d5", "d-5"]
        is_p5 = vlq.vIntervals[1].simpleName in ["P5", "P-5"]
        return is_d5 and is_p5

    return process_vlqs(helper, stream, chordified_stream, "D5 to P5 ->")


# Function below inclues parallel unisons
def get_parallel_octaves(stream, **kwargs):
    chordified_stream = kwargs['chordified_stream']
    return process_vlqs(
        lambda vlq: vlq.parallelOctave(), 
        stream, 
        chordified_stream,
        "Parallel 8ves ->"
    )


# rewrite so focuses on outer voices
def get_hidden_fifths(stream, **kwargs):
    chordified_stream = kwargs['chordified_stream']
    return process_vlqs(
        lambda vlq: vlq.hiddenFifth(), 
        stream, 
        chordified_stream,
        "Hidden 5ths ->"
    )


# rewrite so focuses on outer voices
def get_hidden_octaves(stream, **kwargs):
    chordified_stream = kwargs['chordified_stream']
    return process_vlqs(
        lambda vlq: vlq.hiddenOctave(), 
        stream, 
        chordified_stream,
        "Hidden 8ves =>"
    )


# rewrite so focuses on outer voices
def get_crossed_voices(stream, **kwargs):
    chordified_stream = kwargs['chordified_stream']
    return process_vlqs(
        lambda vlq: vlq.voiceCrossing(), 
        stream, 
        chordified_stream,
        "Crossed Voices ->"
    )

# fix brackets
def annotate_stream(issues, stream, end_height):
    for issue in issues:
        msg = issue['msg']
        part = [
            p for p in stream.getElementsByClass("Part") 
            if p.partAbbreviation == issue['part']
        ][0]
        if "offset" in issue.keys():
            o = issue['offset']
            note = get_note_at_offset(part, o)
            note.addLyric(msg)
        if "offsets" in issue.keys():
            os = issue['offsets']
            n1 = get_note_at_offset(part, os[0])
            n2 = get_note_at_offset(part, os[1])
            bracket = music21.spanner.Line(n1, n2, endHeight=end_height)
            end_height += 1
            part.insert(os[0], bracket)
            n1.addLyric(msg)
    return stream, end_height