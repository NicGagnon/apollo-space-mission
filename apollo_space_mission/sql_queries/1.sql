/*
Q: How many sessions are there?
Google Analytics defines a session as a set of hits with at least one pageview (screen view for Apps) or interactive event
Total Rows = 7276346
Total Sessions = 7275280
 */
SELECT count(*) AS total_sessions
FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` as gse, gse.hit as h
WHERE h.isInteraction = TRUE OR screenviews IS NOT NULL -- Retrieve Sessions by ensuring at at least one interaction or screenview
