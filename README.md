# fb_page_names
Data and SQL scripts showing the history of changes in page names of FB advertisers

This repository describes the known problems with changes in page names of Facebook advertisers.

## Background

As part of monitoring the electoral campaigns in the United States, Wesleyan Media Project downloads and stores the Facebook aggregate reports that are available from this [page](https://www.facebook.com/ads/library/report). The Lifelong ("All Dates") report is particularly important because it provides the total amount spent by a political advertiser on the platform. WMP stores these reports in a database and uses them to compute exact spend by advertisers within specific time periods, for instance, general campaign of 2022.

When an advertiser registers on Facebook platform, it is assigned a unique page id. The advertiser can choose the page name, and can change that name later on. The aggregate reports provide the current (that is, on the date the report was generated) page name, and thus do not provide the continuity in tracking the page names. A reported page name may be modified, or it can even be reported as an empty string if the page was taken down.

This repository provides two CSV tables with information on the previous names of Facebook pages. The `FB_page_name

