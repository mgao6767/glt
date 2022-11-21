
/******************************************************************************/
/* SETUP                                                                      */
/******************************************************************************/

%let wrds_usr = mgao6767; 
%let wrds_pwd = %sysget(WRDS_PASSWORD);


/******************************************************************************/
/* Download WRDS data                                                         */
/******************************************************************************/

%let wrds       = wrds-cloud.wharton.upenn.edu 4016;
options comamid = TCP 
        remote  = WRDS;

signon username=&wrds_usr. password="&wrds_pwd";

%syslput _GLOBAL_;

rsubmit;

proc sql;
	create table urls as 
	select conm as companyName, gvkey, weburl, dldte as deletionDate
	from comp.company;
quit;

proc download data=urls out=urls; run;


endrsubmit;
signoff;

proc export data=urls dbms=csv outfile="./urls.csv" replace; run;

