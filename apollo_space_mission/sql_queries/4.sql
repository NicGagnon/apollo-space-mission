/*
 Q: By using the GoogleAnalyticsSample data and BackendDataSample tables, analyse
    how often users tend to change their location in the beginning of their journey (screens
    like home and listing) versus in checkout and on order placement and demonstrate the
    the deviation between earlier and later inputs (if any) in terms of coordinates change.
    Then, using the BackendDataSample table, see if those customers who changed their
    address ended placing orders and if those orders were delivered successfully, if so, did
    they match their destination.
 */
WITH gse as
    (
        SELECT gse.fullVisitorId AS fullVisitorId,
            gse.visitId AS visitID,
            h.hitNumber AS cur_hitnumber,
            h.eventCategory AS event_category,
            cd.index AS custom_dim_index,
            cd.value AS custom_dim_value
        FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` as gse, unnest(gse.hit) as h, unnest(h.customDimensions) as cd
        WHERE cd.index in (18, 19)
    ),
    gse2 AS
    (
        SELECT
            gse.fullVisitorId AS fullVisitorId,
            gse.visitId AS visitID,
            cd.value AS custom_dim_value
        FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` as gse, unnest(gse.hit) as h, unnest(h.customDimensions) as cd
        WHERE cd.index = 36 and (cd.value IS NOT NULL AND cd.value <> 'NA' AND cd.value NOT LIKE 'CA_%')
        GROUP BY gse.fullVisitorId, gse.visitId, cd.value
    ),
    lc AS
    (
        SELECT
            cur_hit.fullvisitorid as fullVisitorId,
            cur_hit.visitId as visitId,
            cur_hit.cur_hitnumber as cur_hitNumber,
            cur_hit.event_category as event_category,
            prev_hit.custom_dim_value as oldLat,
            cur_hit.custom_dim_value as newLat
        FROM
            gse as prev_hit
        JOIN
            gse as cur_hit
        ON
            prev_hit.fullvisitorid = cur_hit.fullvisitorid
            AND prev_hit.visitid = cur_hit.visitid
        WHERE
            prev_hit.cur_hitnumber = (cur_hit.cur_hitnumber - 1)
            AND cur_hit.custom_dim_index = 19
            AND prev_hit.custom_dim_index = 19
            AND cur_hit.custom_dim_value <> prev_hit.custom_dim_value
    ),
    lc2 AS
    (
        SELECT
            cur_hit.fullvisitorid as fullVisitorId,
            cur_hit.visitId as visitId,
            cur_hit.cur_hitnumber as cur_hitNumber,
            cur_hit.event_category as event_category,
            prev_hit.custom_dim_value as oldLong,
            cur_hit.custom_dim_value as newLong
        FROM
            gse as prev_hit
        JOIN
            gse as cur_hit
        ON
            prev_hit.fullvisitorid = cur_hit.fullvisitorid
            AND prev_hit.visitid = cur_hit.visitid
        WHERE
            prev_hit.cur_hitnumber = (cur_hit.cur_hitnumber - 1)
            AND cur_hit.custom_dim_index = 18
            AND prev_hit.custom_dim_index = 18
            AND cur_hit.custom_dim_value <> prev_hit.custom_dim_value
    ),
    lc_merged AS
    (
        SELECT
            lc.fullVisitorId,
            lc.visitId,
            lc.event_category,
            ST_GEOGPOINT(SAFE_CAST(lc2.oldLong AS FLOAT64), SAFE_CAST(lc.oldLat  AS FLOAT64)) AS oldLocation,
            ST_GEOGPOINT(SAFE_CAST(lc2.newLong AS FLOAT64), SAFE_CAST(lc.newLat  AS FLOAT64)) AS newLocation
        FROM
            lc
        JOIN
            lc2
        ON
            lc.fullvisitorid = lc2.fullVisitorId AND lc.visitId = lc2.visitID AND lc.cur_hitNumber = lc2.cur_hitNumber
    ),
    address_changers AS
    (
        SELECT
            lc_merged.fullvisitorid,
            lc_merged.visitId,
            lc_merged.oldLocation,
            lc_merged.newLocation,
            gse2.custom_dim_value as frontEndId,
            CASE
                WHEN lc_merged.event_category IN ('android.home', 'ios.home', 'android.shop_list', 'ios.shop_list', 'Account') THEN 'early_changer'
                WHEN lc_merged.event_category IN ('android.checkout', 'ios.checkout', 'android.order_confirmation', 'ios.order_confirmation', 'Transaction') THEN 'late_changer'
                ELSE 'mid_changer'
            END
            AS addressChangeStatus
        FROM lc_merged
        INNER JOIN gse2
        ON lc_merged.fullVisitorId = gse2.fullVisitorId AND lc_merged.visitId = gse2.visitID
    ),
    bds as
    (
        SELECT
            ac.fullVisitorId,
            ac.visitID,
            ac.oldLocation,
            ac.newLocation,
            geopointDropoff,
            addressChangeStatus,
            CASE
                WHEN orderDate IS NOT NULL THEN 'yes'
                ELSE 'no'
            END as didCustomerOrder,
            CASE
                WHEN declinereason_code IS NOT NULL THEN 'yes'
                ELSE 'no'
            END as wasOrderSuccesful,
            CASE
                WHEN declinereason_code IS NULL THEN 'no' -- Only to follow nested if logic
                WHEN ST_EQUALS(newLocation, geopointCustomer) THEN 'yes'
                ELSE 'no'
            END as doesDeliveryAddrMatchChangedAddr
    FROM address_changers as ac
            LEFT JOIN `dhh-analytics-hiringspace.BackendDataSample.transactionalData` as td
            ON ac.frontEndId = td.frontendOrderId
    )
SELECT *
FROM bds