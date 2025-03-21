pip install djangorestframework
dash
potly
static
show columns after data is proseesed
please wait fetching data
please wait ,reading the processing the data for the plot

<<<<<<< HEAD

=======
pip install channels
>>>>>>> a669fa9 (SSM)
python manage.py collectstatic


class Prop_Plot(View):
    def get(self, request):
        global ssm_data
        if not ssm_data:
            return JsonResponse({"error": "No data available."}, status=400)

        files = list(ssm_data.keys())  # List available files
        return render(request, "prop_plot.html", {"files": files})

    def post(self, request):
        pass
        global ssm_data
        try:
            
            data = json.loads(request.body)
            selected_files = data.get("files", {})
            if not selected_files:
                return JsonResponse({"error": "No files or columns selected"}, status=400)
            
            source_index=data.get("source_index")
            df1=ssm_data["PROP_file_SSM_1"]
            df2=ssm_data["PROP_file_SSM_2"]
            df3=ssm_data["PROP_file_SSM_3"]
            prop_col_1=selected_files["PROP_file_SSM_1"]
            prop_col_2=selected_files["PROP_file_SSM_2"]
            prop_col_3=selected_files["PROP_file_SSM_3"]
            columns=selected_files["PROP_file_SSM"]
            prop_col=[prop_col_1,prop_col_2,prop_col_3]
            indexes1 = df1.index[df1['src_index'] == source_index].tolist()
            indexes2 = df2.index[df1['src_index'] == source_index].tolist()
            indexes3 = df3.index[df1['src_index'] == source_index].tolist()
            plot_df = pd.DataFrame(columns=['MJD'])
            plot_df = pd.DataFrame(columns=['SSM'])
            plot_df = pd.DataFrame(columns=['MJD'])
            for df,indexes in zip((df1,df2,df3),(indexes1,indexes2,indexes3)):
                for ind in indexes: 
                    
                    
                        stares=df["total_obs"].iloc[ind]
                        for stare in range (1,stares+1):
                            plot_df['MJD']=df[f'MJD_{stare}']
                            if prop_col_1:
                                for col in prop_col_1:
                                    if plot_df["MJD"]== df1[]:
                                        plot_df[f'{col}_S1']=df1[f'{col}_{stare}']
                            if prop_col_2:
                                for col in prop_col_2:
                                    plot_df[f'{col}_S2']=df2[f'{col}_{stare}']
            
            for df,indexes in zip((df1,df2,df3),(indexes1,indexes2,indexes3)):
                
                for ind in indexes: 
                    
                    
                        stares=df["total_obs"].iloc[ind]
                        for stare in range (1,stares+1):
                            for col in columns                            
                                plot_df['MJD']=df[f'MJD_{stare}']
                            
                      
            


        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        
<<<<<<< HEAD
        return
=======
        return
>>>>>>> a669fa9 (SSM)
