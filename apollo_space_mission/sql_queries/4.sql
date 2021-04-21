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
 */
WITH foc AS
(
    SELECT fullvisitorId, visitId, min(h2.hitNumber) as hitNumber,
    FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` as gse, gse.hit as h2, h2.customDimensions as cd
    WHERE (h2.isInteraction = TRUE OR screenviews IS NOT NULL) AND cd.value = 'order_confirmation'
    GROUP BY fullvisitorId, visitId
)
SELECT ROUND(AVG(h.time) / 60000, 2) AS avgConfirmOrderTime
FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` as gse, gse.hit as h
JOIN foc
ON gse.fullvisitorid = foc.fullvisitorId AND gse.visitId = foc.visitId AND h.hitNumber = foc.hitNumber
