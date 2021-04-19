/*
 This is for a two week window
 */
SELECT fullvisitorid, count(visitorId)
FROM `dhh-analytics-hiringspace.BackendDataSample.transactionalData`
GROUP BY fullvisitorid;

/*
 This is for until-this-point
 */
SELECT fullvisitorid, MAX(visitNumber)
FROM `dhh-analytics-hiringspace.BackendDataSample.transactionalData`
GROUP BY fullvisitorid