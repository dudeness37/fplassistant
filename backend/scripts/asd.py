"""
Simple test to see what Sportmonks data we can access
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv('../infra/.env')

def test_sportmonks_endpoints():
    api_key = os.getenv('SPORTMONKS_API_KEY')
    base_url = 'https://api.sportmonks.com/v3/football'
    
    print("Testing Sportmonks API endpoints...")
    print("=" * 50)
    
    # Test core endpoints
    endpoints = [
        ('fixtures', 'Recent fixtures'),
        ('teams', 'All teams'),
        ('players', 'All players'),
        ('leagues', 'All leagues'),
        ('seasons', 'All seasons'),
        ('standings', 'League standings'),
    ]
    
    for endpoint, description in endpoints:
        try:
            url = f'{base_url}/{endpoint}?api_token={api_key}'
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint:15} | {description}")
                print(f"   Keys: {list(data.keys())}")
                if 'data' in data:
                    print(f"   Records: {len(data['data'])}")
                    if data['data']:
                        # Show sample of first record
                        sample = data['data'][0]
                        print(f"   Sample keys: {list(sample.keys())[:5]}...")
            else:
                print(f"❌ {endpoint:15} | HTTP {response.status_code}")
        
        except Exception as e:
            print(f"❌ {endpoint:15} | Error: {e}")
        
        print()
    
    # Test Premier League specific data
    print("Testing Premier League specific endpoints...")
    print("-" * 50)
    
    pl_endpoints = [
        ('fixtures?filter[league_id]=8', 'PL fixtures'),
        ('teams?filter[league_id]=8', 'PL teams'),
        ('standings?filter[league_id]=8', 'PL standings'),
    ]
    
    for endpoint, description in pl_endpoints:
        try:
            url = f'{base_url}/{endpoint}&api_token={api_key}'
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {description:20} | Found {len(data.get('data', []))} records")
                if data.get('data'):
                    sample = data['data'][0]
                    print(f"   Sample: {sample.get('name', sample.get('home_team', 'N/A'))}")
            else:
                print(f"❌ {description:20} | HTTP {response.status_code}")
        
        except Exception as e:
            print(f"❌ {description:20} | Error: {e}")
        
        print()

if __name__ == "__main__":
    test_sportmonks_endpoints()