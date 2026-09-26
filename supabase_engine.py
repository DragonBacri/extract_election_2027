from supabase import create_client, Client
from dotenv import load_dotenv
import os
import supabase

load_dotenv(dotenv_path= '.env.prod')

sup_url = os.getenv("SUPABASE_URL")
sup_key = os.getenv("SUPABASE_KEY")



def create_engine() :
    supabase: Client = create_client(sup_url, sup_key)
    
    return supabase