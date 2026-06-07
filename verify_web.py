import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:8001")
        await page.screenshot(path="dashboard.png")
        print("Screenshot saved to dashboard.png")

        # Test task submission
        await page.fill('textarea[name="description"]', 'Test task from Playwright')
        await page.click('button[type="submit"]')
        await asyncio.sleep(1)
        content = await page.content()
        if '{"status":"received","description":"Test task from Playwright"}' in content:
            print("Task submission verified")
        else:
            print("Task submission failed or response unexpected")
            print(content)

        await browser.close()

asyncio.run(run())
