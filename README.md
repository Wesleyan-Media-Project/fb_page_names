# fb_page_names
Data and SQL scripts showing the history of changes in page names of FB advertisers

This repository describes the known problems with changes in page names of Facebook advertisers.

## Background

As part of monitoring the electoral campaigns in the United States, Wesleyan Media Project downloads and stores the Facebook aggregate reports that are available from this [page](https://www.facebook.com/ads/library/report). The Lifelong ("All Dates") report is particularly important because it provides the total amount spent by a political advertiser on the platform. WMP stores these reports in a database and uses them to compute exact spend by advertisers within specific time periods, for instance, general campaign of 2022. You can read more about the aggregate reports and how they are processed in the [fb_agg_reports_import](https://github.com/Wesleyan-Media-Project/fb_agg_reports_import) repository.

When an advertiser registers on Facebook platform, it is referred to as a "Facebook page" and is assigned a unique page id. The advertiser can choose the name of the page, and can change that name later on. The aggregate reports provide the current (that is, on the date the report was generated) page name, and thus do not provide the continuity in tracking the names. A reported page name may be modified, or it can even be reported as an empty string if the page was taken down. In addition, there are transitory problems when some of the posted reports miss page names - the field is reported as an empty string instead.

This repository provides two CSV tables with information on the previous names of Facebook pages. One of them - FB_page_name_date_spans - is provided as a Zipped file due to the limits on the size of a file that can be hosted on GitHub.

Facebook started including `page_id` field into the aggregate reports in July 2019 and our tables report page name changes between July 2019 and August 2023.

## Page name date spans

To use this table, download the file `FB_page_name_date_spans.csv.zip` and unpack it. The resulting CSV file will be 143 MB large. 

For each page id that had a change in its name, there is a row showing the page_id, page_name, and the date span when this name was in effect. The goal of this table is to assist analysts who have data for a past period but need to find out under what name did an advertiser operate at the time.

For example, here is a screenshot of the rows referring to Rep. Cori Bush [Wikipedia page](https://en.wikipedia.org/wiki/Cori_Bush) who in 2020 was elected to Congress as a representatives of the 1st Congressional District of Missouri.

<img width="912" alt="Screenshot 2023-08-21 at 9 40 16 AM" src="https://github.com/Wesleyan-Media-Project/fb_page_names/assets/17502191/8e6f0e66-59fa-4102-acc9-9a14279a107b">

The SQL script that was used to generate the data is contained in the `fb_page_name_data_spans.sql` file in the repo.

## Page name history

The CSV file with this table is 9 MB large and did not require compression. The table contains page_id, last non-empty name of the page, and the previous names separated by the equals sign `=` as a delimiter.

Here is a screenshot of a few rows.

<img width="886" alt="Screenshot 2023-08-21 at 9 54 51 AM" src="https://github.com/Wesleyan-Media-Project/fb_page_names/assets/17502191/09d99e83-226f-4225-81a3-5c7a3b7272ff">

We anticipate that the `last_known_as` field will be especially useful. As was already mentioned above, when a page gets deleted, it is still reported in the aggregate report, but the page name field is empty. For somebody who is in possession of only a single CSV file with the aggregate report, it is impossible to find out (in an automated way) the names that were used by the page in the past.

The SQL script that was used to generate this table is available in the `fb_page_name_history.sql` file.


## Possible applications

As an illustration of the utility of the data, let's examine if there were cases when pages have traded names: a name that was owned by one page_id would become associated with a different page_id.

The script takes the `FB_page_name_history.csv` file, splits the `all_names` string into individual page_names, joins the table with itself and keeps the rows where the page_ids were different.

As a final touch, the script chooses the rows where the names contained 'PAC' - an abbreviation for "Political Action Committee".


```{r}
library(dplyr)
library(readr)
library(tidyr)
library(stringi)

df = read_csv("FB_page_name_history.csv",
                         col_types = "ccc")

d = df %>% mutate(pn = stri_split(all_names, fixed="=")) %>% 
  unnest(pn) %>% 
  filter(pn != "") %>% 
  filter(!stri_detect(all_names, regex="(?i)Marketplace|Instagram")) %>% 
  select(-last_known_as)
  
x = d %>% 
  inner_join(d, 
             by="pn", 
             suffix=c("_x", "_y"),
             relationship = "many-to-many") %>% 
  filter(page_id_x != page_id_y) %>% 
  distinct(pn, page_id_x, all_names_x, page_id_y, all_names_y)
  

x %>% filter(stri_detect(all_names_x, fixed="PAC")) %>% write_csv("pac_demo.csv")

```
And here is a screenshot of the `pac_demo.csv` opened in Excel:

<img width="933" alt="Screenshot 2023-08-21 at 10 37 44 AM" src="https://github.com/Wesleyan-Media-Project/fb_page_names/assets/17502191/11880e1a-1e4a-46dc-8403-e42ca0620d7a">

