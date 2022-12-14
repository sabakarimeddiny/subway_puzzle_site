from genericpath import isfile
import os
import pickle
import numpy as np
import pandas as pd

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry import MultiPolygon
import shapely.wkt
import fiona

def get_coords_from_string(string):
    return np.array(string.split('(')[1].split(')')[0].split(' ')).astype(float)

def get_coord_dist(coords1, coords2):
    return np.sqrt(np.sum((np.array(coords1) - np.array(coords2))**2))

def get_lines_from_note(note):
    note = note.split(',')
    note = [x.strip() for x in note]
    note = [x for x in note if '-all times' in x or len(x)==1]
    note = [x.split('-')[0] for x in note]
    return note

bb = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'nybb.csv'))
boro_borders = {}
for b in range(len(bb)):
    boro = bb.loc[b]['BoroName']
    boro_borders[boro] = shapely.wkt.loads(bb.loc[b]['the_geom'])

def find_boro(point):
    point = Point(point)
    for k, v in boro_borders.items():
        if v.contains(point):
            return k

shpfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'neighborhoods','geo_export_b1478601-ea50-4cad-a3b4-05a503b5f043.shp')
shape = fiona.open(shpfile)

def find_neighborhood(coords):
    point = Point(coords)
    for neighborhood in shape:
        try:
            pg = MultiPolygon([Polygon(x) for x in neighborhood['geometry']['coordinates']])
        except:
            pg = MultiPolygon([Polygon(x[0]) for x in neighborhood['geometry']['coordinates']])
        if pg.contains(point):
            return neighborhood['properties']['ntaname']

class Puzzle:

    def __init__(self):
        if not os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'table.p')):
            self.THRESHOLD = 0.0025
            path_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'subway.csv')
            a = pd.read_csv(path_).drop(columns=['URL','OBJECTID'])
            a['the_geom'] = [get_coords_from_string(x) for x in a['the_geom']]
            # a['LINE'] = [x.split('-') for x in a['LINE'].values]
            a['LINE'] = [get_lines_from_note(x) for x in a['NOTES'].values]
            a['NOTES'] = [x.split(',') for x in a['NOTES'].values]
            indices_to_drop = []

            for i in range(len(a)):
                current_station = a.loc[i]
                nbhd = find_neighborhood(current_station['the_geom'])
                current_station['NAME'] = current_station['NAME'] + ' (' + nbhd + ')'

            for i in range(len(a)):
                if i in indices_to_drop:
                    continue
                try:
                    current_station = a.loc[i]
                except KeyError:
                    continue
                for j in range(len(a)):
                    if j == i or j in indices_to_drop:
                        continue
                    else:
                        try:
                            candidate_station = a.loc[j]
                        except KeyError:
                            continue
                        if current_station['NAME'] == candidate_station['NAME']:
                            if get_coord_dist(current_station['the_geom'],candidate_station['the_geom']) < self.THRESHOLD:
                                [current_station['LINE'].append(x) for x in candidate_station['LINE']]
                                [current_station['NOTES'].append(x) for x in candidate_station['NOTES']]
                                current_station['LINE'] = list(set(current_station['LINE']))
                                current_station['NOTES'] = list(set(current_station['NOTES']))
                                indices_to_drop.append(j)
                            else:
                                candidate_station['NAME'] = candidate_station['NAME'] + '_' 
                # nbhd = find_neighborhood(current_station['the_geom'])
                # current_station['NAME'] = current_station['NAME'] + ' (' + nbhd + ')'

            df = a.drop(indices_to_drop)
            df = df.reset_index().drop('index',axis=1)            

            station_graph = {}
            for i in range(len(df)):
                station = df.loc[i]['NAME']
                # if station in list(station_graph.keys()):
                #     station = station + '_'
                connections = []
                for j in range(len(df)):
                    if j == i:
                        continue
                    else:
                        a_set = set(df.loc[i]['LINE'])
                        b_set = set(df.loc[j]['LINE'])
                        if len(a_set.intersection(b_set)) > 0:
                            connections.append(df.loc[j]['NAME'])
                station_graph[station] = connections

            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'table.p'), "wb") as f:
                pickle.dump(df, f)
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'graph.p'), "wb") as f:
                pickle.dump(station_graph, f)

            self.subway_table = df
            self.station_graph = station_graph
            
        else:
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'table.p'), "rb") as f:
                self.subway_table = pickle.load(f)
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'graph.p'), "rb") as f:
                self.station_graph = pickle.load(f)
    
    def choose_random_stations(self, n = 2):
        return self.subway_table.sample(n)['NAME'].values

    def find_all_paths(self, start, end, path=[]):
        if start in path:
            return []
        path = path + [start]
        if start == end:
            return [path]
        if not start in list(self.station_graph.keys()):
            return []
        paths = []
        for node in self.station_graph[start]:
            if node not in path and len(path) < 4:
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_shortest_paths(self, start, end):
        paths = self.find_all_paths(start, end)
        return [x for x in paths if len(x) == len(min(paths, key=len))]

    def find_common_lines(self, station1, station2):
        return set(list(self.subway_table[self.subway_table['NAME'] == station1]['LINE'].values)[0])\
                    .intersection(set(list(self.subway_table[self.subway_table['NAME'] == station2]['LINE'].values)[0]))

    def find_connecting_lines(self, paths, unique = True):
        line_paths = []
        for path in paths:
            lines = []
            for i in range(len(path)-1):
                lines.append(list(self.find_common_lines(path[i],path[i+1])))
            if lines not in line_paths or not unique:
                line_paths.append(lines)
        return line_paths


    def check_solution(self, answer, solution):
        verify = np.zeros(len(answer))
        for e, i in enumerate(answer):
            if i in set([x for y in np.array(solution)[:,e] for x in y]):
                verify[e] = 1
            for k, j in enumerate(solution[0]):
                if e == k:
                    continue
                else:
                    if i in set([x for y in np.array(solution)[:,k] for x in y]):
                        verify[e] = 0.5
        return verify

    def verify_solution(self, answer, solution):
        if np.shape(solution)[1] != len(answer):
            return False
        for y in range(np.shape(solution)[1]):
            if y == 0:
                verify = np.array([answer[y] in x for x in np.array(solution)[:,y].flatten()])
            else:
                verify = verify & np.array([answer[y] in x for x in np.array(solution)[:,y].flatten()])
        return True in verify