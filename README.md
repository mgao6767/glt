# glt

Use [lighthouse-ci](https://github.com/andreasonny83/lighthouse-ci) to collect Google Lighthouse scores for some companies.

The `urls.csv` is a list of companies is constructed using the script `company_url.sas`, which contains the `gvkey`, `companyName`, `weburl` and `deletionDate` sourced from Compustat via WRDS.

To allow for time to load and execute all JavaScript logic, it waits for a certain amount of time by providing a `pauseAfterLoadMs` value in the custom config file.

## collection process

Make sure that [`npm`](https://www.npmjs.com/) is installed.

First, download this repo to local computer and navigate into the folder.

```bash
git clone https://github.com/mgao6767/glt.git
cd glt
```

Second, use SAS to run `company_url.sas` and get `urls.csv` in the folder.

Then, run `main.py`. Two folders will be created: `/data` for storing the scores by date-company, and `/log` for storing the associated log files by date.
