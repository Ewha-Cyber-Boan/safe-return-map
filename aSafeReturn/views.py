from django.shortcuts import render
from aSafeReturn.models import *
import json, requests, folium
import os
from pathlib import Path

def index(request):
    return render(request, 'aSafeReturn/start.html')

def markerMap(request):
    return render(request, 'aSafeReturn/markerMap.html')

def findPath(request):
    # 최단경로 좌표데이터 초기화
    s = ShortestL.objects.all()
    s.delete()

    start = request.POST.get("start_point")
    end = request.POST.get("end_point")

    print(start)
    print(end)

    http_header = {
        'x-requested-with': 'XMLHttpRequest'
    }
    session = requests.Session()
    session.headers.update(http_header)

    # 서대문구를 center로 설정하고 검색.
    search_startId_url = 'https://map.naver.com/v5/api/search?caller=pcweb&query=' + start + '&type=all&page=1&displayCount=1&isPlaceRecommendationReplace=true&lang=ko'
    search_endId_url = 'https://map.naver.com/v5/api/search?caller=pcweb&query=' + end + '&type=all&page=1&displayCount=1&isPlaceRecommendationReplace=true&lang=ko'

    r3 = session.get(search_startId_url).text
    r4 = session.get(search_endId_url).text

    r3_json = json.loads(r3)
    r4_json = json.loads(r4)

    startId = r3_json['result']['place']['list'][0]['id']
    endId = r4_json['result']['place']['list'][0]['id']

    start_lat = r3_json['result']['place']['list'][0]['x']
    start_lng = r3_json['result']['place']['list'][0]['y']

    end_lat = r4_json['result']['place']['list'][0]['x']
    end_lng = r4_json['result']['place']['list'][0]['y']

    startl = start_lat + ',' + start_lng
    endl = end_lat + ',' + end_lng

    # 추천 경로 가져오기
    search_findWalk_url_base = 'https://map.naver.com/v5/api/dir/findwalk?'
    query_string = 'lo=ko&r=step&st=1&o=all&l=' + startl + ',' + start + ',' + startId + ';' + endl + ',' + end + ',' + endId + '&lang=ko'

    res = session.get(search_findWalk_url_base + query_string).text
    res_json = json.loads(res)

    steps = res_json['routes'][0]['legs'][0]['steps']

    for step in steps:
        ShortestL.objects.create(latitude=str(step['lat']), longitude=str(step['lng']))

    for i in range(len(steps)): #step.turnDesc
        steps[i]["turnDesc"] = str(i+1)+'. '+steps[i]["turnDesc"]

    latLngs = ShortestL.objects.all().values()

    coordinates = []
    for l in latLngs:
        coordinates.append([float(l['latitude']), float(l['longitude'])])

    ave_lat = sum(p[0] for p in coordinates) / len(coordinates)
    ave_lon = sum(p[1] for p in coordinates) / len(coordinates)

    map = folium.Map(location=[ave_lat, ave_lon],
                     tiles="OpenStreetMap",
                     zoom_start=15
                     )

    for l in latLngs:
        folium.Marker(location=[l['latitude'], l['longitude']], icon=folium.Icon(color='red', icon='flag')).add_to(
            map)

    path = folium.PolyLine(
        locations=coordinates,
        color='red',
        weight=5
    ).add_to(map)

    slat = float(start_lat)
    slng = float(start_lng)
    elat = float(end_lat)
    elng = float(end_lng)

    bigger_lat = slat if slat > elat else elat
    smaller_lat = slat if slat < elat else elat

    bigger_lng = slng if slng > elng else elng
    smaller_lng = slng if slng < elng else elng

    lights = LightL.objects.filter(latitude__gt=smaller_lng).filter(latitude__lt=bigger_lng).filter(longitude__gt=smaller_lat).filter(longitude__lt=bigger_lat)

    for l in lights:
        folium.Marker(location=[l.latitude, l.longitude], icon=folium.Icon(color='green', icon='star')).add_to(map)

    polices = [
        [37.5759828, 126.9240639],
        [37.58300663, 126.9128523],
        [37.56490176, 126.9667851],
        [37.5585522, 126.9430126],
        [37.57025874, 126.9328507],
        [37.562275,	126.9638375],
        [37.583615,	126.936213],
        [37.595257,	126.946388],
        [37.58817887, 126.9445502]
    ]
    for p in polices:
        folium.Marker(location=[p[0], p[1]], icon=folium.Icon(color='blue', icon='star')).add_to(map)

    BASE = Path(__file__).resolve(strict=True).parent.parent
    p = os.path.join(BASE, 'templates', 'aSafeReturn', 'markerMap.html')

    map.save(p)
    return render(request, 'aSafeReturn/map.html',
                  {'steps': steps, 'start_point': start, 'end_point': end})

