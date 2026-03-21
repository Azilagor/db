

-- Запрос 1: Рейтинг популярных маршрутов за прошлый год
-- Сложный JOIN (route + hike + tourist_hike + route_season + inventory)
-- HAVING для фильтрации маршрутов с походами
WITH route_point_counts AS (
    SELECT
        route_id,
        COUNT(*) AS point_count
    FROM route_point
    GROUP BY route_id
),
route_seasons_agg AS (
    SELECT
        rs.route_id,
        STRING_AGG(s.name, ', ' ORDER BY s.name) AS seasons
    FROM route_season rs
    JOIN season s ON s.id = rs.season_id
    GROUP BY rs.route_id
),
hike_stats AS (
    SELECT
        h.route_id,
        COUNT(DISTINCT h.id)            AS hike_count,
        COUNT(DISTINCT th.tourist_id)   AS unique_tourists,
        COUNT(th.tourist_id)            AS total_tourists,
        ROUND(COUNT(th.tourist_id)::NUMERIC / NULLIF(COUNT(DISTINCT h.id), 0), 2) AS avg_tourists_per_hike
    FROM hike h
    LEFT JOIN tourist_hike th ON th.hike_id = h.id
    WHERE EXTRACT(YEAR FROM h.start_date) = EXTRACT(YEAR FROM NOW()) - 1
    GROUP BY h.route_id
    HAVING COUNT(DISTINCT h.id) > 0
),
popular_inventory AS (
    SELECT DISTINCT ON (h.route_id)
        h.route_id,
        i.name  AS inventory_name,
        SUM(hi.quantity) AS total_qty
    FROM hike h
    JOIN hike_inventory hi ON hi.hike_id = h.id
    JOIN inventory i ON i.id = hi.inventory_id
    WHERE EXTRACT(YEAR FROM h.start_date) = EXTRACT(YEAR FROM NOW()) - 1
    GROUP BY h.route_id, i.name
    ORDER BY h.route_id, SUM(hi.quantity) DESC
)
SELECT
    r.id                                        AS route_id,
    r.name                                      AS route_name,
    COALESCE(rpc.point_count, 0)                AS point_count,
    COALESCE(rsa.seasons, '—')                  AS seasonality,
    el.name                                     AS difficulty,
    COALESCE(hs.hike_count, 0)                  AS hike_count,
    COALESCE(hs.unique_tourists, 0)             AS unique_tourists,
    COALESCE(hs.total_tourists, 0)              AS total_tourists,
    COALESCE(hs.avg_tourists_per_hike, 0)       AS avg_tourists_per_hike,
    COALESCE(pi.inventory_name, '—')            AS popular_inventory
FROM route r
JOIN experience_level el ON el.id = r.level_id
LEFT JOIN route_point_counts rpc ON rpc.route_id = r.id
LEFT JOIN route_seasons_agg rsa ON rsa.route_id = r.id
LEFT JOIN hike_stats hs ON hs.route_id = r.id
LEFT JOIN popular_inventory pi ON pi.route_id = r.id
ORDER BY hike_count DESC;



-- Запрос 2: Клиенты, не участвовавшие в турах более года
-- LEFT JOIN + IS NULL для поиска отсутствующих данных
WITH last_hike AS (
    SELECT
        th.tourist_id,
        MAX(h.start_date)       AS last_hike_date,
        COUNT(DISTINCT h.id)    AS total_hikes
    FROM tourist_hike th
    JOIN hike h ON h.id = th.hike_id
    GROUP BY th.tourist_id
),
seasonal_counts AS (
    SELECT
        th.tourist_id,
        SUM(CASE WHEN EXTRACT(MONTH FROM h.start_date) IN (3,4,5)   THEN 1 ELSE 0 END) AS spring_count,
        SUM(CASE WHEN EXTRACT(MONTH FROM h.start_date) IN (6,7,8)   THEN 1 ELSE 0 END) AS summer_count,
        SUM(CASE WHEN EXTRACT(MONTH FROM h.start_date) IN (9,10,11) THEN 1 ELSE 0 END) AS autumn_count,
        SUM(CASE WHEN EXTRACT(MONTH FROM h.start_date) IN (12,1,2)  THEN 1 ELSE 0 END) AS winter_count
    FROM tourist_hike th
    JOIN hike h ON h.id = th.hike_id
    GROUP BY th.tourist_id
)
SELECT
    t.id                                AS client_id,
    t.full_name,
    t.email                             AS contact,
    lh.last_hike_date,
    COALESCE(lh.total_hikes, 0)         AS total_hikes,
    CONCAT(
        COALESCE(sc.spring_count, 0), '-',
        COALESCE(sc.summer_count, 0), '-',
        COALESCE(sc.autumn_count, 0), '-',
        COALESCE(sc.winter_count, 0)
    )                                   AS seasonal_breakdown
FROM tourist t
LEFT JOIN last_hike lh ON lh.tourist_id = t.id
LEFT JOIN seasonal_counts sc ON sc.tourist_id = t.id
WHERE lh.last_hike_date < NOW() - INTERVAL '1 year'
   OR lh.last_hike_date IS NULL
ORDER BY lh.last_hike_date ASC NULLS FIRST;



-- Запрос 3: Статистика походов по месяцам за прошлый год
-- Оконная функция ROWS BETWEEN для нарастающего итога
-- LAG для сравнения с предыдущим месяцем
WITH monthly_data AS (
    SELECT
        EXTRACT(MONTH FROM h.start_date)::INT          AS month_num,
        TRIM(TO_CHAR(h.start_date, 'Month'))           AS month_name,
        CASE
            WHEN EXTRACT(MONTH FROM h.start_date) IN (12,1,2) THEN 'Зима'
            WHEN EXTRACT(MONTH FROM h.start_date) IN (3,4,5)  THEN 'Весна'
            WHEN EXTRACT(MONTH FROM h.start_date) IN (6,7,8)  THEN 'Лето'
            ELSE 'Осень'
        END                                             AS season_name,
        COUNT(DISTINCT h.id)                            AS hike_count,
        COUNT(th.tourist_id)                            AS total_participants,
        COUNT(DISTINCT th.tourist_id)                   AS unique_participants
    FROM hike h
    LEFT JOIN tourist_hike th ON th.hike_id = h.id
    WHERE EXTRACT(YEAR FROM h.start_date) = EXTRACT(YEAR FROM NOW()) - 1
    GROUP BY month_num, month_name, season_name
),
with_running_totals AS (
    SELECT
        *,
        SUM(hike_count) OVER (
            ORDER BY month_num
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_hike_count,
        SUM(total_participants) OVER (
            ORDER BY month_num
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_participants,
        LAG(hike_count) OVER (ORDER BY month_num) AS prev_month_hikes
    FROM monthly_data
),
top_guide_per_month AS (
    SELECT DISTINCT ON (EXTRACT(MONTH FROM h.start_date)::INT)
        EXTRACT(MONTH FROM h.start_date)::INT  AS month_num,
        g.full_name                             AS top_guide_name,
        COUNT(gh.hike_id)                       AS guide_hike_count
    FROM guide_hike gh
    JOIN guide g ON g.id = gh.guide_id
    JOIN hike h ON h.id = gh.hike_id
    WHERE EXTRACT(YEAR FROM h.start_date) = EXTRACT(YEAR FROM NOW()) - 1
    GROUP BY EXTRACT(MONTH FROM h.start_date)::INT, g.full_name
    ORDER BY EXTRACT(MONTH FROM h.start_date)::INT, COUNT(gh.hike_id) DESC
)
SELECT
    wrt.month_num,
    wrt.month_name,
    wrt.season_name,
    wrt.hike_count,
    wrt.total_participants,
    wrt.unique_participants,
    wrt.running_hike_count,
    wrt.running_participants,
    wrt.prev_month_hikes,
    wrt.hike_count - COALESCE(wrt.prev_month_hikes, 0) AS hike_count_diff,
    tg.top_guide_name,
    tg.guide_hike_count
FROM with_running_totals wrt
LEFT JOIN top_guide_per_month tg ON tg.month_num = wrt.month_num
ORDER BY wrt.month_num;



-- Запрос 4: Географическая информация о маршрутах
-- Оконные функции для первой/последней точки
WITH ordered_points AS (
    SELECT
        rp.id,
        rp.route_id,
        rp.name,
        rp.latitude,
        rp.longitude,
        rp.order_id,
        ROW_NUMBER() OVER (PARTITION BY rp.route_id ORDER BY rp.order_id NULLS LAST, rp.id) AS rn,
        COUNT(*) OVER (PARTITION BY rp.route_id) AS total_points
    FROM route_point rp
),
first_points AS (
    SELECT route_id, name AS first_name, latitude AS first_lat, longitude AS first_lon
    FROM ordered_points WHERE rn = 1
),
last_points AS (
    SELECT route_id, name AS last_name, latitude AS last_lat, longitude AS last_lon
    FROM ordered_points WHERE rn = total_points
),
segment_distances AS (
    SELECT
        p1.route_id,
        p1.name   AS from_point,
        p2.name   AS to_point,
        ROUND(r.length_km / NULLIF(COUNT(*) OVER (PARTITION BY p1.route_id), 0), 2) AS segment_km
    FROM ordered_points p1
    JOIN ordered_points p2
        ON p2.route_id = p1.route_id
        AND p2.rn = p1.rn + 1
    JOIN route r ON r.id = p1.route_id
),
segment_stats AS (
    SELECT
        route_id,
        ROUND(AVG(segment_km)::NUMERIC, 2) AS avg_segment_km,
        ROUND(MAX(segment_km)::NUMERIC, 2) AS max_segment_km,
        ROUND(MIN(segment_km)::NUMERIC, 2) AS min_segment_km
    FROM segment_distances
    GROUP BY route_id
)
SELECT
    r.id                                        AS route_id,
    r.name                                      AS route_name,
    op_cnt.total_points,
    fp.first_name                               AS first_point,
    CONCAT(fp.first_lat, ', ', fp.first_lon)    AS first_point_coords,
    lp.last_name                                AS last_point,
    CONCAT(lp.last_lat, ', ', lp.last_lon)      AS last_point_coords,
    COALESCE(r.length_km, 0)                    AS length_km,
    COALESCE(ss.avg_segment_km, 0)              AS avg_segment_km,
    COALESCE(ss.max_segment_km, 0)              AS max_segment_km,
    COALESCE(ss.min_segment_km, 0)              AS min_segment_km
FROM route r
LEFT JOIN (SELECT DISTINCT route_id, total_points FROM ordered_points) op_cnt
    ON op_cnt.route_id = r.id
LEFT JOIN first_points fp ON fp.route_id = r.id
LEFT JOIN last_points  lp ON lp.route_id = r.id
LEFT JOIN segment_stats ss ON ss.route_id = r.id
ORDER BY r.length_km DESC NULLS LAST;




-- Запрос 5: Пробег транспорта по маршрутам
-- LAG для расчёта простоя между походами
WITH transport_hike_history AS (
    SELECT
        ht.transport_id,
        h.id         AS hike_id,
        h.start_date,
        COALESCE(r.length_km, 0) AS route_km,
        LAG(h.start_date) OVER (
            PARTITION BY ht.transport_id
            ORDER BY h.start_date
        ) AS prev_hike_date
    FROM hike_transport ht
    JOIN hike  h ON h.id = ht.hike_id
    JOIN route r ON r.id = h.route_id
),
transport_stats AS (
    SELECT
        transport_id,
        MIN(start_date)                                      AS first_hike_date,
        MAX(start_date)                                      AS last_hike_date,
        ROUND(AVG(start_date - prev_hike_date)::NUMERIC, 1) AS avg_downtime_days,
        ROUND(SUM(route_km)::NUMERIC, 2)                    AS total_km
    FROM transport_hike_history
    GROUP BY transport_id
),
annual_km AS (
    SELECT
        transport_id,
        EXTRACT(YEAR FROM start_date)::INT AS yr,
        SUM(route_km)                      AS yearly_km
    FROM transport_hike_history
    GROUP BY transport_id, EXTRACT(YEAR FROM start_date)::INT
),
avg_annual_km AS (
    SELECT
        transport_id,
        ROUND(AVG(yearly_km)::NUMERIC, 2) AS avg_yearly_km
    FROM annual_km
    GROUP BY transport_id
)
SELECT
    t.id                                   AS transport_id,
    t.name                                 AS transport_name,
    t.kind                                 AS transport_type,
    ts.first_hike_date,
    ts.last_hike_date,
    COALESCE(ts.avg_downtime_days, 0)      AS avg_downtime_days,
    COALESCE(ts.total_km, 0)              AS total_km,
    COALESCE(aa.avg_yearly_km, 0)         AS avg_yearly_km
FROM transport t
LEFT JOIN transport_stats ts ON ts.transport_id = t.id
LEFT JOIN avg_annual_km   aa ON aa.transport_id  = t.id
ORDER BY ts.total_km DESC NULLS LAST;