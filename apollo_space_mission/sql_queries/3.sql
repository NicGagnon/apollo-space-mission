/*
 Q: How much time does it take on average to reach the order_confirmation screen per session (in minutes)?
 foc - First Order Confirmation
 */
WITH foc AS -- Table represents sessions with a custom dimension value of order_confirmation
(
    SELECT fullvisitorId, visitId, min(h2.hitNumber) as hitNumber
    FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` as gse, gse.hit as h2, h2.customDimensions as cd
    WHERE (h2.isInteraction = TRUE OR screenviews IS NOT NULL) AND cd.value = 'order_confirmation'
    GROUP BY fullvisitorId, visitId
)
SELECT ROUND(AVG(h.time) / 60000, 2) AS avgConfirmOrderTime -- Time (milliseconds) reflects time since session started, hence avg of all the aforementioned sessions provides avg order time
FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` as gse, gse.hit as h
JOIN foc
ON gse.fullvisitorid = foc.fullvisitorId AND gse.visitId = foc.visitId AND h.hitNumber = foc.hitNumber
