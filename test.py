import time
import json
from playwright.sync_api import sync_playwright, expect, Page, Locator

# Initialize stats dictionary
stats = {
    'execution_time': 0.0,
    'assertions_passed': 0,
    'assertions_failed': 0,
    'total_assertions': 0,
    'step_coverage': [],
    'performance': {
        'page_loads': [],  # List of floats (time in seconds)
        'action_times': [] # List of floats (time in seconds)
    },
    'accessibility_violations': 0, # Not directly tested in this script, but included for completeness
    'locator_retries': 0,         # Not directly tested in this script, but included for completeness
    'errors': []                  # List of strings
}

def track_assertion(assertion_func, *args, **kwargs):
    """Helper to wrap assertions and track stats."""
    stats['total_assertions'] += 1
    try:
        assertion_func(*args, **kwargs)
        stats['assertions_passed'] += 1
    except AssertionError as e:
        stats['assertions_failed'] += 1
        stats['errors'].append(f"Assertion Failed: {e}")
    except Exception as e:
        stats['assertions_failed'] += 1
        stats['errors'].append(f"Unexpected Error during assertion: {e}")

def track_action_time(action_func, *args, **kwargs):
    """Helper to measure and track action execution time."""
    start = time.time()
    result = action_func(*args, **kwargs)
    end = time.time()
    stats['performance']['action_times'].append(end - start)
    return result

def run_test():
    global stats # Declare global to modify the dictionary

    start_time = time.time()

    with sync_playwright() as p:
        # Launch browser in non-headless mode
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # --- Step 1: Navigate to saucedemo.com ---
            step_start_time = time.time()
            page.goto("https://www.saucedemo.com/")
            page.wait_for_load_state('networkidle') # Wait for the page to be fully loaded
            stats['performance']['page_loads'].append(time.time() - step_start_time)
            stats['step_coverage'].append('Navigate to Login Page')

            # --- Step 2: Enter username and password ---
            # Locate username input using get_by_placeholder
            username_input = page.get_by_placeholder("Username")
            track_assertion(expect(username_input).to_be_visible)
            track_action_time(username_input.fill, "standard_user")

            # Locate password input using get_by_placeholder
            password_input = page.get_by_placeholder("Password")
            track_assertion(expect(password_input).to_be_visible)
            track_action_time(password_input.fill, "secret_sauce")

            # Locate login button using get_by_role (button) and get_by_text (Login)
            # Using .filter() to ensure we get the specific login button if multiple exist
            login_button = page.get_by_role("button", name="Login").filter(has_text="Login")
            track_assertion(expect(login_button).to_be_visible)
            track_action_time(login_button.click)
            stats['step_coverage'].append('Login')

            # --- Step 3: Verify products page after login ---
            # Wait for an element unique to the products page to be visible
            # Using get_by_text for the "Products" header
            products_header = page.get_by_text("Products").nth(0) # Use .nth(0) to pick the first if multiple exist
            track_assertion(expect(products_header).to_be_visible)

            # Also verify a specific product item to ensure content is loaded
            # Using get_by_alt_text for an image, or get_by_text for a product name
            sauce_labs_backpack = page.get_by_text("Sauce Labs Backpack")
            track_assertion(expect(sauce_labs_backpack).to_be_visible)

            # Verify the URL changed to the inventory page
            track_assertion(expect(page).to_have_url("https://www.saucedemo.com/inventory.html"))
            stats['step_coverage'].append('Verify Products Page')

        except Exception as e:
            stats['errors'].append(f"Test execution failed: {e}")
            # Optionally, take a screenshot on error
            # page.screenshot(path="error_screenshot.png")
        finally:
            # Close the browser
            browser.close()

    # Calculate total execution time
    stats['execution_time'] = time.time() - start_time

    # Print stats as JSON
    print("STATS_JSON_START")
    print(json.dumps(stats, indent=4))
    print("STATS_JSON_END")

if __name__ == "__main__":
    run_test()