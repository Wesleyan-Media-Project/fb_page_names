create temp function removeDuplicates(s STRING, d STRING)
RETURNS STRING
LANGUAGE js
AS """
const names = s.split(d);
let word_set = new Set();
let unique_array = new Array();
let previous_name = "";

for (v of names) {
  if (previous_name != v) {
    unique_array.push(v); 
    previous_name = v;
    };
  };
return unique_array.join(d);
""";


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
  group by page_id, page_name, section
  ), 

c1 as (select page_id, max(max_date) as final_date 
  from c
  group by page_id),

c2 as (select x.page_id, x.page_name, x.min_date, x.max_date 
  from c as x inner join c1 as y using (page_id)
  where NOT (x.page_name = "" and x.max_date <> y.final_date)),
 
d as (select distinct page_id, LAST_VALUE(page_name) OVER my_window as last_known_as
  from c
  where page_name <> ""
  WINDOW my_window as (
    partition by page_id 
    order by max_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING))

select c2.page_id, d.last_known_as, 
  removeDuplicates(STRING_AGG(c2.page_name, "=" order by max_date), "=") as all_names
  from c2 inner join d using (page_id)
  group by c2.page_id, d.last_known_as
  HAVING COUNT(distinct c2.page_name) > 1
  order by page_id;
