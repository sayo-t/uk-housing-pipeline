select
    district,
    date_trunc('month', sale_date)::date            as sale_month,
    property_type,
    count(*)                                        as sales_count,
    round(avg(price))                               as avg_price,
    percentile_cont(0.5) within group (order by price) as median_price
from {{ ref('stg_price_paid') }}
where ppd_category_type = 'A'
group by 1, 2, 3
