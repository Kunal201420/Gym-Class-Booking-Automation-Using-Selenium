from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import os
import time

# User credentials and URL
ACCOUNT_EMAIL = "kunal@test.com"  # Change to your email
ACCOUNT_PASSWORD = "Kunal$201420"        # Change to your password
GYM_URL = "https://appbrewery.github.io/gym/"

# Setup Chrome with persistent session profile and detached browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=chrome_options)
driver.get(GYM_URL)

# Explicit wait with comfortable timeout
wait = WebDriverWait(driver, 10)  # Increased timeout to 10 seconds

def retry(func, retries=7, description=None):
    """Retry wrapper for resilience to network or loading issues."""
    for attempt in range(1, retries + 1):
        try:
            return func()
        except (TimeoutException, StaleElementReferenceException) as e:
            print(f"Attempt {attempt} for {description} failed: {e}. Retrying...")
            time.sleep(1)
    raise Exception(f"Failed to {description} after {retries} attempts.")

def login():
    """Log in to the gym website."""
    login_btn = wait.until(ec.element_to_be_clickable((By.ID, "login-button")))
    login_btn.click()

    email_input = wait.until(ec.presence_of_element_located((By.ID, "email-input")))
    email_input.clear()
    email_input.send_keys(ACCOUNT_EMAIL)

    password_input = driver.find_element(By.ID, "password-input")
    password_input.clear()
    password_input.send_keys(ACCOUNT_PASSWORD)

    submit_btn = driver.find_element(By.ID, "submit-button")
    submit_btn.click()

    # Wait until the schedule page loads as confirmation
    wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

def book_class(booking_button):
    """Click booking or waitlist button and wait for confirmation."""
    booking_button.click()
    wait.until(lambda d: booking_button.text in ["Booked", "Waitlisted"])

def main():
    retry(login, description="login")

    class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")
    booked = 0
    waitlisted = 0
    already_handled = 0

    for card in class_cards:
        day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
        day_text = day_group.find_element(By.TAG_NAME, "h2").text

        # Filter classes for Tuesday or Thursday at 6:00 PM
        if "Tue" in day_text or "Thu" in day_text:
            time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
            if "6:00 PM" in time_text:
                class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
                button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")

                info = f"{class_name} on {day_text} {time_text}"

                if button.text == "Booked" or button.text == "Waitlisted":
                    print(f"Already {button.text.lower()} for: {info}")
                    already_handled += 1
                elif button.text == "Book Class":
                    retry(lambda: book_class(button), description="book class")
                    print(f"Successfully booked: {info}")
                    booked += 1
                elif button.text == "Join Waitlist":
                    retry(lambda: book_class(button), description="join waitlist")
                    print(f"Joined waitlist for: {info}")
                    waitlisted += 1
                time.sleep(0.5)

    print(f"\nSummary: Booked: {booked}, Waitlisted: {waitlisted}, Already handled: {already_handled}")

    # Optional: Verify bookings on My Bookings page
    def verify_bookings():
        my_bookings_link = wait.until(ec.element_to_be_clickable((By.ID, "my-bookings-link")))
        my_bookings_link.click()
        wait.until(ec.presence_of_element_located((By.ID, "my-bookings-page")))

        cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")
        verified = 0

        for c in cards:
            try:
                when_info = c.find_element(By.XPATH, ".//p[strong[text()='When:']]").text
                if ("Tue" in when_info or "Thu" in when_info) and "6:00 PM" in when_info:
                    class_title = c.find_element(By.TAG_NAME, "h3").text
                    print(f"Verified booking: {class_title}")
                    verified += 1
            except NoSuchElementException:
                continue

        print(f"Total bookings verified: {verified}")

    verify_bookings()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Do not quit Chrome immediately since detach=True. To close browser, call driver.quit() manually.
        print("Execution completed. Remember to close the browser manually if needed.")
