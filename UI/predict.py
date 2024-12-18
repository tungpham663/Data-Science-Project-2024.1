import pickle
import numpy as np
import pandas as pd

def loadModel():
    model = pickle.load(open('./trained_model/XGBRegressor.pkl', 'rb'))
    return model

def predict(brand, cpu, cpu_brand_type, cpu_hz, gpu, ram_type, ram, ram_bus, storage, screen_resolution,
            screen_ratio,screen_size, battery, weight):
    ohe = pickle.load(open('./trained_model/ohe.pkl', 'rb'))
    pred_model = loadModel()
    cate_data = {
        "GPU Manufacturer": [gpu],
        "Manufacturer": [brand],
        "RAM Type": [ram_type],
        "CPU": [cpu],
        "Screen Resolution": [screen_resolution],
        "Screen Ratio": [screen_ratio],
        "CPU Brand Modifier": [cpu_brand_type],
    }
    nume_data = {
        "Battery": [float(battery)],
        "Bus (MHz)": [float(ram_bus)],
        "CPU Speed (GHz)": [float(cpu_hz)],
        "RAM (GB)": [float(ram)],
        "Screen Size (inch)": [float(screen_size)],
        "Storage (GB)": [float(storage)],
        "Weight (kg)": [float(weight)],
    }
    cate_data = pd.DataFrame(cate_data)
    nume_data = pd.DataFrame(nume_data)
    cate_data = ohe.transform(cate_data)
    cate_data = pd.DataFrame(cate_data, columns=ohe.get_feature_names_out())
    data = pd.concat([nume_data, cate_data], axis=1)
    
    return round(float(np.exp(pred_model.predict(np.array(data))[0])) / 1_000_000, 3)