import unittest

from transcribe import Segment, deduplicate_rolling_captions, join_transcript_text


class RollingCaptionCleanupTests(unittest.TestCase):
    def test_removes_incremental_overlap(self):
        source = [
            Segment(0.00, 1.00, "Это важная фраза"),
            Segment(1.00, 2.00, "важная фраза продолжается"),
            Segment(2.00, 3.00, "продолжается дальше."),
        ]
        cleaned, stats = deduplicate_rolling_captions(source)
        self.assertEqual(join_transcript_text(cleaned), "Это важная фраза продолжается дальше.")
        self.assertEqual(stats["removed_words"], 4)

    def test_removes_single_word_overlap(self):
        source = [
            Segment(0.00, 1.00, "Мы пришли домой"),
            Segment(1.00, 2.00, "домой поздно."),
        ]
        cleaned, _ = deduplicate_rolling_captions(source)
        self.assertEqual(join_transcript_text(cleaned), "Мы пришли домой поздно.")

    def test_keeps_real_repetition_inside_a_cue(self):
        source = [Segment(0.00, 1.00, "Это очень, очень важно.")]
        cleaned, _ = deduplicate_rolling_captions(source)
        self.assertEqual(join_transcript_text(cleaned), "Это очень, очень важно.")

    def test_does_not_remove_repetition_after_a_pause(self):
        source = [
            Segment(0.00, 1.00, "Он сказал да"),
            Segment(2.00, 3.00, "да, конечно."),
        ]
        cleaned, _ = deduplicate_rolling_captions(source)
        self.assertEqual(join_transcript_text(cleaned), "Он сказал да да, конечно.")

    def test_drops_fully_repeated_cue(self):
        source = [
            Segment(0.00, 1.00, "Повторяющаяся фраза"),
            Segment(1.00, 2.00, "Повторяющаяся фраза"),
        ]
        cleaned, stats = deduplicate_rolling_captions(source)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(stats["removed_entries"], 1)


if __name__ == "__main__":
    unittest.main()
