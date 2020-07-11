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

# Example 1
Make tables to count the number of lesions found in the LAD/LCx/RCA for each processed patient.  Split results into STEMI versus Other MI groups.  Recreate the table below.

![example1-tables](/readme-media/example1-tables.png)