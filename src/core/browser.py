from playwright.sync_api import sync_playwright

def create_browser(profile_path: str, headless: bool = False):
    p = sync_playwright().start()
    browser = p.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        channel="chrome",
        headless=headless,
        args=[
            "--disable-session-crashed-bubble",
            "--disable-features=AutomationControlled",
            "--no-first-run",
            "--no-default-browser-check",
        ])
    return p, browser
