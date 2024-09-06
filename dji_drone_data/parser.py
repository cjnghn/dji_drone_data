import re
import datetime
from typing import List, Dict, Any


class DJIDroneDataParser:
    """Parses SRT data and extracts GPS, timestamp, and other metadata."""

    def __init__(self):
        self.srt_pattern = re.compile(
            r"(\d+)\n"
            r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n"
            r'<font size="28">SrtCnt : (\d+), DiffTime : (\d+)ms\n'
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\n"
            r"\[iso : (\d+)\] "
            r"\[shutter : ([\d/\.]+)\] "
            r"\[fnum : (\d+)\] "
            r"\[ev : ([-]?\d+)\] "
            r"\[ct : (\d+)\] "
            r"\[color_md : (\w+)\] "
            r"\[focal_len : (\d+)\] "
            r"\[dzoom_ratio: (\d+), delta:(\d+)\],"
            r"\[latitude: ([\d\.]+)\] "
            r"\[longitude: ([\d\.]+)\] "
            r"\[rel_alt: ([\d\.]+) abs_alt: ([\d\.]+)\]"
        )

    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse the SRT file and extract relevant data.

        Args:
            file_path (str): Path to the SRT file.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing parsed data.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            srt_content = file.read()
        return self.parse(srt_content)

    def parse(self, srt_content: str) -> List[Dict[str, Any]]:
        """
        Parse the SRT content and extract relevant data.

        Args:
            srt_content (str): The SRT file content as a string.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing parsed data.
        """
        parsed_data = []
        for match in self.srt_pattern.finditer(srt_content):
            entry = self._create_entry_from_match(match)
            parsed_data.append(entry)
        return parsed_data

    def _create_entry_from_match(self, match: re.Match) -> Dict[str, Any]:
        """
        Create a dictionary entry from a regex match object.

        Args:
            match (re.Match): A regex match object containing SRT data.

        Returns:
            Dict[str, Any]: A dictionary containing parsed data from the match.
        """
        return {
            "subtitle_number": int(match.group(1)),
            "start_time": self._parse_time(match.group(2)),
            "end_time": self._parse_time(match.group(3)),
            "srt_cnt": int(match.group(4)),
            "diff_time": int(match.group(5)),
            "timestamp": datetime.datetime.strptime(
                match.group(6), "%Y-%m-%d %H:%M:%S.%f"
            ),
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

    @staticmethod
    def _parse_time(time_str: str) -> datetime.timedelta:
        """
        Parse a time string into a timedelta object.

        Args:
            time_str (str): A time string in the format "HH:MM:SS,mmm".

        Returns:
            datetime.timedelta: A timedelta object representing the parsed time.
        """
        h, m, s = time_str.replace(",", ".").split(":")
        return datetime.timedelta(hours=int(h), minutes=int(m), seconds=float(s))
