import streamlit as st
import pandas as pd
import os


folder_path = "/home/kshitij/stylumia/streamlit-thresholding/data/c-batteries/forward"
folder_path_2 = "/home/kshitij/stylumia/streamlit-thresholding/data/c-batteries/reverse/excels"

def read_data(file_path):
    data = pd.read_excel(file_path)
    data.sort_values(by='match_score_0', inplace=True, ascending=False)
    return data

file_paths = [f"{folder_path}/{file}" for file in os.listdir(folder_path)]
file_paths_2 = [f"{folder_path_2}/{file}" for file in os.listdir(folder_path_2)]
file_paths.extend(file_paths_2)
file_names = [file.split("/")[-1] for file in file_paths]

result = -1
result_dict = {}
visited_files = set()

def main():
    st.title("Thresholding")

    menu = file_names
    choice = st.sidebar.selectbox("Files", menu)
    
    st.write(f"Selected file: {choice}")

    data = read_data(file_paths[menu.index(choice)])
    cols_req = ['lowes_feature_image_s3', 'lowes_cdt','match_score_0','match_feature_image_s3_0','match_cdt_0']
    data = data[cols_req]
    image_cols = ['lowes_feature_image_s3', 'match_feature_image_s3_0']
    data[image_cols] = data[image_cols].apply(lambda x: x.apply(lambda y: f"https://assets.stylumia.com/originals/{y}"))

    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    col1, col2 = st.columns(2)

    col1.image(data.iloc[st.session_state.current_index]['lowes_feature_image_s3'], width=200)
    col1.markdown(f"**CDT:**", unsafe_allow_html=True)
    for key, value in eval(data.iloc[st.session_state.current_index]['lowes_cdt']).items():
        col1.write(f"  - {key}: {value}")

    col2.image(data.iloc[st.session_state.current_index]['match_feature_image_s3_0'], width=200)
    col2.markdown(f"**CDT:**", unsafe_allow_html=True)
    for key, value in eval(data.iloc[st.session_state.current_index]['match_cdt_0']).items():
        col2.write(f"  - {key}: {value}")

    if col1.button("Next"):
        visited_files.add(menu.index(choice)-1)
        st.session_state.current_index += 1
        if st.session_state.current_index >= len(data):
            st.session_state.current_index = 0

    if col2.button("Previous"):
        visited_files.add(menu.index(choice)-1)
        st.session_state.current_index -= 1
        if st.session_state.current_index < 0:
            st.session_state.current_index = len(data)-1

    if st.button("Threshold Product"):
        result = data.iloc[st.session_state.current_index]['match_score_0']
        visited_files.add(menu.index(choice))
        result_dict[choice] = result

    # st.write(f"Visited files: {visited_files}")
    # if len(visited_files) == len(file_names):
    #     st.write("All files visited!")
    #     st.write(result_dict)
    # else:
    #     st.write(f"Files missed: {set(file_names) - visited_files}")

if __name__ == "__main__":
    main()
