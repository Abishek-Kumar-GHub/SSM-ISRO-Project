import os
import pandas as pd
import json
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import render,redirect
import pickle
from plotly.offline import plot
import plotly.graph_objects as go
import re
from astropy.io import fits
from django.conf import settings
import plotly.express as px
from viz_app.utils import source_name_index as sn
import numpy as np
from django.urls import reverse

pd.set_option("display.float_format", lambda x: f"{x:.15g}")

# Global variable to store dataframes
views_dir = os.path.dirname(os.path.abspath(__file__))
pickle_file_path = os.path.join(views_dir, 'SSM_dataframe_new.pkl')

# Load the initial DataFrame structure
with open(pickle_file_path, "rb") as f:
    ssm_data = pickle.load(f)

def plot_html(request):
    global ssm_data
    if not ssm_data:
        return render(request, "date_selector.html", {"error": "No data loaded. Please select a date range."})

    files = list(ssm_data.keys())  # Get available files without reloading
    return render(request, "plot_html.html", {"files": files})


def index(request):
    return render(request, "index.html")
class CorrelationView(View):
    def get(self, request):
        global ssm_data

        if not ssm_data:
            return JsonResponse({"error": "No data available. Please select a date range first."}, status=400)

        # Get available file names
        files = list(ssm_data.keys())

        return render(request, "correlation_html.html", {
            "files": files
        })

    def post(self, request):
        try:
            data = json.loads(request.body)
            file_name = data.get("file_name")
            selected_columns = data.get("columns", [])

            if not file_name or len(selected_columns) < 2:
                return JsonResponse({"error": "Select at least two columns."}, status=400)           
            df = ssm_data.get(file_name)            
            if df is None or df.empty:
                return JsonResponse({"error": "File not found or has no data."}, status=404)
            
            missing_columns = [col for col in selected_columns if col not in df.columns]
            if missing_columns:
                return JsonResponse({"error": f"Missing columns: {missing_columns}"}, status=400)
            
            correlation_matrix = df[selected_columns].corr()
            
            if correlation_matrix.empty:
                return JsonResponse({"error": "Correlation matrix is empty. Check the selected columns."}, status=400)

            # Create Plotly heatmap
            fig = px.imshow(
                correlation_matrix,
                labels=dict(x="Columns", y="Columns", color="Correlation"),
                x=correlation_matrix.columns,
                y=correlation_matrix.index,
                color_continuous_scale="RdBu",
                zmin=-1, 
                zmax=1
            )

            # Convert Plotly figure to JSON
            plot_json = fig.to_json()

            return JsonResponse({"plot_json": plot_json}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


def date_selector(request):
    return render(request, "date_selector.html")



# View to handle date selection and data population
class FileView(View):
    def get(self, request):
        global ssm_data  # Ensure global storage

        start_date_str = request.GET.get("start_date")
        end_date_str = request.GET.get("end_date")
       
        if not start_date_str or not end_date_str:
            return render(request, "date_selector.html", {"error": "Both 'start_date' and 'end_date' are required."})

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            if start_date > end_date:
                return render(request, "date_selector.html", {"error": "'Start Date' must be before 'End Date'."})

            date_list = get_date_list(start_date, end_date)
            base_path = "/home/abishekkumar/Downloads/Ssm-20250117T102130Z-001/Ssm"

            # Read the data and store it **only once**
            ssm_data = read_date(date_list, base_path, ssm_data)

            if not ssm_data:
                return render(request, "date_selector.html", {"error": "No data loaded for the given date range."})
<<<<<<< HEAD
            i=0
=======
            i=1
>>>>>>> a669fa9 (SSM)
            if i== 0:

                files = list(ssm_data.keys())
                return render(request, "plot_html.html", {
                    "files": files,
                    "start_date": start_date_str,
                    "end_date": end_date_str
                })
            else :
                return redirect(reverse('prop_plot') + f'?start_date={start_date_str}&end_date={end_date_str}')
                

        except ValueError:
            return render(request, "date_selector.html", {"error": "Invalid date format. Use 'YYYY-MM-DD'."})




# View to get columns of a selected http://127.0.0.1:8000/viz_app/file/?start_date=2015-10-17&end_date=2015-11-07file
def get_columns(request):
    file_name = request.GET.get("file_name")
    if not file_name:
        return JsonResponse({'error': 'File name is required'}, status=400)

    try:
        if file_name=="PROP_file":
            columns=['ro_orbit_no', 'stare_seq_no', 'MJD', 'dwell_seq_no', 'SSM_ID', 
 'sum_band_int', 'sum_band_int_uncert', 'sum_band_int_upperlimit_flag', 
 'A_band_int', 'A_band_int_uncert', 'A_band_upperlimit_flag', 
 'B_band_int', 'B_band_int_uncert', 'B_band_upperlimit_flag', 
 'C_band_int', 'C_band_int_uncert', 'C_band_upperlimit_flag', 
 'chi_sq', 'theta_X', 'theta_Y', 'earth_angle', 'exp_time', 
 'hardness_ratio_1', 'hardness_ratio_2', 'bkgnd_rate', 'no_src_FOV', 
 'qual_fac', '_qfac_rserr', '_qfac_errl1', '_qfac_errl2', '_qfac_hk', 
 '_qfac_chisq', '_qfac_thetax', '_qfac_thetay', '_qfac_earthang', 
 '_qfac_exptime', '_qfac_numsrc', 'sum_band_int_uncert_svdfit', 
 'sum_band_int_uncert_imgrms', 'A_band_int_uncert_svdfit', 
 'A_band_int_uncert_imgrms', 'B_band_int_uncert_svdfit', 
 'B_band_int_uncert_imgrms', 'C_band_int_uncert_svdfit', 
 'C_band_int_uncert_imgrms']
            
        else:
            df = ssm_data[file_name]
            columns = df.columns.tolist()
        return JsonResponse({'columns': columns}, status=200)
    except KeyError:
        return JsonResponse({'error': f'File "{file_name}" not found'}, status=404)

# View to generate the plot
class GeneratePlotView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            file_name = data.get("file_name")
            x_axis = data.get("x_axis")
            y_axis = data.get("y_axis")  # Only one Y-axis at a time
            graph_type = data.get("graph_type", "scatter")
            color = data.get("color", "blue")

            if not file_name or not x_axis or not y_axis:
                return JsonResponse({"error": "File name, X-axis, and Y-axis are required."}, status=400)

            # Load data
            df = ssm_data.get(file_name)

            if x_axis not in df.columns or y_axis not in df.columns:
                return JsonResponse({"error": f"Invalid column name: {x_axis} or {y_axis}."}, status=400)

            # Convert data to lists
            x_data = df[x_axis].tolist()
            y_data = df[y_axis].tolist()

            

            # Create Plotly figure
            fig = go.Figure()

            if graph_type == "scatter":
                fig.add_trace(go.Scatter(
                    x=x_data, y=y_data,
                    mode="markers",  # Scatter plot with only markers
                    name=y_axis,
                    marker=dict(size=3, color=color)  # Increased marker size
                ))
            elif graph_type == "bar":
                fig.add_trace(go.Bar(
                    x=x_data, y=y_data, name=y_axis, marker=dict(color=color)
                ))
            elif graph_type == "line":
                fig.add_trace(go.Scatter(
                    x=x_data, y=y_data,
                    mode="lines+markers",  # Line with markers
                    name=y_axis,
                    line=dict(color=color, width=3),  # Make the line thicker
                    marker=dict(size=5, color=color)  # Make points bigger
                ))

            

            # Update layout for better visualization
            fig.update_layout(
                title=f"{y_axis} vs {x_axis}",
                xaxis=dict(title=x_axis, type="linear"),
                yaxis=dict(title=y_axis, type="linear"),
                template="plotly_white",
                height=800, width=1000,
                margin=dict(l=50, r=50, t=50, b=50),
            )

            # Generate Plotly JSON
            plot_json = fig.to_json()

            return JsonResponse({"plot_json": plot_json, "y_axis": y_axis}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class GenerateFITSView(View):
    def get(self, request):
        global ssm_data

        if not ssm_data:
            return JsonResponse({"error": "No data available. Please select a date range first."}, status=400)

        # Get available file names
        files = list(ssm_data.keys())

        return render(request, "fits_creator.html", {
            "files": files
        })
        

    def post(self, request):
        global ssm_data
        if not ssm_data:
            return JsonResponse({"error": "No data available. Please select a date range first."}, status=400)

        try:
            data = json.loads(request.body)
            file_name = data.get("file_name")
            selected_columns = data.get("columns", [])

            if not file_name or not selected_columns:
                return JsonResponse({"error": "File name and at least one column are required."}, status=400)

            df = ssm_data.get(file_name)
            if df is None:
                return JsonResponse({"error": "File not found in the system."}, status=404)

            fits_cols = [fits.Column(name=col, format="E", array=df[col].values) for col in selected_columns]

            hdu = fits.BinTableHDU.from_columns(fits_cols)
            hdul = fits.HDUList([fits.PrimaryHDU(), hdu])

            fits_file_name = f"{file_name}_filtered.fits"
            fits_file_path = os.path.join(settings.MEDIA_ROOT, fits_file_name)
            hdul.writeto(fits_file_path, overwrite=True)

            return JsonResponse({"message": "FITS file created successfully.", "download_url": f"/media/{fits_file_name}"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



# Helper function to generate date list
def get_date_list(start_date, end_date):
    current_date = start_date
    date_list = []
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y%m%d"))  # Date in 'YYYYMMDD' format
        current_date += timedelta(days=1)    
    return date_list

    
    
#to read the date file and call appropriate method
def read_date(date_list,base_path,dataframes):    

    for date in date_list:
        # Step 1: Match folders/files using date pattern (e.g., 20240731_A13_081T01_9000006354)
        date_regex = re.compile(rf'{date}_\w+_\w+_\w+')
        matching_folders = [d for d in os.listdir(base_path) if date_regex.match(d)]
        if not matching_folders:                       
            continue        
        match = re.search(r'_(.*)', matching_folders[0])
        if match:
            extracted_value = match.group(1)
        
        # for level_1  dir handeling
        
        ssm_dirs_level_1 =rf"{base_path}/{matching_folders[0]}/{matching_folders[0]}_level1/SSM"
        # **Find dynamic folder like SSM_47809**
        ssm_path_orb_level_1 = [d for d in os.listdir(ssm_dirs_level_1) if re.match(r'SSM_\d+', d)]
        
        if  ssm_path_orb_level_1:
            
            for orb in ssm_path_orb_level_1:
                match = re.search(r'_(.*)', orb)
                if match:
                    orbit_value = match.group(1)

                lbt_file_path= rf"{ssm_dirs_level_1}/SSM_{orbit_value}/AS1{extracted_value}_{orbit_value}ssm.lbt"
                orb_file_path=rf"{ssm_dirs_level_1}/SSM_{orbit_value}/AS1{extracted_value}_{orbit_value}ssm.orb"
                mkf_file_path=rf"{ssm_dirs_level_1}/SSM_{orbit_value}/AS1{extracted_value}_{orbit_value}ssm_aug.mkf"
                hk_file_path=rf"{ssm_dirs_level_1}/SSM_{orbit_value}/hk/AS1{extracted_value}_{orbit_value}ssmhk_level1.fits"
                tem_file_path=rf"{ssm_dirs_level_1}/SSM_{orbit_value}/tem/AS1{extracted_value}_{orbit_value}ssmtem_level1.fits"
                level1_file_path=rf"{ssm_dirs_level_1}/SSM_{orbit_value}/AS1{extracted_value}_{orbit_value}ssm_level1.fits"
                att_level1_file_path=rf"{ssm_dirs_level_1}/SSM_{orbit_value}/aux/AS1{extracted_value}_{orbit_value}ssm_att_level1.fits"

                dataframes=lbt_file(lbt_file_path,dataframes)
                dataframes=orb_file(orb_file_path,dataframes)
                dataframes=mkf_file(mkf_file_path,dataframes)
                dataframes=level_1_fits(level1_file_path,dataframes)
                dataframes=hk_file(hk_file_path,dataframes)
                dataframes=tem_file(tem_file_path,dataframes) 
                dataframes=att_file_read(att_level1_file_path,dataframes)
        # for level_2   dir handeling
        ssm_dirs_level_2 =rf"{base_path}/{matching_folders[0]}/{matching_folders[0]}_level2/SSM"
        ssm_path_orb_level_2 = [d for d in os.listdir(ssm_dirs_level_2) if re.match(r'SSM_\d+', d)]
        
        if  ssm_path_orb_level_2:            
            for orb in ssm_path_orb_level_2:
                match = re.search(r'_(.*)', orb)
                if match:
                    orbit_value = match.group(1)
                ssm_1_prop_dir_path=rf"{ssm_dirs_level_2}/SSM_{orbit_value}/AS1{extracted_value}_{orbit_value}ssm_prop_ssm1/"
                ssm_2_prop_dir_path=rf"{ssm_dirs_level_2}/SSM_{orbit_value}/AS1{extracted_value}_{orbit_value}ssm_prop_ssm2/"
                ssm_3_prop_dir_path=rf"{ssm_dirs_level_2}/SSM_{orbit_value}/AS1{extracted_value}_{orbit_value}ssm_prop_ssm3/"
                #aug fits
                ssm_1_aug_fits_path=rf"{ssm_dirs_level_2}/SSM_{orbit_value}/evtlstgtifil/AS1{extracted_value}_{orbit_value}ssm_level2_clean_ssm1_aug.fits"
                ssm_2_aug_fits_path=rf"{ssm_dirs_level_2}/SSM_{orbit_value}/evtlstgtifil/AS1{extracted_value}_{orbit_value}ssm_level2_clean_ssm2_aug.fits"
                ssm_3_aug_fits_path=rf"{ssm_dirs_level_2}/SSM_{orbit_value}/evtlstgtifil/AS1{extracted_value}_{orbit_value}ssm_level2_clean_ssm3_aug.fits"
                #stroing the aug data by calling aug_fits_read function for all aug ssm(1,2,3)
                dataframes=aug_fits_read(ssm_1_aug_fits_path,"Level_2_Clean_SSM_1_Aug_fits_file",dataframes)
                dataframes=aug_fits_read(ssm_2_aug_fits_path,"Level_2_Clean_SSM_2_Aug_fits_file",dataframes)
                dataframes=aug_fits_read(ssm_3_aug_fits_path,"Level_2_Clean_SSM_3_Aug_fits_file",dataframes)
                # prop func call for all ssm
                dataframes=prop_ssm_1_files(ssm_1_prop_dir_path,dataframes)
                dataframes=prop_ssm_2_files(ssm_2_prop_dir_path,dataframes)
                dataframes=prop_ssm_3_files(ssm_3_prop_dir_path,dataframes)
    return dataframes
    
    


#level_1 files
def lbt_file(file_path, dataframes):
    dataframes=aug_fits_read(file_path, 'LBT_file', dataframes)
    return dataframes

def orb_file(file_path, dataframes):
    dataframes=aug_fits_read(file_path, 'ORB_file', dataframes)
    return dataframes

def mkf_file(file_path, dataframes):
    dataframes=read_mkf_level1(file_path, 'MKF_file', dataframes)
    return dataframes

def level_1_fits(file_path, dataframes):
    dataframes=aug_fits_read(file_path, 'LEVEL_1_fits_file', dataframes)
    return dataframes

def hk_file(file_path, dataframes):
    dataframes=aug_fits_read(file_path, 'HK_file', dataframes)
    return dataframes

def tem_file(file_path, dataframes):
    dataframes=aug_fits_read(file_path, 'TEMPORAL_file', dataframes)
    return dataframes

def att_file_read(file_path, dataframes):
    try:
        with fits.open(file_path) as hdul:
            for i, df_name in enumerate(["SSM_ATT_POS_STREAM", "SSM_ATT_STARE_SEQ"]):
                if i+1 < len(hdul) and hasattr(hdul[i+1], 'data'):  # Ensure HDU exists and has data
                    df_new = pd.DataFrame(hdul[i+1].data)  # Read FITS data into a DataFrame

                    if df_name in dataframes:
                        dataframes[df_name] = pd.concat([dataframes[df_name], df_new], ignore_index=True)
                    else:
                        dataframes[df_name] = df_new  # First-time assignment
                        
    except Exception as e:
        print(f"Error reading FITS file {file_path}: {e}")

    return dataframes

#prop files handeling

def prop_ssm_1_files(prop_dir,dataframes):
    prop_files_path = [d for d in os.listdir(prop_dir) if re.match(r'SSM1_\d+_\d+_\d+\.prop', d)]
    for prop_file in prop_files_path:
        prop_path=rf"{prop_dir}/{prop_file}"
        read_prop_file(dataframes,"PROP_file_SSM_1",prop_path)
    return dataframes

def prop_ssm_2_files(prop_dir,dataframes):
    prop_files_path = [d for d in os.listdir(prop_dir) if re.match(r'SSM2_\d+_\d+_\d+\.prop', d)]
    for prop_file in prop_files_path:
        prop_path=rf"{prop_dir}/{prop_file}"
        read_prop_file(dataframes,"PROP_file_SSM_2",prop_path)
    return dataframes

def prop_ssm_3_files(prop_dir,dataframes):
    prop_files_path = [d for d in os.listdir(prop_dir) if re.match(r'SSM3_\d+_\d+_\d+\.prop', d)]
    for prop_file in prop_files_path:
        prop_path=rf"{prop_dir}/{prop_file}"
        read_prop_file(dataframes,"PROP_file_SSM_3",prop_path)
    return dataframes


##### file reading in below all files


# method to read the prop file all(ssm(1,2,3))
def read_prop_file(dataframes, prop_file_name, file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return dataframes

    try:
        # Retrieve the existing DataFrame or create a new one if it doesn't exist
        if prop_file_name in dataframes:
            df = dataframes[prop_file_name]
            all_columns = df.columns.tolist()  # Get all columns from existing DF
        else:
            df = pd.DataFrame()
            all_columns = []  # No existing columns initially

        new_row = {}

        # Parse the prop file
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    # Handle missing or invalid values
                    if key in ["alt_name", "src_name", "category"] and value == "-":
                        value = "NaN"
                    elif value == "":
                        value = 0

                    new_row[key] = value

        if new_row:
            # Ensure all expected columns are present with defaults
            for column in all_columns:
                if column not in new_row:
                    if column in ["alt_name", "src_name", "category"]:
                        new_row[column] = "NaN"
                    else:
                        new_row[column] = 0

            # Check for new columns in the current row
            for key in new_row.keys():
                if key not in all_columns:
                    all_columns.append(key)
                    df[key] = "0"  # Add new column with default value

            # Add the new row to the DataFrame
            new_df = pd.DataFrame([new_row])
            if df.empty:
                dataframes[prop_file_name] = new_df
            else:
                dataframes[prop_file_name] = pd.concat([df, new_df], ignore_index=True)            

        else:
            print(f"No valid data found in {file_path}")

    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

    return dataframes

## reading fits file in level1 like(lbt,orb,tem,hk)
def read_mkf_level1(file_path, file_name, dataframes):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return dataframes

    try:
        with fits.open(file_path) as hdul:
            data = hdul[1].data  # Extract HDU 1 data
            
            # Initialize dictionary for DataFrame
            data_dict = {}

            # Process each column
            for colname in data.names:
                coldata = data[colname]

                # Check if the column contains 2D data
                if coldata.ndim == 2:
                    # Flatten each column entry into separate columns
                    for i in range(coldata.shape[1]):
                        new_colname = f"{colname}_{i+1}"  # e.g., Q_SAT_1, Q_SAT_2, Q_SAT_3, Q_SAT_4
                        data_dict[new_colname] = coldata[:, i]
                else:
                    data_dict[colname] = coldata

            # Convert to Pandas DataFrame
            new_df = pd.DataFrame(data_dict)

            # Merge with existing dataframes
            if file_name in dataframes:
                dataframes[file_name] = pd.concat([dataframes[file_name], new_df], ignore_index=True)
            else:
                dataframes[file_name] = new_df            

    except FileNotFoundError:
        print(f"File not found (FITS error): {file_path}")
    except OSError as e:
        print(f"Error opening the file {file_path}: {e}")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
    return dataframes
 
 # reading clean aug fits file all(ssm(1,2,3,))

def aug_fits_read(file_path, file_name, dataframes):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return dataframes  
    

    try:
        # Initialize or retrieve the existing DataFrame for the file
        new_df = dataframes.get(file_name, pd.DataFrame())
        
        with fits.open(file_path) as hdul:
            # Iterate through all extensions in the FITS file
            for i in range(1, len(hdul)):  # Start from extension 1 (skip primary)
                hdu = hdul[i]
                
                if hdu.data is not None:  # Check if the HDU has data                    
                    df = pd.DataFrame(hdu.data)                    
                    # Concatenate the new data with the existing DataFrame
                    new_df = pd.concat([new_df, df], ignore_index=True)
                else:
                    print(f"Extension {i}: {hdu.name} has no data.")     
        
        # Update the dataframes dictionary
        dataframes[file_name] = new_df       
    
    except OSError as e:
        print(f"Error opening the file {file_path}: {e}")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
    
    finally:
        return dataframes

class Prop_Plot(View):
    def get(self, request):
        global ssm_data
        if not ssm_data:
            return JsonResponse({"error": "No data available."}, status=400)

        files = list(ssm_data.keys())  # List available files
        items_to_remove = ["LBT_file", "ORB_file", "PROP_file_SSM_1", "PROP_file_SSM_2", "PROP_file_SSM_3"]
        files = [file for file in files if file not in items_to_remove]
        files.append("PROP_file")
        return render(request, "prop_plot.html", {"files": files})

    def post(self, request):        
        global ssm_data
        try:           
            data = json.loads(request.body)
            selected_files = data.get("files", {})
            source_index=data.get("source_index")
            if not selected_files:
                return JsonResponse({"error": "No files or columns selected"}, status=400)            
            other_files_dict = {}  # Stores all other files
            columns=[]            
            # Iterate and separate files
            for file_name, col in selected_files.items():
                if file_name == "PROP_file":
                   columns.append(col)  # Store PROP_file_SSM separately
                else:
                    other_files_dict[file_name] = col  # Store other files  
            columns.insert(0, "MJD")
            columns=list(columns)
            print(columns)        
            print(other_files_dict)
            
            df1=ssm_data["PROP_file_SSM_1"]
            df2=ssm_data["PROP_file_SSM_2"]
            df3=ssm_data["PROP_file_SSM_3"]
            
            df1['src_index'] = df1['src_index'].astype(int)
            df2['src_index'] = df2['src_index'].astype(int)
            df3['src_index'] = df3['src_index'].astype(int)  # If df3 is relevant
                       
            indexes1 = df1.index[df1['src_index'] == source_index].tolist()
            indexes2 = df2.index[df2['src_index'] == source_index].tolist()
            indexes3 = df3.index[df3['src_index'] == source_index].tolist()
            
            plot_df = pd.DataFrame(columns=['MJD'], dtype=np.float64)            
            row_data = {}
            for df, indexes in zip((df1, df2, df3), (indexes1, indexes2, indexes3)):
                if not  indexes:
                    continue
                for ind in indexes: 
                    
                    stares = int(df["total_obs"].iloc[ind])   # Get total_obs value for index

                    for stare in range(1, stares + 1):
                        for col in columns:
                            print(col)
                            col_name = f'{col}_{stare}'  # Dynamic column name

                            if col_name in df.columns:  # Check if column exists
                                row_data[col_name] = df.at[ind, col_name]  # Store value in dict


                    new_df = pd.DataFrame([row_data])  # Convert dict to DataFrame
                    plot_df = pd.concat([plot_df, new_df], ignore_index=True)  
            for file_name, col in other_files_dict.items():
                for ind, val in enumerate(plot_df['MJD'].values):
                    df = ssm_data[file_name]

                    # Determine the correct MJD column
                    if file_name == "HK_file":
                        mjd_name = "SSM_START_T_MJD"
                    elif file_name == "TEMPORAL_file":
                        mjd_name = "SSM_TEMPO_TIME_MJD"
                    elif file_name == "MKF_file":
                        mjd_name = "MJD"
                    elif file_name in ["LEVEL_1_fits_file", "Level_2_Clean_SSM_1_Aug_fits_file", 
                                       "Level_2_Clean_SSM_2_Aug_fits_file", "Level_2_Clean_SSM_3_Aug_fits_file"]:
                        mjd_name = "SSM_PL_EVTTIME_MJD"
                    elif file_name == "SSM_ATT_POS_STREAM":
                        mjd_name = "TIME"
                    elif file_name == "SSM_ATT_STARE_SEQ":
                        mjd_name = "MID_MJD"

                    # Compute absolute difference
                    df['abs_diff'] = np.abs(df[mjd_name] - val)
                    tolerance = 5e-7  # Adjust this value as needed

                    # Find closest matching row
                    closest_matches = df[df['abs_diff'] <= tolerance]
                    if not closest_matches.empty:
                        closest_value = closest_matches[mjd_name].max()
                        ind_old = closest_matches[mjd_name].idxmax()

                        # Assign values to plot_df
                        for c in col:
                            plot_df.at[ind, c] = df.loc[ind_old, c]
            print(plot_df["MJD"])
                    
                 


        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        
        return JsonResponse({"message": "Data processed successfully", "plot_data": plot_df.to_dict()}, status=200)
