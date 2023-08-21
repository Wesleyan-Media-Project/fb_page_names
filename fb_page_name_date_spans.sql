with a0 as (select page_id, max(page_name) as page_name, date
  from wmp-laura.fb_lifelong.fb_lifelong
  where page_id <> "0"
  group by page_id, date),

a as (
  select page_id, page_name, date,
  LAG(page_name, 1) OVER my_window as prev_name
  from a0
  WINDOW my_window as (partition by page_id order by date)
  order by date),

a1 as (select page_id, page_name, date,
  page_name <> prev_name as is_new
  from a
  where prev_name is NOT NULL), 

b as ( select *, SUM(CAST(is_new as INT)) OVER my_window as section
  from a1
  WINDOW my_window as (
    partition by page_id
    order by date 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
  ),

c as (select page_id, page_name, min(date) as min_date, max(date) as max_date
  from b
  group by page_id, page_name, section)

select * from c order by page_id, max_date;
