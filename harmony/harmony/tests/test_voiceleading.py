from harmony_checker.voiceleading import *

e1 = music21.converter.parse("harmony/tests/examples/Example_1.mxl")
e1_chordified = e1.chordify()
e1_chordified.write("musicxml", "harmony/tests/examples/example1_chordified.xml")


e2 = music21.converter.parse("harmony/tests/examples/Example_2.mxl")
e2_chordified = e2.chordify()
e2_chordified.write("musicxml", "harmony/tests/examples/example2_chordified.xml")


def test_get_num_parts_1():
    assert not get_num_parts(e1, chordified_stream=e1_chordified)


def test_get_num_parts_2():
    result = get_num_parts(e2, chordified_stream=e2_chordified)
    assert result == [{"offset": 0, "msg": "Wrong # of parts", "part": "T."}]


def test_get_num_notes_1():
    assert not get_num_notes(e1, chordified_stream=e1_chordified)


def test_get_num_notes_2():
    result = get_num_notes(e2, chordified_stream=e2_chordified)
    rest = {"offset": 14, "part": "T.", "msg": "Missing Note"}
    chord = {"offset": 14, "part": "S.", "msg": "Extra Note(s)"}
    assert len(result) == 2 and rest in result and chord in result


def test_get_parts_out_of_range_1():
    assert not get_parts_out_of_range(e1, chordified_stream=e1_chordified)


def test_get_parts_out_of_range_2():
    result = get_parts_out_of_range(e2, chordified_stream=e2_chordified)
    s = {"offset": 14, "part": "S.", "msg": "Part out of Range"}
    a1 = {"offset": 12, "part": "A.", "msg": "Part out of Range"}
    a2 = {"offset": 14, "part": "A.", "msg": "Part out of Range"}
    t = {"offset": 0, "part": "T.", "msg": "Part out of Range"}
    assert (
        len(result) == 4
        and s in result
        and a1 in result
        and a2 in result
        and t in result
    )


def test_get_doubled_leading_tones_1():
    assert not get_doubled_leading_tones(e1, chordified_stream=e1_chordified)


def test_get_doubled_leading_tones_2():
    result = get_doubled_leading_tones(e2, chordified_stream=e2_chordified)
    sop = {"offset": 4, "part": "S.", "msg": "Doubled Leading Tone"}
    alto = {"offset": 4, "part": "A.", "msg": "Doubled Leading Tone"}
    assert len(result) == 2 and sop in result and alto in result


def test_get_omitted_thirds_1():
    assert not get_omitted_thirds(e1, chordified_stream=e1_chordified)


def test_get_omitted_thirds_2():
    result = get_omitted_thirds(e2, chordified_stream=e2_chordified)
    c1 = {"offset": 0, "part": "T.", "msg": "Omitted Third"}
    c2 = {"offset": 2, "part": "T.", "msg": "Omitted Third"}
    c3 = {"offset": 4, "part": "T.", "msg": "Omitted Third"}
    c4 = {"offset": 10, "part": "T.", "msg": "Omitted Third"}
    assert (
        len(result) == 4
        and c1 in result
        and c2 in result
        and c3 in result
        and c4 in result
    )


def test_adj_voice_spacing_1():
    assert not get_overspacing(e1, chordified_stream=e1_chordified)


def test_adj_voice_spacing_2():
    result = get_overspacing(e2, chordified_stream=e2_chordified)
    s = {"offset": 0, "part": "S.", "msg": "Overspaced Chord"}
    a = {"offset": 0, "part": "A.", "msg": "Overspaced Chord"}
    t = {"offset": 0, "part": "T.", "msg": "Overspaced Chord"}
    assert len(result) == 3 and s in result and a in result and t in result


def test_get_melodic_aug_2_1():
    assert not get_melodic_aug_2(e1, chordified_stream=e1_chordified)


def test_get_melodic_aug_2_2():
    result = get_melodic_aug_2(e2, chordified_stream=e2_chordified)
    s = {"offsets": (2, 4), "part": "S.", "msg": "Aug 2 ->"}
    a = {"offsets": (2, 4), "part": "A.", "msg": "Aug 2 ->"}
    assert len(result) == 2 and s in result and a in result


def test_get_parallel_fifths_1():
    assert not get_parallel_fifths(e1, chordified_stream=e1_chordified)


def test_get_parallel_fifths_2():
    result = get_parallel_fifths(e2, chordified_stream=e2_chordified)
    s = {"offsets": (8, 10), "part": "S.", "msg": "Parallel 5ths ->"}
    a = {"offsets": (8, 10), "part": "A.", "msg": "Parallel 5ths ->"}
    assert len(result) == 2 and s in result and a in result


def test_get_parallel_octaves_1():
    assert not get_parallel_octaves(e1, chordified_stream=e1_chordified)


def test_get_parallel_octaves_2():
    result = get_parallel_octaves(e2, chordified_stream=e2_chordified)
    s = {"offsets": (2, 4), "part": "S.", "msg": "Parallel 8ves ->"}
    a = {"offsets": (2, 4), "part": "A.", "msg": "Parallel 8ves ->"}
    assert len(result) == 2 and s in result and a in result


def test_get_d5_to_p5_1():
    assert not get_d5_to_p5(e1, chordified_stream=e1_chordified)


def test_get_d5_to_p5_2():
    result = get_d5_to_p5(e2, chordified_stream=e2_chordified)
    s = {"offsets": (6, 8), "part": "S.", "msg": "D5 to P5 ->"}
    a = {"offsets": (6, 8), "part": "A.", "msg": "D5 to P5 ->"}
    assert len(result) == 2 and s in result and a in result


def test_get_hidden_fifths_1():
    assert not get_hidden_fifths(e1, chordified_stream=e1_chordified)


def test_get_hidden_fifths_2():
    result = get_hidden_fifths(e2, chordified_stream=e2_chordified)
    t = {"offsets": (8, 10), "part": "T.", "msg": "Hidden 5ths ->"}
    a = {"offsets": (8, 10), "part": "A.", "msg": "Hidden 5ths ->"}
    assert len(result) == 2 and t in result and a in result


def test_get_hidden_octaves_1():
    assert not get_hidden_octaves(e1, chordified_stream=e1_chordified)


def test_get_hidden_octaves_2():
    result = get_hidden_octaves(e2, chordified_stream=e2_chordified)
    t = {"offsets": (10, 12), "part": "T.", "msg": "Hidden 8ves ->"}
    a = {"offsets": (10, 12), "part": "A.", "msg": "Hidden 8ves ->"}
    assert len(result) == 2 and t in result and a in result


def test_get_crossed_voices_1():
    assert not get_crossed_voices(e1, chordified_stream=e1_chordified)


def test_get_crossed_voices_2():
    result = get_crossed_voices(e2, chordified_stream=e2_chordified)
    s = {"offsets": (10, 12), "part": "S.", "msg": "Crossed Voices ->"}
    a = {"offsets": (10, 12), "part": "A.", "msg": "Crossed Voices ->"}
    assert len(result) == 2 and s in result and a in result


def test_annotate_stream_1():
    issues = [
        {"offset": 0, "part": "B.", "msg": "test1"},
        {"offsets": (4, 6), "part": "A.", "msg": "test2"},
    ]
    annotation, end_height = annotate_stream(issues, e1, 1)
    b = [
        p for p in annotation.getElementsByClass("Part") if p.partAbbreviation == "B."
    ][0]
    a = [
        p for p in annotation.getElementsByClass("Part") if p.partAbbreviation == "A."
    ][0]
    b_lyric = get_note_at_offset(b, 0).lyric
    a_lyric = get_note_at_offset(a, 4).lyric
    assert (
        end_height == 3
        and len(a.spanners) == 1
        and a.spanners[0].getOffsetBySite(a) == 4
        and b_lyric == "test1"
        and a_lyric == "test2"
    )
