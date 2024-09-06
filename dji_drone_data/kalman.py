from filterpy.kalman import KalmanFilter
import numpy as np
from dji_drone_data.utils import haversine


class DroneKalmanFilter:
    """Applies Kalman filter to GPS data and estimates velocity and direction."""

    def __init__(self):
        """Initializes the Kalman filter for GPS tracking."""
        self.kf = KalmanFilter(dim_x=4, dim_z=2)
        self.kf.F = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]])
        self.kf.H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
        self.kf.P *= 1000
        self.kf.Q = np.eye(4) * 0.1
        self.kf.R = np.eye(2) * 0.1

    def calculate_velocity_and_direction(self, parsed_data):
        """Calculates velocity and direction based on parsed GPS data.

        Args:
            parsed_data (list): A list of parsed GPS data.

        Returns:
            list: A list of dictionaries with velocity, direction, filtered GPS data, and time delta.
        """
        velocities = []
        for i in range(1, len(parsed_data)):
            prev_data = parsed_data[i - 1]
            current_data = parsed_data[i]

            dt = (current_data["timestamp"] - prev_data["timestamp"]).total_seconds()
            prev_lat, prev_lon = prev_data["latitude"], prev_data["longitude"]
            curr_lat, curr_lon = current_data["latitude"], current_data["longitude"]

            distance = haversine(prev_lat, prev_lon, curr_lat, curr_lon)
            velocity = distance / dt
            direction = np.degrees(np.arctan2(curr_lon - prev_lon, curr_lat - prev_lat))

            self.kf.predict()
            self.kf.update(np.array([curr_lat, curr_lon]))

            velocities.append(
                {
                    "timestamp": current_data["timestamp"],
                    "velocity": velocity,
                    "direction": direction,
                    "filtered_latitude": self.kf.x[0],
                    "filtered_longitude": self.kf.x[1],
                    "time_delta": dt,  # Add time_delta to the returned dictionary
                }
            )

        return velocities
