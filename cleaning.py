import json
import re
import pandas as pd

def load_job_data(filepath, filetype="csv"):
    if filetype == "json":
        with open(filepath, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f]  
            df = pd.DataFrame(data)
    elif filetype == "csv":
        df = pd.read_csv(filepath,encoding='utf-8')  # Pandas  
    else:
        raise ValueError("Unsupported filetype")
    return df

filepath = r'C:\Users\my lenovo\Desktop\Webscraper_for_job\job_data.csv'
df = load_job_data(filepath)
def clean_job_data(df):
    """Cleans and preprocesses the job data in a Pandas DataFrame."""
    df.columns = df.columns.str.lower()
    df.fillna("N/A", inplace=True)
    df.drop_duplicates(subset=["job link"], keep="first", inplace=True)
    def clean_requirements(text):
        text = re.sub(r'\s+', ' ', text).strip()
        return text  # Or return list/string
    df["requirements"] = df["requirements"].apply(clean_requirements)
    return df
cleaned_df=clean_job_data(df)
cleaned_df.to_json("cleaned_job_data.json", orient="records", force_ascii=False)