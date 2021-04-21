/*
 Q: How many sessions does each visitor create?
 */
SELECT fullVisitorId, count(*) AS total_user_sessions
FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` as gse, gse.hit as h
WHERE h.isInteraction = TRUE OR screenviews IS NOT NULL
GROUP BY fullVisitorId
