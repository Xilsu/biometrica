from database import Service

import pandas as pd

class Logs():
    def get_logs(self):
        db = Service('biometrica.db')
        
        query = """SELECT logs.datetime, employees.name, roles.role, logs.authorized, employees.avatar 
                    FROM employees
                    LEFT JOIN logs ON employees.id = logs.employee_id
                    LEFT JOIN roles ON employees.role_id = roles.id 
                    ORDER BY logs.datetime"""
                    
        cursor, info = db.select(query)
        
        db.close()
        
        columns_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(info, columns=columns_names)
        
        return df