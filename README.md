# Microsoft Access Database

For this project, we will use a Microsoft Access database and parse data using SQL queries.  We use Microsoft Access because it provides us an intuitive GUI.  Once we get a better grasp of our database design, we can shift to using MySQL or another free SQL service.  Unfortunately, Microsoft Access is only available for Windows PCs, as far as I know.

## Basic Terminology

### Tables
Think of a "table" as an Excel sheet.  A database is basically a collection of tables.  We can define set relationships between each table and link our data together in interesting ways (this is why we are specifically using a _relational_ database).

### Record
A "record" is just one row of a table.

### Query
A query is just a specific way of filter our data based on specific criteria.  We can also use queries to combine several tables or combine parts of separate tables.  All queries will have the prefix "qsel".


## Path to __Confirm__ Database
```
\\polaris.radsci.uci.edu\MCP_STUDY\STUDY\DATABASE\db_CONFIRM.accdb
```
## Confirm Tables
  The tables in the Confirm database are arranged as follows:
- Tables always have the prefix "tbl"
- Tables from the Confirm study have the prefix "tblConfirm"
- Tables that do not have the "tblConfirm" prefix are assumed to be generated from the MCP processing code
- "tblMCP" contains myocardial mass at-risk (mass_mcp_g) and other very important data generated during the MCP processing

## Important Fields in tblMCP
- id_main_vessel - This field denotes which main vessel the specific record is a part of
- id_patient - This is the Confirm patient ID; This can be related to the "confirm_idc_str" field in tblConfirmCONFIRM (very important)
- id_vessel_study - This is the "lesion ID" of the particular record;  This can be related to the "lesion_id" field in tblConfirmPerLesion
- id_vtree - This is the "type" of vessel tree organization;  There are three types "scct", "full", and "sub"; "scct" is a branch by branch organization of vessel branches, "full" organizes SCCT vessel segments into LAD, LCx and RCA trees (3 records for each patient), "sub" organizes vessel branches into proximal and distal vessel trees for the LAD, LCx, and RCA, based on the lesion; We will mainly be using the "sub" organization
- id_vessel - This is the actual vessel segment ID;  For "scct" organization, this the SCCT vessel label; For "sub", the vessel ID will denote the proximal/distal tree and which main vessel the record is of;  We will mainly be using id_vessel with "_dist", as this is the myocardial mass at-risk __distal__ to a lesion
- mass_mcp_g - This is the mass of myocardium relative to the vessel record, as determined by the MCP code, in __grams__
- mass_lv_g - This is the mass of the total left ventricle myocardium for that particular patient, in __grams__

## View Query as SQL
You can view a query made in Microsoft Access as an SQL query.  Basically, this will allow you to build a query in Access, and then copy and paste the SQL query into Python.  To view the SQL form of a query:  Open a query (double-click on the query on the left panel) > In the top left corner where it says "View", click the dropdown arrow and select "SQL" > You will now see the SQL query

Be aware, some conventions in Microsoft Access might not transfer directly to SQL.  For example, in Microsoft Access you use an * to search for a partial string occurrence (LIKE *_find_this_occurrence*).  When you use the SQL query in Python code, you might have to change the * to a % (LIKE %_find_this_occurrence%).

# Helpful Microsoft Access Queries

- _qselResults_: A family of queries to filter data for statistical analysis.  This can be the main starting point.  Each qselResults query is filtered with different criteria.  Currently, all qselResults queries filter patient data to provide the myocardial mass at-risk (mass_mcp_g) for the worst lesion.  There are patients with multiple lesions, we are only going to look at the lesions labeled as “the worst”, based on the Confirm study (see “worst_lesion” column in tblConfirm-Lesion). 


# Goals

Our main goal is to efficiently filter data, perform statistical analysis, and create graphs/tables, using scripts.  Not only with this save time, this will also ensure our results are reproducible.

To achieve this, we will follow some guidelines:

1.	Statistical analysis will be performed using ONE programming language (Python?)
1.	SQL queries will be used to parse data directly from our database
1.	All mathematic operations will be done in our Python code, not in the SQL query
1.	Use source control (GitHub)
1.	Consistent documentation
1.	Prototype first, generalize second
	-	Create a working prototype script
	-	Once we know exactly what we want, refine and generalize the script into reusable functions

# Examples
## Example 1
Make tables to count the number of lesions found in the LAD/LCx/RCA for each processed patient.  Split results into STEMI versus Other MI groups.  Recreate the table below.

![example1-tables](/readme-media/example1-tables.png)


## Example 2
Make a graph of the LV mass, the mass at-risk and the percent mass at-risk of patient data parsed from Example 1.  Do for “worst” lesions in each patient.  Recreate the graph below.

![example2-bargraph](/readme-media/example2-bargraph.png)


# Tasks
## Task 1
Task 1:  Make a bar graph, similar to __Example 2__.  Instead of analyzing the “worst” lesion, sum the mass at-risk of all lesions for each patient.  Split groups into STEMI and Other MI.

