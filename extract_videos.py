import os
from dotenv import load_dotenv
import serpapi
from supabase_engine import create_engine
from datetime import datetime, timedelta
import re

load_dotenv(dotenv_path= '.env.prod')

serp_key = os.getenv("SERP_API_KEY")

supabase = create_engine()

def get_time_from_delay(delay : str) :
    
    if delay :
        
        pattern =  r"(?<![A-Za-z])(?:h|d|min)(?![A-Za-z])|\d+"
        formated_delay  = "".join(re.findall(pattern, delay))
        
        
        
        now  = datetime.now()
        real_time =  datetime.now()
        if 'd' in formated_delay :
            days = int(re.findall(r'\d+',formated_delay)[0]) or 0
            real_time = now - timedelta(days= days )
            
        
        elif 'min' in formated_delay :
            minutes = int(re.findall(r'\d+',formated_delay)[0]) or 0
            real_time = now - timedelta(minutes= minutes )
            
        elif 'h' in formated_delay : 
            hours = int(re.findall(r'\d+',formated_delay)[0]) or 0
            real_time = now - timedelta(hours= hours)
        
    else :
        return datetime.now()
        
    return real_time

def get_videos(searche  = " Elections Présidentielles 2027" ) :
    client = serpapi.Client(api_key=serp_key)

    res = client.search({
    "engine": "youtube",
    "search_query": searche ,
    "sp": "EgQIAhAB",  
    "hl": "en",          
})
    
    return  res["video_results"]


if __name__ == '__main__':
    
    videos = get_videos()
    
    rows = []
    for v in videos :
        row = {
            "link" : v.get('link'),
            "title" : v.get('title'),
            "views" : v.get("views"),
            "channel" : v.get("channel").get("name"),
            "upload_at" : get_time_from_delay(v.get("published_date")).isoformat(),
            "lenght" : v.get('length'),
            "description" : v.get("description")
            
            
        }
        rows.append(row)
    
    res = supabase.table("videos").insert(rows).execute()
    print(len(res.data), "lignes insérées")

