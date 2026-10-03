with source as (

    select * from {{ source('raw', 'price_paid') }}

),

renamed as (

    select
        trim(both '{}' from transaction_id)         as transaction_id,
        price::integer                              as price,
        date_of_transfer::timestamp::date           as sale_date,
        nullif(postcode, '')                        as postcode,
        case property_type
            when 'D' then 'Detached'
            when 'S' then 'Semi-detached'
            when 'T' then 'Terraced'
            when 'F' then 'Flat/Maisonette'
            else 'Other'
        end                                         as property_type,
        case old_new when 'Y' then true when 'N' then false end as is_new_build,
        case duration
            when 'F' then 'Freehold'
            when 'L' then 'Leasehold'
            else 'Unknown'
        end                                         as tenure,
        upper(town_city)                            as town_city,
        upper(district)                             as district,
        upper(county)                               as county,
        ppd_category_type,
        record_status
    from source

)

select * from renamed
