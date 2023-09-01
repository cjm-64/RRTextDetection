import json
import os
import pandas as pd

def get_category_token(annotation_df, token, category_df):
    if annotation_df.at[annotation_df.token[annotation_df.sample_data_token == token].index.values.astype(int)[0], 'category_token']:
        cat_id = annotation_df.at[annotation_df.token[annotation_df.sample_data_token == token].index.values.astype(int)[0], 'category_token']
        for cat_token in category_df.token:
            if cat_token == cat_id:
                return category_df.at[category_df.token[category_df.token == cat_id].index.values.astype(int)[0], 'name']
    else:
        return 'No Category'

def get_attribute_token(annotation_df, token, attribute_df):
    if annotation_df.at[annotation_df.token[annotation_df.sample_data_token == token].index.values.astype(int)[0], 'attribute_tokens']:
        attr_id = annotation_df.at[annotation_df.token[annotation_df.sample_data_token == token].index.values.astype(int)[0], 'attribute_tokens']
        for attr_token in attribute_df.token:
            if attr_token == attr_id[0]:
                return attribute_df.at[attribute_df.token[attribute_df.token == attr_token].index.values.astype(int)[0], 'name']
    else:
        return 'No Annotation'

def main():
    json_folder = 'v1.0-mini'
    json_name = 'attribute.json'
    attribute_df = pd.read_json(os.path.join(json_folder, json_name))

    json_name = 'category.json'
    category_df = pd.read_json(os.path.join(json_folder, json_name))

    json_name = 'sample_data.json'
    sd_df = pd.read_json(os.path.join(json_folder, json_name))

    json_name = 'object_ann.json'
    annotation_df = pd.read_json(os.path.join(json_folder, json_name))

    # name = "samples/CAM_BACK_LEFT/n013-2018-08-03-14-44-49+0800__CAM_BACK_LEFT__1533278795447155.jpg"
    # print(name.split("/"))
    #
    # print(sd_df.token[sd_df.token == '003bf191da774ac3b7c47e44075d9cf9'].index.values.astype(int)[0])

    output_data = pd.DataFrame(columns = ['filename', 'sample_data_token', 'category_token','attribute_token'])
    row_count = 0
    for token in sd_df['token']:
        if token in set(annotation_df['sample_data_token']):
            output_data.loc[len(output_data.index)] = [sd_df.at[sd_df.token[sd_df.token == token].index.values.astype(int)[0], 'filename'].split("/")[2],
                                                       token,
                                                       get_category_token(annotation_df, token, category_df),
                                                       get_attribute_token(annotation_df, token, attribute_df)]

    output_data.to_excel('output.xlsx', index=False)





if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
