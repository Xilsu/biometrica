from database import Service
from scipy.spatial import distance

import ast
import statistics 

class KNNClassifier():
    def __init__(self, k, probe, threshold):
        self.k = k
        self.threshold = threshold
        
        self.gallery_angles = list()
        self.gallery_distances = list()
        self.gallery_anthropometrics = list()
        
        self.probe = probe
        self.probe_angles = list()
        self.probe_distances = list()
        self.probe_anthropometrics = list()
    
    def get_descriptor(self, key, template):
        temp = ast.literal_eval(template[1])
        
        return (template[0], temp[key])  
    
    def get_templates(self):
        db = Service('biometrica.db')
        
        query = """SELECT employee_id, descriptor 
                    FROM templates"""
                    
        cursor, result = db.select(query)
        
        db.close()
        
        return result
    
    def prepare_gallery(self):
        gallery_templates = self.get_templates()
        
        for temp in gallery_templates:
            self.gallery_angles.append(self.get_descriptor('angles', temp))
            self.gallery_distances.append(self.get_descriptor('distances', temp))
            self.gallery_anthropometrics.append(self.get_descriptor('anthropometrics', temp))
            
    def prepare_probe(self):
        angles = ast.literal_eval(self.probe)['angles']
        
        for j in range(0, len(angles)):
            self.probe_angles += angles[j]
        
        distances = ast.literal_eval(self.probe)['distances']
        
        for j in range(0, len(distances)):
            self.probe_distances += distances[j]
        
        anthropometrics = ast.literal_eval(self.probe)['anthropometrics']
        
        for j in range(0, len(anthropometrics)):
            self.probe_anthropometrics += anthropometrics[j]
    
    def classify(self):
        self.prepare_gallery()
        self.prepare_probe()
        
        nearest = list()
        
        for i in range(len(self.gallery_angles)):
            label = self.gallery_angles[i][0]
            
            angles = list()
            distances = list()
            anthropometrics = list()
            
            for j in range(0, len(self.gallery_angles[i][1])):
                angles += self.gallery_angles[i][1][j]
            
            for j in range(0, len(self.gallery_distances[i][1])):
                distances += self.gallery_distances[i][1][j]
            
            for j in range(0, len(self.gallery_anthropometrics[i][1])):
                anthropometrics += self.gallery_anthropometrics[i][1][j]
            
            distance_angles = distance.euclidean(self.probe_angles, angles)
            distance_distances = distance.euclidean(self.probe_distances, distances)
            distance_anthropometrics = distance.euclidean(self.probe_anthropometrics, anthropometrics)
            
            nearest.append((((distance_angles + distance_distances) / 2 + distance_anthropometrics) / 2, label))
        
        nearest = sorted(nearest)
        
        if nearest[0][0] > self.threshold:
            return -1
        
        labels = list()
        
        for rank in nearest[0 : self.k]:
            labels.append(rank[1])
        
        return statistics.mode(labels)