from voiceleading import *
e1 = music21.converter.parse("examples/Example_1.mxl")
e1_chordified = e1.chordify()
e1_chordified.write("musicxml", "examples/example1_chordified.xml")


e2 = music21.converter.parse("examples/Example_2.mxl")
e2_chordified = e2.chordify()
e2_chordified.write("musicxml", "examples/example2_chordified.xml")


def test_get_num_parts_1():
    assert get_num_parts(e1) == 4


def test_get_num_parts_2():
    assert get_num_parts(e2) == 3


def test_get_missing_notes_1():
    assert len(get_missing_notes(e1_chordified)) == 0


def test_get_missing_notes_2():
    assert len(get_missing_notes(e2_chordified)) == 7


def test_get_parts_out_of_range_1():
    assert len(get_parts_out_of_range(e1)) == 0


def test_get_parts_out_of_range_2():
    assert len(get_parts_out_of_range(e2)) == 2


def test_get_doubled_leading_tones_1():
    assert len(get_doubled_leading_tones(e1_chordified)) == 0


def test_get_doubled_leading_tones_2():
    assert len(get_doubled_leading_tones(e2_chordified)) == 1


def test_get_omitted_thirds_1():
    assert len(get_omitted_thirds(e1_chordified)) == 0


def test_get_omitted_thirds_2():
    assert len(get_omitted_thirds(e2_chordified)) == 4


def test_adj_voice_spacing_1():
    assert len(get_overspacing(e1_chordified)) == 0


def test_adj_voice_spacing_2():
    assert len(get_overspacing(e2_chordified)) == 1


def test_get_melodic_aug_2_1():
    assert len(get_melodic_aug_2(e1)) == 0


def test_get_melodic_aug_2_2():
    assert len(get_melodic_aug_2(e2)) == 2


def test_get_parallel_fifths_1():
    assert len(get_parallel_fifths(e1, e1_chordified)) == 0


def test_get_parallel_fifths_2():
    assert len(get_parallel_fifths(e2, e2_chordified)) == 1


def test_get_parallel_octaves_1():
    assert len(get_parallel_octaves(e1, e1_chordified)) == 0


def test_get_parallel_octaves_2():
    assert len(get_parallel_octaves(e2, e2_chordified)) == 1


def test_get_d5_to_p5_1():
    assert len(get_d5_to_p5(e1, e1_chordified)) == 0


def test_get_d5_to_p5_2():
    assert len(get_d5_to_p5(e2, e2_chordified)) == 1


def test_get_hidden_fifths_1():
    assert len(get_hidden_fifths(e1, e1_chordified)) == 0


def test_get_hidden_fifths_2():
    assert len(get_hidden_fifths(e2, e2_chordified)) == 1


def test_get_hidden_octaves_1():
    assert len(get_hidden_octaves(e1, e1_chordified)) == 0


def test_get_hidden_octaves_2():
    assert len(get_hidden_octaves(e2, e2_chordified)) == 1


def test_get_crossed_voices_1():
    assert len(get_crossed_voices(e1, e1_chordified)) == 0


def test_get_crossed_voices_2():
    assert len(get_crossed_voices(e2, e2_chordified)) == 1


