import pandas as pd
import folium

# 1. Load structured dataset
df = pd.read_csv("locations_data.csv")

# 2. Initialize interactive base map
m = folium.Map(
    location=[6.0000, 6.9000],
    zoom_start=10,
    tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    attr='OpenTopoMap'
)

# 3. Create narrative layer groups
part1_layer = folium.FeatureGroup(name="Part 1: Traditional Igbo Space").add_to(m)
part2_layer = folium.FeatureGroup(name="Part 2: Exile in Mbanta").add_to(m)
part3_layer = folium.FeatureGroup(name="Part 3: Colonial Encounter & Collapse").add_to(m)

# 4. Add markers dynamically from CSV data with layer organization
for index, row in df.iterrows():
    # Assign markers to appropriate layers based on the row's 'part' column
    part_str = str(row.get('part', 'Part 1'))
    if "Part 2" in part_str:
        target_layer = part2_layer
    elif "Part 3" in part_str:
        target_layer = part3_layer
    else:
        target_layer = part1_layer

    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"<b>{row['location_name']}</b><br><b>Category:</b> {row['category']}<br><i>{row.get('quote', '')}</i>",
        icon=folium.Icon(color=row['color'], icon="info-sign")
    ).add_to(target_layer)

# 5. Add layer control toggle panel to the map
folium.LayerControl().add_to(m)
# 5. Add narrative journey path (e.g., Exile Route from Umuofia to Mbanta)
exile_route =[
[6.0159, 6.8667], # Umuofia
[5.8500, 7.0000]  # Mbanta
]
folium.PolyLine(
locations=exile_route,
color="orange",
weight=4,
dash_array="5, 10",
tooltip="Okonkwo's Exile Journey"
).add_to(m)

# 6. Save output map
output_file = "things_fall_apart_map.html"
m.save(output_file)
print(f"Success! Advanced map saved as '{output_file}'.")