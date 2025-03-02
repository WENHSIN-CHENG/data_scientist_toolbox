import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def plot_horizontal_bars(sql_query: str,fig_name: str, shareyaxis: bool=False):
    connection = sqlite3.connect("data/kaggle_survey.db")
    response_counts = pd.read_sql(sql_query,con=connection)
    connection.close()
    fig, axes = plt.subplots(ncols=3, figsize=(32, 8),sharey= shareyaxis)
    survey_years = [2020,2021,2022]
    for i in range(len(survey_years)):
        survey_year = survey_years[i]
        response_counts_year = response_counts[response_counts["surveyed_in"] == survey_year]
        y = response_counts_year["response"].values
        width = response_counts_year["response_count"].values
        axes[i].barh(y,width)
        axes[i].set_title(f"{survey_year}")
    plt.tight_layout()
    fig.savefig(f"{fig_name}.png")

sql_query = """
SELECT surveyed_in,
       question_type,
       response,
       response_count
  FROM aggregated_responses
 WHERE (question_index = 'Q17' AND surveyed_in IN (2020, 2021)) OR
       (question_index = 'Q18' AND surveyed_in = 2022)
 ORDER BY surveyed_in,
          response_count;
"""
plot_horizontal_bars(sql_query, "data_science_job_machine_learnings")