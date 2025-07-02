built a browser automation tool to scrape UPenn's Course review.

reasoning:
was too lazy to figure out how to get the API or email them for the API. so just used playwright and coded a workflow. 

learnings:
no need to complicate things. workflow > agent for simple stuff. 
playwright consistent browser is amazing. you can just bypass the login stuff via human and then by having it remember the browser, you can just be auto logged in. 
parallelizing is important. I didn't do that. but if I had threaded/created multiple playwright instances to scrape different parts of their course catalog, it wouldn't have taken so long. 
