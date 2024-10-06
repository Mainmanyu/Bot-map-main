import sqlite3
from config import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


class DB_Map():
    def __init__(self, database):
        self.database = database
    
    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.commit()

    def add_city(self,user_id, city_name ):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]  
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1
            else:
                return 0

            
    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT cities.city 
                            FROM users_cities  
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))

            cities = [row[0] for row in cursor.fetchall()]
            return cities


    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT lat, lng
                            FROM cities  
                            WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates

    def create_grapf(self, path, cities):
        ax = plt.оси(проекция=ccr.Mollweide())
        ax.stock_img()
        for city in cities:
            coordinates = self.get_coordinates(city)

        if coordinates:
            lat, lng = coordinates

            plt.plot([lat],[lng], color="b", marker=",",transform=ccrs.Geodetic())

            plt.savefig(path)

            plt.close()

    def draw_distance(self, city1, city2):
        
        city1_lon, city1_lat = -75, 43
        city2_lon, city2_lat = 77.23, 28.61

        plt.plot([city1_lon, city2_lon], [city1_lat, city2_lat],
            color='gray', linestyle='--',
            transform=ccrs.PlateCarree(),  
            )
        
        plt.text(city1_lon - 3, city1_lat - 12, 'New York',
            horizontalalignment='right',  
            transform=ccrs.Geodetic()  
            )
        
        plt.text(city2_lon + 3, city2_lat - 12, 'Delhi',
            horizontalalignment='left',  
            transform=ccrs.Geodetic()  
            )

        plt.show()

        pass


if __name__=="__main__":
    
    m = DB_Map(DATABASE)
    m.create_user_table()
