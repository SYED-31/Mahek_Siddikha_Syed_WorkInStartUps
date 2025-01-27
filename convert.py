import pandas as pd
import json

# Load the JSON data from the output file
# Use raw string (r) to avoid escape sequence issues
with open(r"scrapy_project/scrapy_project/spiders/output/output.json", "r", encoding='utf-8') as f:
    data = json.load(f)

# Convert the JSON data into a DataFrame
df = pd.DataFrame(data)

# Rename columns to match the desired format
df.rename(columns={
    "job_title": "Job Title",
    "company_name": "Company Name",
    "location": "Location",
    "job_type": "Job Type",
    "job_description": "Job Description",
    "email": "Contact Information",
    "application_link": "Application Link"
}, inplace=True)

# Reorder columns to match the desired format
df = df[["Job Title", "Company Name", "Location", "Job Type", "Job Description", "Contact Information", "Application Link"]]

# Save the DataFrame to an Excel file
df.to_excel("Mahek_Siddikha_Syed_WorkInStartUps.xlsx", index=False, engine="openpyxl")

print("Excel file saved as Mahek_Siddikha_Syed_WorkInStartUps.xlsx")