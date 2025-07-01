


##########
#########
# MAKING THIS FOR PENN COURSE REVIEW. JUST A SIMPLE AUTOMATION TOOL. AGENTIC STUFF NEXT VERSION.
# MAKING THIS FOR PENN COURSE REVIEW. JUST A SIMPLE AUTOMATION TOOL. AGENTIC STUFF NEXT VERSION.
# MAKING THIS FOR PENN COURSE REVIEW. JUST A SIMPLE AUTOMATION TOOL. AGENTIC STUFF NEXT VERSION.
#########
##########

import asyncio
import os
import base64
from dotenv import load_dotenv
from playwright.async_api import async_playwright

from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Initialize client with API key from environment
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


async def cleanContent(elements_list):
    usable_elements = []
    for index in range(len(elements_list)):
        text = await elements_list[index].inner_text()

        if text:
            usable_elements.append({
                "text": text,
                "element": elements_list[index]
            })
            print(text)

    return usable_elements

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto('https://penncoursereview.com/')
        await page.wait_for_load_state('domcontentloaded')
        
  
        clickableContent = await page.query_selector_all('a, button, span, [role = "button"], [onClick]')
        #the *= means contains instead of equals.
        inputForms = await page.query_selector_all('textarea, input, div, [name*="username"], [name*="login"], [name*="password"], [name*="email"], [placeholder*="username"], [placeholder*="password"], [placeholder*="email"], [id*="login"], [id*="signup"]')
        # Also search for sign-in related elements more broadly
        signInElements = await page.query_selector_all('a[href*="signin"], a[href*="login"], button[aria-label*="sign"], [id*="sign"], [class*="sign"], a:has-text("Sign in"), a:has-text("sign in"), button:has-text("Sign in")')
        
        await page.screenshot(path="/Users/zikangjiang/learning_coding/browser_agent_tutorial1/ss.png")

        parsed_clickable_content = await cleanContent(clickableContent)
        parsed_inputForms = await cleanContent(inputForms)
        parsed_signInElements = await cleanContent(signInElements)

        # Read the screenshot and encode it for Gemini
        screenshot_path = "/Users/zikangjiang/learning_coding/browser_agent_tutorial1/ss.png"
        with open(screenshot_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = [
                "You are a helpful browser use assistant. you do the tasks on the browser that the user tells you to do! ",
                "I want to figure out what courses I should take for my freshman year at UPenn.",
                "These are the elements extracted from the website. What is the current situation and What is the action we should take next. Respond with the specific element name that we should click or that we should input text into. If that element is not available in the list of elements presented, then respond by saying what we still need to look. ",
                f"{parsed_clickable_content}, {parsed_inputForms},{parsed_signInElements}",
            ]
        )
        print("=== AI RESPONSE ===")
        print(response.candidates[0].content.parts[0].text)

asyncio.run(main())



#Note: probably save the below (FIXES NEEDED) part for v2 or something. If I'm just doing browser automation, then I can just code a workflow. 

#FIXES NEEDED
#need to make sure it gets the entire page a lot better 
#can potentially use langchain to make the responses cleaner because THEN, 
# we can use Gemini to tell us what to get the label of and then we can get that element and we can have tools(or for now just a workflow) 
# where if it needs to click it runs that code or if it needs to input it does that. 
# ok, that's very cool. and then everytime the page changes, we just take another screen shot. 