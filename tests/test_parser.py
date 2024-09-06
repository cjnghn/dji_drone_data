import unittest
from datetime import datetime, timedelta
from dji_drone_data.parser import DJIDroneDataParser


class TestDJIDroneDataParser(unittest.TestCase):
    def setUp(self):
        # Set up the SRT data for testing
        self.srt_data = """1
00:00:00,000 --> 00:00:00,033
<font size="28">SrtCnt : 1, DiffTime : 33ms
2024-09-04 13:29:07.288
[iso : 120] [shutter : 1/2000.0] [fnum : 170] [ev : 0] [ct : 5165] [color_md : default] [focal_len : 240] [dzoom_ratio: 10000, delta:0],[latitude: 37.451022] [longitude: 126.656545] [rel_alt: 45.000 abs_alt: 111.890] </font>

2
00:00:00,033 --> 00:00:00,066
<font size="28">SrtCnt : 2, DiffTime : 33ms
2024-09-04 13:29:07.324
[iso : 120] [shutter : 1/2000.0] [fnum : 170] [ev : 0] [ct : 5164] [color_md : default] [focal_len : 240] [dzoom_ratio: 10000, delta:0],[latitude: 37.451022] [longitude: 126.656545] [rel_alt: 45.000 abs_alt: 111.890] </font>

3
00:00:00,066 --> 00:00:00,100
<font size="28">SrtCnt : 3, DiffTime : 34ms
2024-09-04 13:29:07.354
[iso : 120] [shutter : 1/2000.0] [fnum : 170] [ev : 0] [ct : 5164] [color_md : default] [focal_len : 240] [dzoom_ratio: 10000, delta:0],[latitude: 37.451022] [longitude: 126.656545] [rel_alt: 45.000 abs_alt: 111.890] </font>

4
00:00:00,100 --> 00:00:00,133
<font size="28">SrtCnt : 4, DiffTime : 33ms
2024-09-04 13:29:07.388
[iso : 120] [shutter : 1/2000.0] [fnum : 170] [ev : 0] [ct : 5163] [color_md : default] [focal_len : 240] [dzoom_ratio: 10000, delta:0],[latitude: 37.451022] [longitude: 126.656545] [rel_alt: 45.000 abs_alt: 111.890] </font>
        """
        self.parser = DJIDroneDataParser()

    def test_parse_srt_data(self):
        # Parse the SRT data
        result = self.parser.parse(self.srt_data)

        # Expected results for the first parsed entry
        expected_first_entry = {
            "subtitle_number": 1,
            "start_time": timedelta(hours=0, minutes=0, seconds=0),
            "end_time": timedelta(hours=0, minutes=0, seconds=0.033),
            "srt_cnt": 1,
            "diff_time": 33,
            "timestamp": datetime(2024, 9, 4, 13, 29, 7, 288000),
            "iso": 120,
            "shutter": "1/2000.0",
            "fnum": 170,
            "ev": 0,
            "ct": 5165,
            "color_md": "default",
            "focal_len": 240,
            "dzoom_ratio": 10000,
            "dzoom_delta": 0,
            "latitude": 37.451022,
            "longitude": 126.656545,
            "rel_altitude": 45.0,
            "abs_altitude": 111.89,
        }

        # Check if the first parsed entry matches the expected result
        self.assertEqual(result[0], expected_first_entry)

        # Check the number of parsed entries
        self.assertEqual(len(result), 4)

        # Check that the last entry has correct subtitle number
        self.assertEqual(result[-1]["subtitle_number"], 4)


if __name__ == "__main__":
    unittest.main()
