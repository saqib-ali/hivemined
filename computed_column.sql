ALTER TABLE openstatistics.rssitems DROP COLUMN SHOW_ON_HIVEMINED;
ALTER TABLE openstatistics.rssitems
ADD COLUMN SHOW_ON_HIVEMINED INT AS 
(CASE 
WHEN "postUrl" LIKE '%careers.%.edu%' OR "postUrl" LIKE '%jobs.%.edu%'  OR "postUrl" LIKE '%opportunities.%.edu%'  OR "postUrl" LIKE '%employment.%.edu%' OR "postUrl" LIKE '%careers.%.ac.%' OR "postUrl" LIKE '%jobs.%.ac.%' OR "postUrl" LIKE '%opportunities.%.ac.%' OR "postUrl" LIKE '%employement.%.ac.%'  OR "postUrl" LIKE '%.ac.%/job%' OR "postUrl" LIKE '%.ac.%/career%' OR "postUrl" LIKE '%.ac.%/Vacanc%'  OR "postUrl" LIKE '%.edu.%/job%' OR "postUrl" LIKE '%.edu.%/career%'  OR "postUrl" LIKE '%.edu.%/Vacanc%' OR "postUrl" LIKE '%.edu/job%' OR "postUrl" LIKE '%.edu/career%'  OR "postUrl" LIKE '%.edu/Vacanc%' OR "postUrl" LIKE '%wvu.taleo.net%'  OR "postUrl" LIKE '%cfopitt.taleo.net%'  OR "postUrl" LIKE 'https://www.jobbnorge.no/en/%' OR "postUrl" LIKE '%umb.taleo.net%' OR "postUrl" LIKE '%iit.taleo.net%'  OR "postUrl" LIKE '%facultypositions.stanford.edu%'
OR "postUrl" LIKE 'https://earlham.edu/job/%'
THEN 1
ELSE 0
END)
STORED;



