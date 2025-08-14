# This script is intended to be run on an NVIDIA Jetson Nano.
# It requires the Jetson.GPIO library to be installed.
# To install: pip install Jetson.GPIO

import Jetson.GPIO as GPIO
import time

# --- Configuration ---
# Use the physical pin number on the Jetson Nano board.
# You would connect your relay's signal wire to this pin.
SPRAYER_PIN = 12  # Example: Pin 12

# --- Functions ---

def setup_gpio():
    """
    Initializes the GPIO pins. This should be called once when the main
    inference script starts.
    """
    # Use the physical pin numbering scheme (BCM is the other option)
    GPIO.setmode(GPIO.BOARD)
    
    # Set up the sprayer pin as an output pin and initialize it to LOW (off)
    GPIO.setup(SPRAYER_PIN, GPIO.OUT, initial=GPIO.LOW)
    print(f"GPIO setup complete. Sprayer on pin {SPRAYER_PIN} is ready.")

def activate_sprayer(duration=0.5):
    """
    Activates the sprayer for a specified duration.
    
    Args:
        duration (float): The number of seconds to keep the sprayer on.
    """
    print(f"-> Activating sprayer for {duration} seconds...")
    
    # Send a HIGH signal to the pin to turn the relay ON
    GPIO.output(SPRAYER_PIN, GPIO.HIGH)
    
    # Keep the sprayer on for the specified duration
    time.sleep(duration)
    
    # Send a LOW signal to the pin to turn the relay OFF
    GPIO.output(SPRAYER_PIN, GPIO.LOW)
    
    print("-> Sprayer deactivated.")

def cleanup_gpio():
    """
    Resets all GPIO pins to their default state. This should be called
    when the program exits to ensure no pins are left active.
    """
    GPIO.cleanup()
    print("GPIO cleanup complete. All pins reset.")

# --- Example Usage (for testing purposes) ---
if __name__ == '__main__':
    try:
        # This is how you would use the functions in your main script
        setup_gpio()
        
        print("\n--- Running a test spray ---")
        # Simulate detecting a weed
        activate_sprayer(1) # Test by spraying for 1 second
        
        time.sleep(2)
        
        print("\nTest complete.")

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        # Always run cleanup to reset the pins
        cleanup_gpio()