import machine
import time

# Define the trig and echo pins
TRIG_PIN = 3
ECHO_PIN = 2

# Configure the trig and echo pins
trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)

# Flag to control the measurement
measure_active = True

def trigger_object_detection():
    global measure_active
    with open("trigger.txt", "w") as f:
        f.write("Triggered")
    print("Starting object detection.")
    measure_active = False  # Stop further measurements

# Function to measure the distance using the ultrasonic sensor
def get_distance():
    # Trigger the ultrasonic sensor
    trig.value(0)
    time.sleep_us(2)  # Wait for 2 microseconds
    trig.value(1)
    time.sleep_us(10)  # Send a 10-microsecond pulse
    trig.value(0)

    # Measure the time for the echo pin to go high and low
    while echo.value() == 0:
        pulse_start = time.ticks_us()
    while echo.value() == 1:
        pulse_end = time.ticks_us()

    # Calculate the pulse duration
    pulse_duration = pulse_end - pulse_start

    # Convert the pulse duration to distance (in centimeters)
    distance = (pulse_duration * 0.0343) / 2

    return distance

# Main loop
try:
    threshold_distance = 100.0  # 1 meter in centimeters
    threshold_time = 2  # 2 seconds
    start_time = None

    while measure_active:
        distance = get_distance()
        print("Distance: {:.2f} cm".format(distance))

        # Check if the distance is within the threshold
        if distance <= threshold_distance:
            if start_time is None:
                start_time = time.time()
            elif time.time() - start_time >= threshold_time:
                trigger_object_detection()
                break  # Exit the loop after triggering
        else:
            start_time = None  # Reset the timer if the condition is not met

        time.sleep(0.1)  # 0.1 second delay

except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    print("\nMeasurement stopped by user")
