from typing import List, Dict, Any
import numpy as np
from filterpy.kalman import KalmanFilter


class DJIDroneDataAnalyzer:
    """Analyzes parsed DJI drone data."""

    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
        self.kf = self._initialize_kalman_filter()

    def _initialize_kalman_filter(self) -> KalmanFilter:
        """Initialize the Kalman filter for position estimation."""
        kf = KalmanFilter(dim_x=2, dim_z=2)
        kf.x = np.array(
            [self.data[0]["latitude"], self.data[0]["longitude"]]
        )  # initial state
        kf.F = np.eye(2)  # state transition matrix
        kf.H = np.eye(2)  # measurement function
        kf.P *= 1000.0  # initial uncertainty
        kf.R = np.eye(2) * 1e-6  # measurement uncertainty
        return kf

    def smooth_trajectory(self) -> List[Dict[str, float]]:
        """
        Apply Kalman filter to smooth the drone's trajectory.

        Returns:
            List[Dict[str, float]]: Smoothed latitude and longitude coordinates.
        """
        smoothed_coords = []
        for i, entry in enumerate(self.data):
            if i > 0:
                dt = (
                    entry["timestamp"] - self.data[i - 1]["timestamp"]
                ).total_seconds()
                self.kf.F = np.array([[1, 0], [0, 1]])
                self.kf.Q = np.eye(2) * dt * 1e-4  # process noise

            z = np.array([entry["latitude"], entry["longitude"]])
            self.kf.predict()
            self.kf.update(z)

            smoothed_coords.append(
                {
                    "latitude": float(self.kf.x[0]),
                    "longitude": float(self.kf.x[1]),
                }
            )
        return smoothed_coords

    def calculate_total_distance(self) -> float:
        """
        Calculate the total distance traveled by the drone.

        Returns:
            float: Total distance in meters.
        """
        total_distance = 0
        for i in range(1, len(self.data)):
            lat1, lon1 = self.data[i - 1]["latitude"], self.data[i - 1]["longitude"]
            lat2, lon2 = self.data[i]["latitude"], self.data[i]["longitude"]
            total_distance += self.haversine(lat1, lon1, lat2, lon2)
        return total_distance

    @staticmethod
    def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Compute the great-circle distance between two points on Earth.

        Args:
            lat1 (float): Latitude of the first point.
            lon1 (float): Longitude of the first point.
            lat2 (float): Latitude of the second point.
            lon2 (float): Longitude of the second point.

        Returns:
            float: Distance in meters.
        """
        R = 6371  # Earth radius in kilometers
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        a = (
            np.sin(dlat / 2) ** 2
            + np.cos(np.radians(lat1))
            * np.cos(np.radians(lat2))
            * np.sin(dlon / 2) ** 2
        )
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        return R * c * 1000  # Distance in meters
