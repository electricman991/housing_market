from fastapi import FastAPI, HTTPException
import json
import csv
import pandas as pd
import os
import subprocess
cwd = os.path.dirname(os.path.realpath(__file__))

app = FastAPI()

def read_csv_file(file_path, lines, page_size=100, page=1):
    data = []
    start = (page - 1) * page_size
    end = start + page_size

    with open(file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for _ in range(start):
            next(csv_reader)
        
        for line_number, row in enumerate(csv_reader, start=start):
            if line_number >= end:
                break
            data.append(row)
        
        
    return data

def paginate(data, page, page_size, specific=None):
    start = (page - 1) * page_size
    end = start + page_size
    my_dict = {}
    
    if specific is not None:
        
        new_data = [item for item in data if item['RegionName'] == specific]
        if new_data == []:
            return {"error": "There is no data for the given parameter"}
        return new_data
    
    return data

@app.get("/")
async def root():
    return {"message": "Welcome to the Housing Market API!"}

@app.get("/housing_prices/{region_type}")

async def housing_prices_state(page: int = 1, region_type: str = 'state'):
    csvs = {'city': 'City_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv', 'county': 'County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv', 'metro': 'Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv', 'neighborhood': 'Neighborhood_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv', 'state': 'State_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv', 'zip': 'Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv'}
    house_type = {'adjusted': 'Housing_Values_Adjusted', 'BottomTier': 'Housing_Values_BottomTier_5-35', 'Condo': 'Housing_Values_Condo-Co-op', 'MidTier': 'Housing_Values_Raw_MidTier_35-65', 'Single-Family': 'Housing_Values_Single-Family', 'TopTier': 'Housing_Values_TopTier_65-95'}
    page_size = 100
    region_list = ['city', 'metro', 'state', 'zip', 'county']
    if region_type not in region_list:
        #return {"error": f"{region_type} is not a valid region type. Please choose from this list {region_list}"}
        raise HTTPException(status_code=404, detail=f"{region_type} is not a valid region type. Please choose from this list {region_list}")
    total_data = subprocess.check_output(f'wc -l {cwd}/housing_data/Zillow_Home_Values/{house_type["adjusted"]}/{csvs[region_type]}', shell=True)
    total_data = int(total_data.decode('utf-8').split(' ')[0])
    page_calculation = total_data // page_size
    if total_data % page_size != 0:
        total_pages = page_calculation + 1
    else:
        total_pages = page_calculation
    if page > total_pages:
        raise HTTPException(status_code=404, detail=f"For region type {region_type} there are only {total_pages} pages of data")
        #return {"error": f"Please choose a page number between 1 and {total_pages}"}
   
    json_data = read_csv_file(f'{cwd}/housing_data/Zillow_Home_Values/{house_type["adjusted"]}/{csvs[region_type]}', page_size, page_size, page)

    paginated_data = paginate(json_data, page, page_size)
    return {"page": page, "page_size": page_size, "total_amount": total_data, "total_pages": total_pages, "data": paginated_data}

@app.get("/housing_prices/{house_size}/{data}")
async def housing_prices_single(page: int = 1, data: str = 'metro', house_size: str = '1', specific: str = None):
    csvs = {'city': f'City_zhvi_bdrmcnt_{house_size}_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv', 'county': f'County_zhvi_bdrmcnt_{house_size}_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv', 'metro': f'Metro_zhvi_bdrmcnt_{house_size}_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv', 'neighborhood': f'Neighborhood_zhvi_bdrmcnt_{house_size}_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv', 'state': f'State_zhvi_bdrmcnt_{house_size}_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv', 'zip': f'Zip_zhvi_bdrmcnt_{house_size}_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv'}
    house_data = {'1': 'Housing_Values_1-Bedroom/', '2': 'Housing_Values_2-Bedroom/', '3': 'Housing_Values_3-Bedroom/', '4': 'Housing_Values_4-Bedroom/', '5': 'Housing_Values_5+-Bedroom/'}
    page_size = 100
    house_list = ['1','2','3','4','5']
    region_list = ['city', 'metro', 'state', 'zip', 'county']
    if house_size not in house_list:
        #return {"error": f"{house_size} is not a valid house size. Please enter a valid house size from 1-5"}
        raise HTTPException(status_code=404, detail=f"{house_size} is not a valid house size. Please enter a valid house size from 1-5")
    if data not in region_list:
        #return {"error": f"{data} is not a valid region type. Please choose from this list {region_list}"}
        raise HTTPException(status_code=404, detail=f"{data} is not a valid region type. Please choose from this list {region_list}")

    total_data = subprocess.check_output(f'wc -l {cwd}/housing_data/House_Values/{house_data[house_size]}/{csvs[data]}', shell=True)
    total_data = int(total_data.decode('utf-8').split(' ')[0])
    page_calculation = total_data // page_size
    if total_data % page_size != 0:
        total_pages = page_calculation + 1
    else:
        total_pages = page_calculation

    if page > total_pages:
        raise HTTPException(status_code=404, detail=f"For housing size {house_size} and region type {data} there are only {total_pages} pages of data")
        #return {"error": f"For housing size {house_size} and region type {data} there are only {total_pages} pages of data"}
    json_data = read_csv_file(f'{cwd}/housing_data/House_Values/{house_data[house_size]}/{csvs[data]}', page_size, page_size, page)
    
    
    paginated_data = paginate(json_data, page, page_size, specific)
    return {"page": page, "page_size": page_size, "total_data": total_data, "total_pages": total_pages, "data": paginated_data}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("housing_data:app", host="0.0.0.0", port=8000, reload=True)