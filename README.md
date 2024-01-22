# Housing Data

This application start an API application that will serve CSV data from the zillow public housing data site at https://www.zillow.com/research/data/. There are currently two endpoints that will serve housing data using either using metro, city, state, county, zip code, or neighborhood endpoints. One endpoints will give the data for all house across the US and the other will give data based on home size between 1 and 5.

# Setup 
In order for the application to work you can first obtain the needed data from [zillow](https://www.zillow.com/research/data/) and go to home values and have data type be "ZHVI All Homes (SFR, Condo/Co-op) Time Series, Smoothed, Seasonally Adjusted" and "ZHVI 1-Bedroom Time Series" and obtain all geography types. Do this for all Bedroom time series data. One you have all the CSV files use clone or download repository. Once the repository is downloaded run these commands to create the necessary directories.
```
cd housing_market

mkdir housing_data

cd housing_data

mkdir House_Values & mkdir Zillow_Home_Values

cd Zillow_Home_Values

mkdir Housing_Values_Adjusted

cd ..

cd House_Values

mkdir Housing_Values_1-Bedroom
mkdir Housing_Values_2-Bedroom
mkdir Housing_Values_3-Bedroom
mkdir Housing_Values_4-Bedroom
mkdir Housing_Values_5+-Bedroom
```

Once all of the directories have been made place all the CSV's from the "ZHVI All Homes (SFR, Condo/Co-op) Time Series, Smoothed, Seasonally Adjusted" into the Zillow_home_values/Housing_Values_Adjusted directory and data from "ZHVI {1-5}-Bedroom Time Series" in their respective locations. For example data from "ZHVI 3-Bedroom Time Series" will go in House_Values/Housing_Values_3-Bedroom. 

# Build Docker Image
Build the docker image by running in the housing_market directory
```
docker build -t real-estate-api .
```

Once the image has been built it can be run with 
```
docker run -p 8000:8000 real-estate-api 
```

# Access Data

Once everthing has been set up you can access data by navigating to localhost:8000 to confirm the api is working. 

## Example Queries


https://github.com/electricman991/housing_market/assets/82842730/5e033d27-f54e-4110-b3da-df7216936f20

Get housing data for cities across the US
```
localhost:8000/housing_prices/city
```

Get housing data for 2 bedroom houses across the US
```
localhost:8000/housing_prices/city/2
```
