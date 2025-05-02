import RPi.GPIO as GPIO
import time

# Step 1: Configuration
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO_PIN = 18           # Example GPIO pin
THRESHOLD = 5           # Example threshold count for some logic
event_counter = 0       # Global variable to count events

# Step 2: Define ISR (Interrupt Service Routine)
def gpio_isr(channel):
    global event_counter
    print(f"[ISR] Interrupt received on GPIO {channel}")
    event_counter += 1

    # Step 3: Threshold check
    if event_counter >= THRESHOLD:
        print(f"[ACTION] Threshold reached: {event_counter}")
        # Trigger some action here
        event_counter = 0  # Reset if needed

# Step 4: Setup GPIO and attach interrupt
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(GPIO_PIN, GPIO.FALLING, callback=gpio_isr, bouncetime=200)

# Step 5: Main loop
try:
    print("Monitoring GPIO interrupts. Press Ctrl+C to exit.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting program...")

# Step 6: Cleanup
finally:
    GPIO.cleanup()
    print("GPIO cleanup completed.")
