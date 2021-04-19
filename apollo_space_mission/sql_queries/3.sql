/*
 Join ocs and aos based on fullvisitorid and sessionid (same as visitId?) and then subtract app.opened - order_confirmation and then create avg(*)
 */
WITH order_confirmation_sessions AS (
    SELECT *
    FROM `dhh-analytics-hiringspace.BackendDataSample.transactionalData`
    GROUP BY visitId
    HAVING hit.customDimensions.index = 11 AND hit.customDimensions.value = 'order_confirmation'
    ),
    app_opened_sessions AS (
    SELECT *
    FROM `dhh-analytics-hiringspace.BackendDataSample.transactionalData`
    GROUP BY visitId
    HAVING hit.eventAction = app.opened
    )
SELECT *
FROM `dhh-analytics-hiringspace.BackendDataSample.transactionalData` as td
JOIN order_confirmation_sessions AS ocs
ON td.unique_id = ocs.unique_id