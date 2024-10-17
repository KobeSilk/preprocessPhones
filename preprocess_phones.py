import numpy as np
import pandas as pd
import streamlit as st
import re

st.title("Phone number cleaner")
phonenumber = st.file_uploader("upload phone numbers",type="csv")
if phonenumber is not None: 
    phonenumber = pd.read_csv(phonenumber)
    column = st.selectbox("Choose column that has phone numbers:",phonenumber.columns,index=None)
    if column is not None:
        df = phonenumber
        df[column] = df[column].astype(str)
        df['mobile_cleaned'] = df[column].apply(lambda x: re.sub(r"[()\[\]{}<>].*?[()\[\]{}<>]|\.|\/|[a-zA-Z]| +", '', str(x)).strip())
        df['mobile_cleaned'] = df['mobile_cleaned'].apply(lambda x: re.sub(r'[^\x20-\x7E]+', '', str(x)))
        df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('32'),'+'+ df.mobile_cleaned,df.mobile_cleaned)
        df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('00'),'+'+ 
        df.mobile_cleaned.str[2:],df.mobile_cleaned)
        df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('0'),'+32'+ 
        df.mobile_cleaned.str[1:],df.mobile_cleaned)
        df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('3'),'+32'+ 
        df.mobile_cleaned.str[1:],df.mobile_cleaned)
        df['mobile_cleaned'] = df['mobile_cleaned'].apply(lambda x: "invalid" if x.count('+') > 1 else x)
        df['mobile_cleaned'] = df['mobile_cleaned'].apply(lambda x: "invalid" if len(str(x)) > 14 else x)
        
        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode("utf-8")
        st.dataframe(df)
        df['mobile_cleaned'] = '="' + df['mobile_cleaned'].astype(str) + '"'
        csv = convert_df(df)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="phones_cleaned.csv",
            mime="text/csv",
        )
else:
    st.error("Please upload a file.")
