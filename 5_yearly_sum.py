# user inputs ________________________________________________________________________________________________

Monthly_product_folder=r"C:\Users\h.jayasekara\Desktop\WaporData\L2_NPP_M" #insert file path
ds_code='L2_NPP_M'    #ds code for file naming should insetr refering WaPOR docs
shapefile = r"C:\Users\h.jayasekara\Desktop\WaporData\Sri_lanka\final1.shp"     #path_to_shapefile.shp
start_date='2015-01-01'
end_date='2022-12-31'
# ____________________________________________________________________________________________________________

product_name = ds_code.split("_")
naming_product = product_name[1]

path_split = os.path.split(Monthly_product_folder)
naming_year = path_split[1]

#output folder name
output_folder=Monthly_product_folder.replace(naming_year,'Maha_{}'.format(naming_product)) 


if (naming_product == "NPP"):
    correction_factor = 0.001
    
elif (naming_product == "AET"):
    correction_factor = 0.1

else:
    print("error")
    sys.exit()
    

# ____________________________________________________________________________________________________________
    
    
input_fhs=glob.glob(os.path.join(Monthly_product_folder,'*.tif'))
input_fhs

#Get year to array
year_dates=pd.date_range(start_date,end_date,freq='Y')

#Get df avail 
WaPOR.API.version=2
df_avail=WaPOR.API.getAvailData(ds_code,time_range='{0},{1}'.format(start_date,end_date))


if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    
    
driver, NDV, xsize, ysize, GeoT, Projection = gis.GetGeoInfo(input_fhs[0])

# for creating a yearly sum
for year in year_dates:
    
    SumArray = np.zeros((ysize, xsize), dtype=np.float32)
    for fh in input_fhs:
        Array = gis.OpenAsArray(fh, nan_values=True)
        SumArray += Array

    SumArray  =  correction_factor * SumArray

    # Save the result as a GeoTIFF file
    out_fh = os.path.join(output_folder, 'WaPOR_{}_{}.tif'.format(naming_product,year.year))  
    gis.CreateGeoTiff(out_fh, SumArray, driver, NDV, xsize, ysize, GeoT, Projection)