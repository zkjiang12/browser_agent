##########
#########
# MAKING THIS FOR PENN COURSE REVIEW. JUST A SIMPLE AUTOMATION TOOL. AGENTIC STUFF NEXT VERSION.
# MAKING THIS FOR PENN COURSE REVIEW. JUST A SIMPLE AUTOMATION TOOL. AGENTIC STUFF NEXT VERSION.
# MAKING THIS FOR PENN COURSE REVIEW. JUST A SIMPLE AUTOMATION TOOL. AGENTIC STUFF NEXT VERSION.
#########
##########

import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
import json

from google import genai

# Load environment variables from .env file
load_dotenv()

# Initialize client with API key from environment
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def parse_course_data(all_texts, department):
    """Parse scraped text into structured course data"""
    courses = []
    i = 0
    
    while i < len(all_texts):
        text = all_texts[i].strip()
        
        # Skip empty or numeric-only text
        if not text or text.replace('.', '').isdigit():
            i += 1
            continue
        
        # Look for course name followed by 4 numbers
        if i + 4 < len(all_texts):
            try:
                course_quality = float(all_texts[i + 1])
                instructor_quality = float(all_texts[i + 2])
                difficulty = float(all_texts[i + 3])
                work_required = float(all_texts[i + 4])
                
                course = {
                    "course_name": text,
                    "course_quality": course_quality,
                    "instructor_quality": instructor_quality,
                    "difficulty": difficulty,
                    "work_required": work_required,
                    "department": department
                }
                courses.append(course)
                print(f"✅ Parsed: {text} - Quality: {course_quality}")
                i += 5  # Skip the 4 numbers
            except (ValueError, IndexError):
                i += 1
        else:
            i += 1
    
    return courses

async def main():
    async with async_playwright() as p:
        # Create a persistent context that saves to disk
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./browser_data",  # Directory to save session data
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security"
            ]
        )
        page = await context.new_page()
        
        await page.goto('https://penncoursereview.com/')
        await page.wait_for_load_state('domcontentloaded')

        #landing page code.
        await page.locator('input').fill("math")
        print("filled input")
        await page.wait_for_load_state('domcontentloaded')
        await page.wait_for_timeout(2000)

        print('pause')
        await page.locator('input').press('Enter')
        print("pressed enter on input field")

        await page.wait_for_load_state('domcontentloaded')
        await page.wait_for_timeout(4000)

        # Scrape departments
        departments = ['AAMW','ACCT','ACFD','AFRC','ALAN','AMCS','AMEL','AMHR','ANAT','ANCH','ANTH','APOP','ARAB','ARCH','ARTH','ASAM','ASLD','ASTR','BAAS','BCHE','BCS','BDS','BE','BEPP','BENF','BENG','BIOE','BIOL','BIOM','BMIN','BMB','BIOT','BSTA','CAMB','CBE','CHEM','CHIC','CHIN','CIMS','CINM','CIS','CIT','CLCH','CLSC','CLST','CML','COGS','COLL','COMM','COML','CPLN','CRIM','CRWR','CZCH','DATA','DATS','DADE','DATA','DEMG','DENT','DIGC','DISG','DSGN','DTCH','DYNM','EALC','EAS','EASC','ECON','EDCL','EDEN','EDHE','EDMC','EDME','EDPR','EDSC','EDSL','EDTC','EDTF','EDUC','EESC','ENGL','ENGR','ENLT','ENM','ENMG','ENVS','EPID','ESE','ETHC','FIGS','FILP','FNAR','FNCE','FREN','FRSM','GADS','GAFL','GAS','GBIO','GCB','GDSD','GEND','GLBS','GMPA','GOHS','GOMD','GOPH','GORT','GPED','GPRD','GPRS','GREK','GRMN','GSWS','GUJR','HCIN','HCMG','HEBR','HIND','HIST','HPR','HQS','HSPV','HSSC','HSOC','IGBO','ICOM','IMP','INDO','INSP','INTG','INTR','IPD','IRIS','ITAL','JPAN','JWST','KAND','KORN','LANG','LALS','LARP','LATN','LAW','LAWM','LEAD','LGIC','LGST','LING','MALG','MAPP','MATH','MEAM','MELC','MGMT','MKTG','MLA','MLYM','MODM','MPHY','MRTI','MSE','MSSP','MSCI','MTHS','MTR','MUSC','MUSA','NANO','NETS','NEUR','NGG','NPLD','NRS (Nursing codes: NURS, NRSC, etc.)','NUTR','OIDD','ORGC','PASH','PERS','PHIL','PHRM','PHYL','PHYS','PLSH','PPE','PPOL','PRTG','PROW','PSCI','PSYC','PUBH','PUNJ','QUEC','REAL','REES','RELC','REG','RELS','ROBO','ROML','RUSS','SARB','SAST','SCMP','SKRT','SOCW','SOCI','SPAN','SPPO','SPRO','SSPP','STAT','STSC','SWAH','SWED','SWRK','TAML','TELU','THAI','THAR','TIBT','TIGR','TURK','TWI','UKRN','URBS','URDU','VCSP','VCSN','VIET','VIPR','VISR','VLST','VMED','VPTH','YDSH','YORB','ZULU']
        all_courses = []

        for dept in departments:
            print(f"\n{'='*50}")
            print(f"SCRAPING {dept} DEPARTMENT")
            print(f"{'='*50}")
            try:
                await page.goto(f"https://penncoursereview.com/department/{dept}")
                await page.wait_for_load_state('domcontentloaded')
                await page.wait_for_timeout(5000)
                
                # Get all span text content
                spans = await page.query_selector_all('span')
                all_texts = []
                
                for span in spans:
                    text = await span.inner_text()
                    if text.strip():
                        all_texts.append(text.strip())
                
                # print(f"Found {len(all_texts)} text elements")
                
                # Parse course data for this department
                department_courses = parse_course_data(all_texts, dept)
                all_courses.extend(department_courses)
                
                # print(f"Parsed {len(department_courses)} courses from {dept}")
            except:
                pass

        # Structure data for output
        structured_data = {
            "total_courses": len(all_courses),
            "departments": departments,
            "courses": all_courses,
            "data_explanation": {
                "course_quality": "Overall course rating (1-5 scale, higher is better)",
                "instructor_quality": "Instructor rating (1-5 scale, higher is better)", 
                "difficulty": "Course difficulty (1-5 scale, higher is more difficult)",
                "work_required": "Workload level (1-5 scale, higher is more work)"
            }
        }

        # Save to JSON file
        with open('penn_courses_data.json', 'w') as f:
            json.dump(structured_data, f, indent=2)
        
        print(f"\n✅ FINAL RESULT:")
        print(f"Total courses scraped: {len(all_courses)}")
        print(f"Data saved to: penn_courses_data.json")
        
        # Print sample of data
        if all_courses:
            print(f"\nSample course:")
            print(json.dumps(all_courses[0], indent=2))

        await context.close()

asyncio.run(main())