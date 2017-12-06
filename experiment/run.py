import pandas as pd

import sonata
import osm

def main():
    result_sonata = sonata.run(100, 5)
    result_osm = osm.run(100, 5)
    df = pd.DataFrame(result_sonata + result_osm)
    print(df)
    df.to_pickle("sonata_osm_packaging_experiment.pkl")

if __name__ == '__main__':
    main()

