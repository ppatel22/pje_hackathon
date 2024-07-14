from djitellopy import Tello
import cv2
from pynput import keyboard
import threading
import time
import csv


class TelloController:
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.tello.streamon()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 50

        self.send_rc_control = False
        self.should_stop = False

        # Video recording setup
        self.frame_width = 960
        self.frame_height = 720
        self.video_writer = cv2.VideoWriter(
            "tello_recording.mp4",
            cv2.VideoWriter_fourcc(*"mp4v"),
            30,
            (self.frame_width, self.frame_height),
        )

        # Position tracking
        self.start_time = time.time()
        self.x, self.y, self.z = 0, 0, 0
        self.yaw = 0

        # CSV logging setup
        self.csv_file = open("tello_position_log.csv", "w", newline="")
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["Time", "X", "Y", "Z", "Yaw"])

    def run(self):
        # Start the keyboard listener in a separate thread
        keyboard_thread = threading.Thread(target=self.keyboard_listener)
        keyboard_thread.start()

        # Main loop for video feed, recording, and position logging
        while not self.should_stop:
            frame = self.tello.get_frame_read().frame

            # Save the raw frame without any overlay
            self.video_writer.write(frame)

            # Add overlay for display purposes only
            display_frame = frame.copy()
            battery = self.tello.get_battery()
            height = self.tello.get_height()
            cv2.putText(
                display_frame,
                f"Battery: {battery}%",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
            cv2.putText(
                display_frame,
                f"Height: {height}cm",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
            cv2.putText(
                display_frame,
                f"X: {self.x:.2f} Y: {self.y:.2f} Z: {self.z:.2f}",
                (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )

            cv2.imshow("Tello Video Stream", display_frame)

            # Update position and log to CSV
            self.update_position()
            self.log_position()

            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.should_stop = True

            self.update()

        self.tello.land()
        self.tello.streamoff()
        self.video_writer.release()
        self.csv_file.close()
        cv2.destroyAllWindows()

    def keyboard_listener(self):
        with keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        ) as listener:
            listener.join()

    def on_press(self, key):
        try:
            if key.char == "w":
                self.up_down_velocity = self.speed
            elif key.char == "s":
                self.up_down_velocity = -self.speed
            elif key.char == "a":
                self.yaw_velocity = -self.speed
            elif key.char == "d":
                self.yaw_velocity = self.speed
            elif key.char == "t":
                self.tello.takeoff()
                self.send_rc_control = True
            elif key.char == "l":
                self.tello.land()
                self.send_rc_control = False
        except AttributeError:
            if key == keyboard.Key.up:
                self.for_back_velocity = self.speed
            elif key == keyboard.Key.down:
                self.for_back_velocity = -self.speed
            elif key == keyboard.Key.left:
                self.left_right_velocity = -self.speed
            elif key == keyboard.Key.right:
                self.left_right_velocity = self.speed
            elif key == keyboard.Key.esc:
                self.should_stop = True
                return False

    def on_release(self, key):
        try:
            if key.char in ["w", "s"]:
                self.up_down_velocity = 0
            elif key.char in ["a", "d"]:
                self.yaw_velocity = 0
        except AttributeError:
            if key in [keyboard.Key.up, keyboard.Key.down]:
                self.for_back_velocity = 0
            elif key in [keyboard.Key.left, keyboard.Key.right]:
                self.left_right_velocity = 0

    def update(self):
        if self.send_rc_control:
            self.tello.send_rc_control(
                self.left_right_velocity,
                self.for_back_velocity,
                self.up_down_velocity,
                self.yaw_velocity,
            )

    def update_position(self):
        # Calculate time elapsed since last update
        current_time = time.time()
        dt = current_time - self.start_time
        self.start_time = current_time

        # Update yaw (rotation around z-axis)
        self.yaw += self.yaw_velocity * dt

        # Calculate displacement in drone's local coordinate system
        dx = self.for_back_velocity * dt
        dy = self.left_right_velocity * dt
        dz = self.up_down_velocity * dt

        # Convert to global coordinate system
        import math

        self.x += dx * math.cos(math.radians(self.yaw)) - dy * math.sin(
            math.radians(self.yaw)
        )
        self.y += dx * math.sin(math.radians(self.yaw)) + dy * math.cos(
            math.radians(self.yaw)
        )
        self.z += dz

    def log_position(self):
        self.csv_writer.writerow(
            [time.time() - self.start_time, self.x, self.y, self.z, self.yaw]
        )


if __name__ == "__main__":
    controller = TelloController()
    controller.run()

# go_xyz_speed(x, y, z, speed)
# curve_xyz_speed(x1, y1, z1, x2, y2, z2, speed)