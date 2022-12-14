import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
import pandas as pd
import numpy as np
import os
import plotly.express as px

#page setting
st.set_page_config(page_title="Simple Data Manipulation",page_icon="📔",layout="wide")


##functions
#upload file
@st.cache(allow_output_mutation=True)
# @st.experimental_memo
def load_file(file,sep):
    file_ext = os.path.splitext(file.name)[1]

    # Can be used wherever a "file-like" object is accepted:

    if file_ext == ".csv":
        df = pd.read_csv(file, sep=sep)

        print(len(df.columns))
    elif file_ext == ".xlsx":
        df = pd.read_excel(file, index_col=0)
       
    return df

#Rename headers
def change_headers(df,headers_needed):

    with st.form(f"{df} rename",clear_on_submit=True):
        "###### Rename headers"
        left,right = st.columns(2)
        
        old_name = left.selectbox("Old name",headers_needed)
        new_name = right.text_input("New name",placeholder="Input")
        
        change_name = st.form_submit_button("Apply change")
        if change_name:
            df.rename(columns={old_name: new_name},inplace=True, errors='raise')

            st.experimental_rerun()
        return df
  
                                            
#sidebar
st.sidebar.header("Upload a file")

uploaded_file = st.sidebar.file_uploader("Choose a file",type=["csv","xlsx"])

# Main body

#About
intro = st.empty()
with intro.container():
    
    """
    # About
    
    This page is made to test my learning about streamlit.
    
    Welcome any comments and suggestions!
    """
    

    st.image("main.jpg",width=300)

#Read data

with st.container():
    
    if uploaded_file is not None:
        
        intro.empty()
        with st.sidebar.expander("Division"):
            header_sep = st.radio("Data columns divided by : ",[",",";"])
        # header_sep = st.sidebar.text_input("Data headers divided by",value=",")
        
        #load_file
        dataframe = load_file(uploaded_file,sep=header_sep)
                                     
        # #Show data
        "## Raw Data" 
        #Show details
        headers, rows,_,_,_ = st.columns(5)
        headers.metric(label="Columns",value=len(dataframe.columns))
        rows.metric(label="Rows",value=len(dataframe))
        
        with st.expander("Show Raw Data",expanded=True):
                
            st.write(dataframe)
         
        # #Result  
        "## Modify Data"
        data_headers = dataframe.columns.to_list()
        headers_needed = st.multiselect("Headers filter (default first 5 columns)",data_headers,default=data_headers[:5])
                
        #Choose the needed columns
        
        filtered_df = dataframe_explorer(dataframe[headers_needed])
      
        with st.expander("Show Modified Data",expanded=True):
            
            headers, rows,_,_,_ = st.columns(5)
            headers.metric(label="Headers",value=len(filtered_df.columns))
            rows.metric(label="Rows",value=len(filtered_df))
            
            st.dataframe(filtered_df, use_container_width=True) 
            
        #     #Rename headers
        #     change_headers(dataframe,headers_needed)
            
        #     # query
        #     with st.form("query",clear_on_submit=False):
        #         query_selected = {} 
        #         data_selection = dataframe  
                
        #         for header in headers_needed:

        #             title = st.multiselect(
        #             f"Select the {header}:",
        #             options=dataframe[header].unique(),
        #             default=dataframe[header].unique())
        #             query_selected[header] = title
                    
        #         query_con = " & ".join(f"{key} == {value}" for key,value in query_selected.items())
        #         add_query = st.form_submit_button("Query")
        #         if add_query:
        #             print(query_con)
        #             data_selection = dataframe.query(query_con)
      
        #Show details
        # "## Result"
        # with st.container():
            
        #     # modified_df = data_selection[headers_needed].query(query_con)
        #     headers, rows,_,_,_ = st.columns(5)
        #     headers.metric(label="Headers",value=len(filtered_df.columns))
        #     rows.metric(label="Rows",value=len(filtered_df))
            
        #     st.write(filtered_df)
            
        #     #Download as excel, json
        #     @st.cache
        #     def convert_df(df):
        #         # IMPORTANT: Cache the conversion to prevent computation on every rerun
        #         return df.to_csv().encode('utf-8')

        #     csv = convert_df(filtered_df)

        #     st.download_button(
        #         label="Download result as CSV",
        #         data=csv,
        #         file_name='modified_df.csv',
        #         mime='text/csv',
        #     )           
        
        with st.expander("Plot Graph - still testing",expanded=False): 
            "## Plot Graph"
            groupby = st.multiselect("Groupby (default=mean)",filtered_df.columns,default=None,key=2)
                
            Agg = st.text_area("Aggregations if any: ",placeholder="e.g.: a:mean,b:sum,c:size")
            
            #Trim the agg input    
            conditions = Agg.strip().split(",")
            
            agg_dict={}
            try:
                for item in conditions:
                    key,value=item.split(":")
                    agg_dict[key.strip()] = value.strip()
                    
            except:
                pass
                
            with st.container():
                
                if len(groupby)==0:
                    graph_df = filtered_df
                else:
                    if len(agg_dict) == 0:
                        graph_df = filtered_df.groupby(groupby, as_index=False).mean(numeric_only=False)
                    else:
                        graph_df = filtered_df.groupby(groupby, as_index=False).agg(agg_dict)
                
                "### Graph Data"
                #Show details
                headers, rows,_,_,_ = st.columns(5)
                headers.metric(label="Columns",value=len(graph_df.columns))
                rows.metric(label="Rows",value=len(graph_df))  
                            
                st.write(graph_df)
                
                #layout setting
                parameter,graph = st.columns([1,3])
                
                #parameters
                graph_list = ["Line Chart","Area Chart","Bar Chart"]
                graph_type = parameter.selectbox("Graph Type",graph_list)

                x_title = parameter.selectbox("x_title",graph_df.columns.to_list())
                y_title = parameter.selectbox("y_title",graph_df.columns.to_list())
                
                
                if graph_type == graph_list[0]:
                    graph.line_chart(graph_df,x=x_title,y=y_title, width=0, height=400)
                elif graph_type == graph_list[1]:
                    graph.area_chart(graph_df,x=x_title,y=y_title, width=0, height=400)
                elif graph_type == graph_list[2]:

                    graph.bar_chart(graph_df,x=x_title,y=y_title, width=0, height=400)
                    
                    # title = f"{x_title} - {y_title} graph"
                    # fig = px.bar(graph_df, x=x_title, y=graph_df[y_title], color=y_title, title=title)
                    # graph.plotly_chart(fig)
            
#footer
with st.container():
    "Made by  &copy;Sam Woo 2023"
