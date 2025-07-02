Built a browser automation tool to scrape UPenn's Course review.

Reasoning + Design Choices:

needed to figure out what classes to take at Penn. didn't want to actually look into requirements. prompted Gemini, but it lacked sufficient context on quality and rigor of courses. So I decided to get that data from Penn Course Review.
But, was too lazy to figure out how to get the API/email them for the API. so just used playwright and coded a workflow to scrape everything. didn't scrape the teacher ratings since proffesor information is searchable with Gemini search grounding tool and that would have really increased the depth of the workflow. 

Learnings:
1) no need to complicate things. workflow > agent for simple stuff. 
2) playwright consistent browser is amazing. you can just bypass the login stuff via human and then by having it remember the browser, you can just be auto logged in. 
3) parallelizing is important. I didn't do that. but if I had threaded/created multiple playwright instances to scrape different parts of their course catalog, it wouldn't have taken so long. 
4) when scraping. CHECK WHAT THE DATA LOOKS LIKE. do it bit by bit. don't just scrape the whole thing at once, data has some bad parts/mispellings rn. Not sure if its my scraper or if its the db.

Meta Learning:
1) coding without tab complete in cursor is important. The best AI assisted coding, especially when learning, is to code most myself from reading the documentation and just trying, then asking Cursor (not agent mode) to explain the problem/potential solutions while prompting it based on ideas I have. AKA human centered, but using AI as a mentor watching over me. 
