/*
 Q: How much time does it take on average to reach the order_confirmation screen per session (in minutes)?
 Join ocs and aos based on fullvisitorid and sessionid (same as visitId?) and then subtract app.opened - order_confirmation and then create avg(*)
 */
SELECT ROUND(AVG(h.time) / 60000, 2) AS avgTimeConfirmOrder
FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` as gse, gse.hit as h
JOIN
    (SELECT fullvisitorId, visitId, min(h2.hitNumber) as hitNumber,
    FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` as gse, gse.hit as h2, h2.customDimensions as cd
    WHERE (h2.isInteraction = TRUE OR screenviews IS NOT NULL) AND (cd.index = 11 AND cd.value = 'order_confirmation')
    GROUP BY fullvisitorId, visitId) as foc
ON gse.fullvisitorid = foc.fullvisitorId AND gse.visitId = foc.visitId AND h.hitNumber = foc.hitNumber
JOIN order_confirmation_sessions AS ocs
ON td.unique_id = ocs.unique_id