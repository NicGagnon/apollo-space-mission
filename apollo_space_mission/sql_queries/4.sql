/*
 Q: By using the GoogleAnalyticsSample data and BackendDataSample tables, analyse
    how often users tend to change their location in the beginning of their journey (screens
    like home and listing) versus in checkout and on order placement and demonstrate the
    the deviation between earlier and later inputs (if any) in terms of coordinates change.

    1. Identify Screen pipeline, whats the order of screens that a client goes through
    2. Determine Beginning and End screens
        a) Beginning Screens: Home, listing
        b) Ending Screens: Checkout, Order Placement
    3. Extract sessions where users changed their location at the beginning
    4. Extract sessions where users changed their location at the end
    5. Table should demonstrate two rows: one for early changers, one for late changers and avg change in terms of lat and lon
    6. (optional but necessary for second step) Table showing all early changers and late changers


    {
        "axis": "longitude",
        "avg_early_location_change": "1.321557510764046",
        "avg_late_location_change": "2.3494541612865283"
    },
    {
        "axis": "latitude",
        "avg_early_location_change": "1.321798197523602",
        "avg_late_location_change": "2.3736642537056114"
    }
    Then, using the BackendDataSample table, see if those customers who changed their
    address ended placing orders and if those orders were delivered successfully, if so, did
    they match their destination.

    1. Join the two tables based on the gse.hit.customDimensions.value and bds.frontendOrderId with cd.index = 36
    2. Add column with 1 or 0 per session depending if they placed and order
    3. Add column with 1 or 0 per session if delivery successful
    4. Add column with 1 or 0 or NA per session if delivery matched destination (NA if delivery not successful)
    5. Final Table should have fullvisitorId, visitId, group_name (early changer, late changer), three columns above
    6. Extract table showing main stats between the two groups (
        % of group that placed an order,
        % of group that had a successful delivery,
        % of successful delivery with matched address per group)

    Q: nuance between 000001 and 0
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
            cur_hit.event_category as event_category,
            cur_hit.cur_hitnumber as cur_hitnumber,
            MAX(prev_hit.custom_dim_value) as old_lon,
            MAX(cur_hit.custom_dim_value) as new_lon,
            MIN(prev_hit.custom_dim_value) as old_lat,
            MIN(cur_hit.custom_dim_value) as new_lat
        FROM
            gse as prev_hit
        JOIN
            gse as cur_hit
        ON
            prev_hit.fullvisitorid = cur_hit.fullvisitorid
            AND prev_hit.visitid = cur_hit.visitid
        WHERE
            prev_hit.cur_hitnumber = (cur_hit.cur_hitnumber - 1)
            AND (
                    (
                        cur_hit.custom_dim_index = 19
                        AND prev_hit.custom_dim_index = 19
                    )
                    OR
                    (
                        cur_hit.custom_dim_index = 18
                        AND prev_hit.custom_dim_index = 18
                    )
            )
            AND cur_hit.custom_dim_value <> prev_hit.custom_dim_value
        GROUP BY cur_hit.fullvisitorid, cur_hit.visitId, cur_hit.cur_hitnumber, cur_hit.event_category
    ),
    early_addr_changers AS
    (
        SELECT
            lc.*,
            gse2.custom_dim_value as frontEndId
        FROM lc
        INNER JOIN gse2
        ON lc.fullVisitorId = gse2.fullVisitorId AND lc.visitId = gse2.visitID
        WHERE lc.event_category in ('android.home', 'ios.home', 'android.shop_list', 'ios.shop_list', 'Account')
    ),
    late_addr_changers AS
    (
        SELECT
            lc.*,
            gse2.custom_dim_value as frontEndId
        FROM lc
        INNER JOIN gse2
        ON lc.fullVisitorId = gse2.fullVisitorId AND lc.visitId = gse2.visitID
        WHERE lc.event_category in ('android.checkout', 'ios.checkout', 'android.order_confirmation', 'ios.order_confirmation', 'Transaction')
    )
SELECT *
FROM late_addr_changers
LIMIT 100


/*

    flt AS
    (
        SELECT
            fullVisitorId,
            visitId,
            event_category,
            max(case when seq = 1 then index end) A new_lon,
            max(case when seq = 1 then index end) A new_lon,
        FROM
            (
                fullVisitorId, visitId, event_category, index, value,
                    row_number() over(partition by fullVisitorId, visitId, event_category order by fullVisitorId, visitId, event_category) seq
                FROM lc
            ) d
            group by fullVisitorId, visitId, event_category
    )
 */