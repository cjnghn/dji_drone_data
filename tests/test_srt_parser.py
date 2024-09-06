import unittest
from datetime import datetime, timedelta
from dji_drone_data.parser import SRTParser


class TestSRTParser(unittest.TestCase):

    def setUp(self):
        """Set up sample SRT content for testing."""
        self.srt_content = """1
00:00:00,000 --> 00:00:00,033
<font size="28">SrtCnt : 1, DiffTime : 33ms
2024-09-04 13:29:07.288
[iso : 120] [shutter : 1/2000.0] [fnum : 170] [ev : 0] [ct : 5165] [color_md : default] [focal_len : 240] [dzoom_ratio: 10000, delta:0],[latitude: 37.451022] [longitude: 126.656545] [rel_alt: 45.000 abs_alt: 111.890] </font>

2
00:00:00,033 --> 00:00:00,066
<font size="28">SrtCnt : 2, DiffTime : 33ms
2024-09-04 13:29:07.324
[iso : 120] [shutter : 1/2000.0] [fnum : 170] [ev : 0] [ct : 5164] [color_md : default] [focal_len : 240] [dzoom_ratio: 10000, delta:0],[latitude: 37.451022] [longitude: 126.656545] [rel_alt: 45.000 abs_alt: 111.890] </font>
"""
        self.parser = SRTParser()

    def test_parse_srt(self):
        """Test if the SRT data is parsed correctly."""
        parsed_data = self.parser.parse(self.srt_content)

        # Check the length of parsed data
        self.assertEqual(len(parsed_data), 2)

        # Verify the content of the first entry
        first_entry = parsed_data[0]
        self.assertEqual(first_entry["subtitle_number"], 1)
        self.assertEqual(first_entry["start_time"], timedelta(0))
        self.assertEqual(first_entry["end_time"], timedelta(milliseconds=33))
        self.assertEqual(first_entry["srt_cnt"], 1)
        self.assertEqual(first_entry["diff_time"], "33ms")
        self.assertEqual(
            first_entry["timestamp"], datetime(2024, 9, 4, 13, 29, 7, 288000)
        )
        self.assertEqual(first_entry["iso"], 120)
        self.assertEqual(first_entry["shutter"], "1/2000.0")
        self.assertEqual(first_entry["fnum"], 170)
        self.assertEqual(first_entry["ev"], 0)
        self.assertEqual(first_entry["ct"], 5165)
        self.assertEqual(first_entry["color_md"], "default")
        self.assertEqual(first_entry["focal_len"], 240)
        self.assertEqual(first_entry["dzoom_ratio"], 10000)
        self.assertEqual(first_entry["dzoom_delta"], 0)
        self.assertEqual(first_entry["latitude"], 37.451022)
        self.assertEqual(first_entry["longitude"], 126.656545)
        self.assertEqual(first_entry["rel_altitude"], 45.000)
        self.assertEqual(first_entry["abs_altitude"], 111.890)

    def test_parse_time(self):
        """Test the parse_time method."""
        time_str = "00:01:23,456"
        expected_timedelta = timedelta(minutes=1, seconds=23, milliseconds=456)
        self.assertEqual(self.parser.parse_time(time_str), expected_timedelta)

    def test_empty_content(self):
        """Test parsing empty content."""
        empty_content = ""
        parsed_data = self.parser.parse(empty_content)
        self.assertEqual(len(parsed_data), 0)

    def test_invalid_content(self):
        """Test parsing invalid content."""
        invalid_content = "This is not a valid SRT content"
        parsed_data = self.parser.parse(invalid_content)
        self.assertEqual(len(parsed_data), 0)


if __name__ == "__main__":
    unittest.main()
