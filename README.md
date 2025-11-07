# Snack & Lift Gym Booking Automation

This project automates the booking process for the Snack & Lift gym website using Selenium and Python. It enables automatic login, booking of specific gym classes, waitlist handling, and robust retry logic to gracefully handle network or UI latency issues.

## Features

- Automatically logs into the Snack & Lift gym website  
- Filters and books Tuesday or Thursday 6:00 PM classes  
- Joins waitlists if classes are full  
- Retry mechanism to handle network timeouts and page load delays  
- Verifies booked classes on the "My Bookings" page  
- Uses a persistent Chrome user profile to maintain session cookies  
- Detached Chrome browser mode for manual inspection after script execution  

## Requirements

- Python 3.7+  
- Google Chrome browser  
- ChromeDriver executable compatible with your Chrome version (in your system PATH)  
- Python packages:  
  - selenium  

Install Selenium with:  

## Setup

1. Clone or download this repository.  
2. Update the `ACCOUNT_EMAIL` and `ACCOUNT_PASSWORD` variables in the script with your Snack & Lift credentials.  
3. Ensure Chromedriver is installed and added to your PATH.

## Usage

Run the Python script:  

The script will:  
- Open a Chrome browser and navigate to https://appbrewery.github.io/gym/  
- Log in with the provided credentials  
- Search for Tuesday or Thursday 6:00 PM classes and attempt booking  
- Join waitlists if the classes are full  
- Print summary of bookings and verify them on the "My Bookings" page  
- Keep the browser open so you can manually inspect the actions  

## Notes

- The browser is kept open after script completion to allow manual verification (due to `detach=True`). Close it manually when done.  
- The script uses a Chrome user data profile folder named `chrome_profile` in the current directory to persist cookies and sessions.  
- Retry wrappers ensure the bot is resilient to slow page loads and element detection timing out.  
- Customize the class filters (day/time) in the script as needed.  

## Troubleshooting

- If you encounter a `SessionNotCreatedException`, ensure to fully close any existing Chrome instances using the profile folder before rerunning the script.  
- Increase the wait timeout (default 10 seconds) in the script if you face network slowness.  
- Verify that element IDs and class names in the HTML have not changed on the gym website for consistent bot operation.  

## License

This is an open example script provided as-is for learning and automation purposes.


