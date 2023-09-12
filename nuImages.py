import json
import os
import time

import pandas as pd
import math


def get_category_token(annotation_df, token, category_df):
    if annotation_df.at[annotation_df.token[annotation_df.sample_data_token == token].index.values.astype(int)[0], 'category_token']:
        cat_id = annotation_df.at[annotation_df.token[annotation_df.sample_data_token == token].index.values.astype(int)[0], 'category_token']
        for cat_token in category_df.token:
            if cat_token == cat_id:
                return category_df.at[category_df.token[category_df.token == cat_id].index.values.astype(int)[0], 'name']
    else:
        return 'No Category'

def get_BoundingBox_size(BB):
    x_start = BB[0]
    y_start = BB[1]
    x_end = BB[2]
    y_end = BB[3]
    bb_width = x_end-x_start
    bb_height = y_end-y_start
    bb_area = bb_width*bb_height
    return (bb_area/(1600*900))*100

def get_BoundingBox_loc(BB):
    bb_mid_x = ((BB[2]-BB[0])/2)+BB[0]
    bb_mid_y = ((BB[3]-BB[1])/2)+BB[1]

    vertslices = math.floor(900/3)
    horzslices = math.floor(1600/3)

    Col_loc = []
    Row_loc = []
    if bb_mid_x < vertslices:
        # First Column
        Col_loc.append([1, 4, 7])
    elif vertslices < bb_mid_x and bb_mid_x <= vertslices*2:
        # Second Column
        Col_loc.append([2, 5, 8])
    else:
        # Third column
        Col_loc.append([3, 6, 9])

    if bb_mid_y < horzslices:
        # First row
        Row_loc.append([1, 2, 3])
    elif horzslices < bb_mid_y and bb_mid_y <= horzslices*2:
        # Second row
        Row_loc.append([4, 5, 6])
    else:
        # Third Row
        Row_loc.append([7, 8, 9])

    return (list(set(Col_loc[0]).intersection(Row_loc[0]))[0])

def get_bounding_box(annotation_df, token):
    if annotation_df.at[annotation_df.token[annotation_df.sample_data_token == token].index.values.astype(int)[0], 'category_token']:
        bound_box = annotation_df.at[annotation_df.token[annotation_df.sample_data_token == token].index.values.astype(int)[0], 'bbox']
        return bound_box
    else:
        return 'No BB'

def get_attribute_token(annotation_df, token, attribute_df):
    if annotation_df.at[annotation_df.token[annotation_df.sample_data_token == token].index.values.astype(int)[0], 'attribute_tokens']:
        attr_id = annotation_df.at[annotation_df.token[annotation_df.sample_data_token == token].index.values.astype(int)[0], 'attribute_tokens']
        for attr_token in attribute_df.token:
            if attr_token == attr_id[0]:
                return attribute_df.at[attribute_df.token[attribute_df.token == attr_token].index.values.astype(int)[0], 'name']
    else:
        return 'No Annotation'

def main():
    json_folder = 'full\\v1.0-train'
    json_name = 'attribute.json'
    attribute_df = pd.read_json(os.path.join(json_folder, json_name))

    json_name = 'category.json'
    category_df = pd.read_json(os.path.join(json_folder, json_name))

    json_name = 'sample_data.json'
    sd_df = pd.read_json(os.path.join(json_folder, json_name))

    json_name = 'object_ann.json'
    annotation_df = pd.read_json(os.path.join(json_folder, json_name))

    output_data = pd.DataFrame(columns = ['filename', 'sample_data_token', 'category_token', 'bound_box_size', 'bound_box_loc', 'attribute_token'])
    for token in sd_df['token']:
        if token in set(annotation_df['sample_data_token']):
            BB = get_bounding_box(annotation_df, token)
            output_data.loc[len(output_data.index)] = [sd_df.at[sd_df.token[sd_df.token == token].index.values.astype(int)[0], 'filename'].split("/")[2],
                                                       token,
                                                       get_category_token(annotation_df, token, category_df),
                                                       get_BoundingBox_size(BB),
                                                       get_BoundingBox_loc(BB),
                                                       get_attribute_token(annotation_df, token, attribute_df)]

    output_data.to_excel('output.xlsx', index=False)





if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time()-start)
