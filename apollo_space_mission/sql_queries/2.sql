/*
 Q: How many sessions does each visitor create?
 A: Same as previous question with the addition of group by on visitor ID
 */
SELECT fullVisitorId, count(*) AS total_user_sessions
FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` as gse, gse.hit as h
WHERE h.isInteraction = TRUE OR screenviews IS NOT NULL
GROUP BY fullVisitorId
