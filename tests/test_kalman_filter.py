import unittest
from dji_drone_data.kalman import DroneKalmanFilter
from dji_drone_data.parser import SRTParser


class TestDroneKalmanFilter(unittest.TestCase):

    def setUp(self):
        """Set up sample SRT content and Kalman filter for testing."""
        self.srt_content = """1
00:00:00,000 --> 00:00:00,033
<font size="28">SrtCnt : 1, DiffTime : 33ms
2024-09-04 13:29:07.288
[iso : 120] [shutter : 1/2000.0] [fnum : 170] [ev : 0] [ct : 5165] [color_md : default] [focal_len : 240] [dzoom_ratio: 10000, delta:0],[latitude: 37.451022] [longitude: 126.656545] [rel_alt: 45.000 abs_alt: 111.890] </font>

2
00:00:00,033 --> 00:00:00,066
<font size="28">SrtCnt : 2, DiffTime : 33ms
2024-09-04 13:29:07.324
[iso : 120] [shutter : 1/2000.0] [fnum : 170] [ev : 0] [ct : 5164] [color_md : default] [focal_len : 240] [dzoom_ratio: 10000, delta:0],[latitude: 37.451032] [longitude: 126.656555] [rel_alt: 45.100 abs_alt: 111.990] </font>

3
00:00:00,066 --> 00:00:00,099
<font size="28">SrtCnt : 3, DiffTime : 33ms
2024-09-04 13:29:07.360
[iso : 120] [shutter : 1/2000.0] [fnum : 170] [ev : 0] [ct : 5163] [color_md : default] [focal_len : 240] [dzoom_ratio: 10000, delta:0],[latitude: 37.451042] [longitude: 126.656565] [rel_alt: 45.200 abs_alt: 112.090] </font>
"""
        self.parser = SRTParser()
        self.parsed_data = self.parser.parse(self.srt_content)
        self.kalman_filter = DroneKalmanFilter()

    def test_velocity_direction_calculation(self):
        """Test if velocity and direction are calculated correctly."""
        velocity_data = self.kalman_filter.calculate_velocity_and_direction(
            self.parsed_data
        )

        # Test the number of calculated velocity entries
        self.assertEqual(len(velocity_data), 2)  # Should be 2 for 3 data points

        # Verify the structure of velocity data
        for entry in velocity_data:
            self.assertIn("velocity", entry)
            self.assertIn("direction", entry)
            self.assertIn("filtered_latitude", entry)
            self.assertIn("filtered_longitude", entry)
            self.assertIn("time_delta", entry)

        # Check if velocity and direction are reasonable (non-zero in this case)
        self.assertGreater(velocity_data[0]["velocity"], 0)
        self.assertIsNotNone(velocity_data[0]["direction"])

    def test_kalman_filter_smoothing(self):
        """Test if Kalman filter is smoothing the data."""
        velocity_data = self.kalman_filter.calculate_velocity_and_direction(
            self.parsed_data
        )

        # Check if filtered coordinates are different from raw coordinates
        for i, entry in enumerate(velocity_data):
            raw_lat = self.parsed_data[i + 1][
                "latitude"
            ]  # i+1 because velocity is calculated from the second point
            raw_lon = self.parsed_data[i + 1]["longitude"]
            self.assertNotEqual(entry["filtered_latitude"], raw_lat)
            self.assertNotEqual(entry["filtered_longitude"], raw_lon)

    def test_time_delta_calculation(self):
        """Test if time delta between measurements is calculated correctly."""
        velocity_data = self.kalman_filter.calculate_velocity_and_direction(
            self.parsed_data
        )

        expected_time_delta = 0.036  # 36ms between each measurement
        for entry in velocity_data:
            self.assertAlmostEqual(entry["time_delta"], expected_time_delta, places=3)

    def test_empty_data(self):
        """Test behavior with empty data."""
        empty_data = []
        velocity_data = self.kalman_filter.calculate_velocity_and_direction(empty_data)
        self.assertEqual(len(velocity_data), 0)

    def test_single_data_point(self):
        """Test behavior with a single data point."""
        single_data = [self.parsed_data[0]]
        velocity_data = self.kalman_filter.calculate_velocity_and_direction(single_data)
        self.assertEqual(len(velocity_data), 0)


if __name__ == "__main__":
    unittest.main()
