from django.test import TestCase
from playwright.sync_api import Playwright, sync_playwright, expect

def test_default_stock_loads(playwright: Playwright) -> None:
    #setup
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:8000/stock-lookup/")

    #Assert
    expect(page.locator("text=AAPL")).to_be_visible()
    print("✓ Test PASSED! Found AAPL on the page")

    

    #cleaup
    context.close()
    browser.close()

    # Run the test
if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_default_stock_loads(playwright)

