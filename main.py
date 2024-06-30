import requests

# 設置 API 
google_maps_api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
ptx_api_key = 'YOUR_PTX_API_KEY'

# Google Maps Directions API
def get_directions(origin, destination, mode):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode={mode}&key={google_maps_api_key}"
    response = requests.get(url)
    return response.json()

# 台鐵費用查詢 (使用PTX平台API)
def get_train_fare(origin_station, destination_station):
    url = f"https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/ODFare/{origin_station}/to/{destination_station}?%24top=30&%24format=JSON"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {ptx_api_key}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# 高鐵費用查詢 (使用PTX平台API)
def get_high_speed_rail_fare(origin_station, destination_station):
    url = f"https://ptx.transportdata.tw/MOTC/v2/Rail/THSR/ODFare/{origin_station}/to/{destination_station}?%24top=30&%24format=JSON"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {ptx_api_key}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# 公車費用查詢 (使用PTX平台API)
def get_bus_fare(route_name, city, origin_stop, destination_stop):
    url = f"https://ptx.transportdata.tw/MOTC/v2/Bus/RouteFare/City/{city}/{route_name}?%24top=30&%24format=JSON"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {ptx_api_key}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# 主程序
origin = "Taipei"
destination = "Kaohsiung"

# Google Maps Directions API 規劃路線
directions = get_directions(origin, destination, "transit")

# 提起路線的交通方式
for leg in directions['routes'][0]['legs']:
    for step in leg['steps']:
        travel_mode = step['travel_mode']
        if travel_mode == 'TRANSIT':
            transit_details = step['transit_details']
            line = transit_details['line']
            vehicle_type = line['vehicle']['type']

            # 處理不同的交通方式
            if vehicle_type == 'TRAIN':
                origin_station = transit_details['departure_stop']['name']
                destination_station = transit_details['arrival_stop']['name']
                train_fare = get_train_fare(origin_station, destination_station)
                print(f"\nTrain Fare from {origin_station} to {destination_station}:")
                print(train_fare)
            
            elif vehicle_type == 'HIGH_SPEED_RAIL':
                origin_station = transit_details['departure_stop']['name']
                destination_station = transit_details['arrival_stop']['name']
                high_speed_rail_fare = get_high_speed_rail_fare(origin_station, destination_station)
                print(f"\nHigh Speed Rail Fare from {origin_station} to {destination_station}:")
                print(high_speed_rail_fare)

            elif vehicle_type == 'BUS':
                route_name = line['short_name']
                city = "Taipei"  # 範例為台北，可以依據實際情況更改
                origin_stop = transit_details['departure_stop']['name']
                destination_stop = transit_details['arrival_stop']['name']
                bus_fare = get_bus_fare(route_name, city, origin_stop, destination_stop)
                print(f"\nBus Fare on route {route_name} from {origin_stop} to {destination_stop}:")
                print(bus_fare)
