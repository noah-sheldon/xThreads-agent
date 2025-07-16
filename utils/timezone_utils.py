"""
Timezone utilities for UK/US time conversion and optimal posting times
"""

from datetime import datetime, time
from zoneinfo import ZoneInfo
from typing import Dict, List

def get_uk_time() -> datetime:
    """Get current UK time"""
    return datetime.now(tz=ZoneInfo("Europe/London"))

def get_us_eastern_time() -> datetime:
    """Get current US Eastern time"""
    return datetime.now(tz=ZoneInfo("America/New_York"))

def convert_us_to_uk_time(us_time_str: str) -> str:
    """Convert US time string to UK time"""
    try:
        # Parse US time (assuming Eastern)
        us_time = datetime.strptime(us_time_str, "%H:%M").time()
        us_datetime = datetime.combine(datetime.today(), us_time)
        us_datetime = us_datetime.replace(tzinfo=ZoneInfo("America/New_York"))
        
        # Convert to UK time
        uk_datetime = us_datetime.astimezone(ZoneInfo("Europe/London"))
        return uk_datetime.strftime("%H:%M")
    except:
        return us_time_str

def get_optimal_posting_times() -> Dict[str, Dict[str, str]]:
    """Get optimal posting times for each platform (UK time)"""
    return {
        'twitter': {
            'slot1': '14:00',      # 9 AM EST
            'slot2': '15:30',      # 10:30 AM EST  
            'slot3': '17:00',      # 12 PM EST
            'slot4': '20:00'       # 3 PM EST
        },
        'threads': {
            'slot1': '14:30',      # 9:30 AM EST
            'slot2': '16:00',      # 11 AM EST
            'slot3': '17:30'       # 12:30 PM EST
        },
        'linkedin': {
            'slot1': '13:00'       # 8 AM EST
        },
        'reddit': {
            'slot1': '12:00',      # 7 AM EST
            'slot2': '14:30'       # 9:30 AM EST
        },
        'instagram': {
            'slot1': '16:00'       # 11 AM EST
        },
        'tiktok': {
            'slot1': '17:30'       # 12:30 PM EST
        },
        'facebook': {
            'slot1': '18:30'       # 1:30 PM EST
        },
        'quora': {
            'slot1': '23:30'       # 6:30 PM EST
        }
    }

def is_optimal_posting_time(platform: str, uk_time_str: str) -> bool:
    """Check if given UK time is optimal for platform"""
    optimal_times = get_optimal_posting_times()
    platform_times = optimal_times.get(platform, {})
    
    return uk_time_str in platform_times.values()

def get_next_optimal_time(platform: str) -> str:
    """Get the next optimal posting time for a platform"""
    current_uk = get_uk_time()
    optimal_times = get_optimal_posting_times()
    platform_times = optimal_times.get(platform, {})
    
    current_time_str = current_uk.strftime("%H:%M")
    
    # Find next optimal time
    for time_key in ['primary', 'secondary', 'tertiary']:
        optimal_time = platform_times.get(time_key)
        if optimal_time and optimal_time > current_time_str:
            return optimal_time
    
    # If no time today, return primary time for tomorrow
    return platform_times.get('primary', '12:00')