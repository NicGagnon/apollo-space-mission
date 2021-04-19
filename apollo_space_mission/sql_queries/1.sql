/*
Unique visitId
 */
SELECT count(*)
FROM `dhh-analytics-hiringspace.BackendDataSample.transactionalData`
GROUP BY visitId