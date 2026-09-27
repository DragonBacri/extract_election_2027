from dotenv import load_dotenv
import pandas as pd
from supabase_engine import create_engine
from datetime import datetime, timedelta



load_dotenv(dotenv_path= '.env.prod')


supabase = create_engine()


def import_polls() :
    url = "https://raw.githubusercontent.com/MieuxVoter/presidentielle2027/main/presidentielle2027.csv"
    df = pd.read_csv(url)
    
    return df[['poll_id', 'hypothese', 'nom_institut', 'commanditaire', 'debut_enquete', 'fin_enquete', 'echantillon', 'tour', 'candidat', 'parti', 'intentions', 'erreur_sup', 'erreur_inf']]

def import_hypotheses() :
    url = "https://raw.githubusercontent.com/MieuxVoter/presidentielle2027/main/hypotheses.csv"
    df = pd.read_csv(url) 
    
    resp_out = supabase.table("hypotheses").delete().neq("id", -1).execute()
    resp_in  = supabase.table("hypotheses").insert(df.to_dict("records")).execute()
    
    return resp_in
    
    

def get_polls_last_date(df_polls) :
    last_date_dt = pd.to_datetime(df_polls['fin_enquete']).drop_duplicates().sort_values(ascending= False).reset_index(drop= True)[0]
    last_date_str = df_polls['fin_enquete'].drop_duplicates().sort_values(ascending= False).reset_index(drop= True)[0]
    
    return last_date_dt, last_date_str

def replace_last_polls(df_polls, last_date_dt, last_date_str) :
    resp_del = supabase.table('polls').delete().gte("fin_enquete", last_date_dt).execute()
    df_last_date = df_polls[df_polls['fin_enquete'] == last_date_str]
    
    resp_add = supabase.table("polls").insert(df_last_date.to_dict("records")).execute()
    
    return resp_del, resp_add


if __name__ == '__main__':
    
    df_polls = import_polls()
    
    
    date_dt, date_str = get_polls_last_date(df_polls= df_polls)
    
    resp_del, resp_add = replace_last_polls(df_polls= df_polls, last_date_dt= date_dt, last_date_str= date_str)
    
    print(f"delete polls : {resp_del}")
    print(f"insert polls : {resp_add}")
    
    resp_hypo = import_hypotheses()
    
    print(f"import hypothese {resp_hypo}")
    
    
    
    
    

   
