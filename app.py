import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto('https://www.amazon.com/')
        await page.wait_for_load_state('load')
  
        await page.screenshot(path="/Users/zikangjiang/learning_coding/browser_agent_tutorial1/ss.png")
        clickableContent = await page.query_selector_all('a, button, [role = "button"], [onClick]')
        # print(clickableContent)

        labeled_elements = []
        labeled_elements_text = []
        for index in range(len(clickableContent)):
            text = await clickableContent[index].inner_text()
            cleaned_text = " ".join(text.split())

            if text:
                labeled_elements.append(clickableContent[index])
                labeled_elements_text.append(cleaned_text)

                if text == "Men's fashion":
                    await clickableContent[index].click()
                    await page.wait_for_load_state('load')
                    await page.screenshot(path="/Users/zikangjiang/learning_coding/browser_agent_tutorial1/clicked.png")
                    # print(click_result)

asyncio.run(main())