import pandas as pd
from ripe.atlas.cousteau import Traceroute, AtlasCreateRequest
file_path = "data_health_insurance.xlsx"
df = pd.read_excel(file_path, sheet_name=0)
print(df)