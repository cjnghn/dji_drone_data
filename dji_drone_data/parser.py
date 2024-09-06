import re
import datetime


class SRTParser:
    """Parses SRT data and extracts GPS, timestamp, and other metadata."""

    def __init__(self):
        # Define regular expression pattern matching the structure of each SRT entry
        self.srt_pattern = re.compile(
            r"(\d+)\n"  # Subtitle number
            r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n"  # Time range
            r'<font size="28">SrtCnt : (\d+), DiffTime : (\d+)ms\n'  # SrtCnt and DiffTime
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\n"  # Timestamp
            r"\[iso : (\d+)\] "  # ISO
            r"\[shutter : ([\d/\.]+)\] "  # Shutter speed
            r"\[fnum : (\d+)\] "  # F-number
            r"\[ev : ([-]?\d+)\] "  # EV
            r"\[ct : (\d+)\] "  # CT
            r"\[color_md : (\w+)\] "  # Color mode
            r"\[focal_len : (\d+)\] "  # Focal length
            r"\[dzoom_ratio: (\d+), delta:(\d+)\],"  # Zoom ratio
            r"\[latitude: ([\d\.]+)\] "  # Latitude
            r"\[longitude: ([\d\.]+)\] "  # Longitude
            r"\[rel_alt: ([\d\.]+) abs_alt: ([\d\.]+)\]"  # Relative and absolute altitude
        )

    def parse_time(self, time_str):
        """Parses SRT time string and converts it to datetime.timedelta object.

        Args:
            time_str (str): Time string in SRT format (HH:MM:SS,mmm).

        Returns:
            datetime.timedelta: Parsed time as a timedelta object.
        """
        h, m, s = time_str.replace(",", ".").split(":")
        return datetime.timedelta(hours=int(h), minutes=int(m), seconds=float(s))

    def parse(self, srt_content):
        """Parses the SRT data content.

        Args:
            srt_content (str): The raw SRT content to be parsed.

        Returns:
            list: A list of dictionaries, each containing parsed data for one SRT entry.
        """
        parsed_data = []

        # Use regular expression to match SRT content
        for match in self.srt_pattern.finditer(srt_content):
            # Extract data from matched groups
            subtitle_number = int(match.group(1))
            start_time = self.parse_time(match.group(2))
            end_time = self.parse_time(match.group(3))
            srt_cnt = int(match.group(4))
            diff_time = match.group(5) + "ms"
            timestamp = datetime.datetime.strptime(
                match.group(6), "%Y-%m-%d %H:%M:%S.%f"
            )

            # Create dictionary with extracted data
            entry = {
                "subtitle_number": subtitle_number,
                "start_time": start_time,
                "end_time": end_time,
                "srt_cnt": srt_cnt,
                "diff_time": diff_time,
                "timestamp": timestamp,
                "iso": int(match.group(7)),
                "shutter": match.group(8),
                "fnum": int(match.group(9)),
                "ev": int(match.group(10)),
                "ct": int(match.group(11)),
                "color_md": match.group(12),
                "focal_len": int(match.group(13)),
                "dzoom_ratio": int(match.group(14)),
                "dzoom_delta": int(match.group(15)),
                "latitude": float(match.group(16)),
                "longitude": float(match.group(17)),
                "rel_altitude": float(match.group(18)),
                "abs_altitude": float(match.group(19)),
            }

            # Add parsed data to the list
            parsed_data.append(entry)

        return parsed_data


# Usage example
if __name__ == "__main__":
    srt_content = """1
00:00:00,000 --> 00:00:00,033
<font size="28">SrtCnt : 1, DiffTime : 33ms
2024-09-04 13:29:07.288
[iso : 120] [shutter : 1/2000.0] [fnum : 170] [ev : 0] [ct : 5165] [color_md : default] [focal_len : 240] [dzoom_ratio: 10000, delta:0],[latitude: 37.451022] [longitude: 126.656545] [rel_alt: 45.000 abs_alt: 111.890] 
2
00:00:00,033 --> 00:00:00,066
<font size="28">SrtCnt : 2, DiffTime : 33ms
2024-09-04 13:29:07.324
[iso : 120] [shutter : 1/2000.0] [fnum : 170] [ev : 0] [ct : 5164] [color_md : default] [focal_len : 240] [dzoom_ratio: 10000, delta:0],[latitude: 37.451022] [longitude: 126.656545] [rel_alt: 45.000 abs_alt: 111.890] """

    parser = SRTParser()
    result = parser.parse(srt_content)

    # Print results
    for entry in result:
        print(entry)
