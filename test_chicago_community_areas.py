import os
import unittest
from chicago_community_areas import (get_neighborhood_for_point,
                                     get_community_area_coords,
                                     download_shapefiles)

import pandas as pd

class TestExampleAreas(unittest.TestCase):
    """Test cases for some example lat, lng coordinates.  Verify that the
    code picks the correct neighborhoods"""

    def setUp(self):

        #If the subdirectory data/ does not exists then fetch down the
        #community boundary shapefiles:
        if not os.path.exists(os.path.join(os.getcwd(), "data")):
            download_shapefiles()

        self.areas = get_community_area_coords()

    def test_example_coords(self):

        #Grant Park
        #https://www.google.com/maps/preview?q=41.8703314,-87.62357420000001
        res = get_neighborhood_for_point(41.8703314, -87.6235742, self.areas)
        self.assertEqual(res, "Grant Park")

        # The city splits the south side of The Loop from the Near South Side
        # along Roosevelt.  Check a point on either side of that road:

        # Loop
        # https://maps.google.com/maps?q=41.8685387,-87.624371
        res = get_neighborhood_for_point(41.8685387,-87.624371, self.areas)
        self.assertEqual(res, "Loop")

        # Near South Side
        # https://maps.google.com/maps?q=41.8672125,-87.6263141
        res = get_neighborhood_for_point(41.8672125, -87.6263141, self.areas)
        self.assertEqual(res, "Near South Side")

        filenames = [
            # foo.csv, ...
        ]

        dataframes = {
            f: pd.read_csv(f).dropna(subset=['Latitude']) for f in filenames
        }

        for name, df in dataframes.iteritems():
            df.insert(0, 'Neighborhood', 'None')

            for index, row in df.iterrows():
                df.loc[index, 'Neighborhood'] = get_neighborhood_for_point(
                    row['Latitude'],
                    row['Longitude'],
                    self.areas
                )
                print("File {}: row {} of {}".format(name, index + 1, len(df)))

            df.to_csv(name)

if __name__ == "__main__":
    unittest.main()
