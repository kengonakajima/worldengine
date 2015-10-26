import h5py
from worldengine.version import __version__
from worldengine.biome import biome_name_to_index, biome_index_to_name
from worldengine.world import World, Step
import numpy


def save_world_to_hdf5(world, filename):
    f = h5py.File(filename, libver='latest', mode='w')

    general_grp = f.create_group("general")
    general_grp["worldengine_version"] = __version__
    general_grp["name"] = world.name
    general_grp["width"] = world.width
    general_grp["height"] = world.height

    elevation_grp = f.create_group("elevation")
    elevation_ths_grp = elevation_grp.create_group("thresholds")
    elevation_ths_grp["sea"] = world.elevation['thresholds'][0][1]
    elevation_ths_grp["plain"] = world.elevation['thresholds'][1][1]
    elevation_ths_grp["hill"] = world.elevation['thresholds'][2][1]
    elevation_data = elevation_grp.create_dataset("data", (world.height, world.width), dtype='float')
    for y in range(world.height):
        for x in range(world.width):
            elevation_data[y, x] = world.elevation['data'][y][x]

    plates_data = f.create_dataset("plates", (world.height, world.width), dtype='int')
    for y in range(world.height):
        for x in range(world.width):
            plates_data[y, x] = world.plates[y][x]

    ocean_data = f.create_dataset("ocean", (world.height, world.width), dtype='bool')
    for y in range(world.height):
        for x in range(world.width):
            ocean_data[y, x] = world.ocean[y][x]

    sea_depth_data = f.create_dataset("sea_depth", (world.height, world.width), dtype='float')
    for y in range(world.height):
        for x in range(world.width):
            sea_depth_data[y, x] = world.sea_depth[y][x]

    if hasattr(world, 'biome'):
        biome_data = f.create_dataset("biome", (world.height, world.width), dtype='int')
        for y in range(world.height):
            for x in range(world.width):
                biome_data[y, x] = biome_name_to_index(world.biome[y][x])

    if hasattr(world, 'humidity'):
        humidity_grp = f.create_group("humidity")
        humidity_quantiles_grp = humidity_grp.create_group("quantiles")
        for k in world.humidity['quantiles'].keys():
            humidity_quantiles_grp[k] = world.humidity['quantiles'][k]
        humidity_data = humidity_grp.create_dataset("data", (world.height, world.width), dtype='float')
        for y in range(world.height):
            for x in range(world.width):
                humidity_data[y, x] = world.humidity['data'][y][x]

    if hasattr(world, 'irrigation'):
        irrigation_data = f.create_dataset("irrigation", (world.height, world.width), dtype='float')
        for y in range(world.height):
            for x in range(world.width):
                irrigation_data[y, x] = world.irrigation[y][x]

    if hasattr(world, 'permeability'):
        permeability_grp = f.create_group("permeability")
        permeability_ths_grp = permeability_grp.create_group("thresholds")
        permeability_ths_grp['low'] = world.permeability['thresholds'][0][1]
        permeability_ths_grp['med'] = world.permeability['thresholds'][1][1]
        permeability_data = permeability_grp.create_dataset("data", (world.height, world.width), dtype='float')
        for y in range(world.height):
            for x in range(world.width):
                permeability_data[y, x] = world.permeability['data'][y][x]

    if hasattr(world, 'watermap'):
        watermap_grp = f.create_group("watermap")
        watermap_ths_grp = watermap_grp.create_group("thresholds")
        watermap_ths_grp['creek'] = world.watermap['thresholds']['creek']
        watermap_ths_grp['river'] = world.watermap['thresholds']['river']
        watermap_ths_grp['mainriver'] = world.watermap['thresholds']['main river']
        watermap_data = watermap_grp.create_dataset("data", (world.height, world.width), dtype='float')
        for y in range(world.height):
            for x in range(world.width):
                watermap_data[y, x] = world.watermap['data'][y][x]

    if hasattr(world, 'precipitation'):
        precipitation_grp = f.create_group("precipitation")
        precipitation_ths_grp = precipitation_grp.create_group("thresholds")
        precipitation_ths_grp['low'] = world.precipitation['thresholds'][0][1]
        precipitation_ths_grp['med'] = world.precipitation['thresholds'][1][1]
        precipitation_data = precipitation_grp.create_dataset("data", (world.height, world.width), dtype='float')
        for y in range(world.height):
            for x in range(world.width):
                precipitation_data[y, x] = world.precipitation['data'][y][x]

    if hasattr(world, 'temperature'):
        temperature_grp = f.create_group("temperature")
        temperature_ths_grp = temperature_grp.create_group("thresholds")
        temperature_ths_grp['polar'] = world.temperature['thresholds'][0][1]
        temperature_ths_grp['alpine'] = world.temperature['thresholds'][1][1]
        temperature_ths_grp['boreal'] = world.temperature['thresholds'][2][1]
        temperature_ths_grp['cool'] = world.temperature['thresholds'][3][1]
        temperature_ths_grp['warm'] = world.temperature['thresholds'][4][1]
        temperature_ths_grp['subtropical'] = world.temperature['thresholds'][5][1]
        temperature_data = temperature_grp.create_dataset("data", (world.height, world.width), dtype='float')
        for y in range(world.height):
            for x in range(world.width):
                temperature_data[y, x] = world.temperature['data'][y][x]

    # lake_map and river_map have inverted coordinates
    if hasattr(world, 'lake_map'):
        lake_map_data = f.create_dataset("lake_map", (world.width, world.height), dtype='float')
        for y in range(world.height):
            for x in range(world.width):
                lake_map_data[x, y] = world.lake_map[x][y]

    # lake_map and river_map have inverted coordinates
    if hasattr(world, 'river_map'):
        river_map_data = f.create_dataset("river_map", (world.width, world.height), dtype='float')
        for y in range(world.height):
            for x in range(world.width):
                river_map_data[x, y] = world.river_map[x][y]

    generation_params_grp = f.create_group("generation_params")
    generation_params_grp['seed'] = world.seed
    generation_params_grp['n_plates'] = world.n_plates
    generation_params_grp['ocean_level'] = world.ocean_level
    generation_params_grp['step'] = world.step.name

    f.close()


def _from_hdf5_quantiles(p_quantiles):
    quantiles = {}
    for p_quantile in p_quantiles:
        quantiles[p_quantile.title()] = p_quantiles[p_quantile].value
    return quantiles


def _from_hdf5_matrix_with_quantiles(p_matrix):
    matrix = dict()
    matrix['data'] = p_matrix['data']
    matrix['quantiles'] = _from_hdf5_quantiles(p_matrix['quantiles'])
    return matrix


def load_world_to_hdf5(filename):
    f = h5py.File(filename, libver='latest', mode='r')

    w = World(f['general/name'].value,
              f['general/width'].value,
              f['general/height'].value,
              f['generation_params/seed'].value,
              f['generation_params/n_plates'].value,
              f['generation_params/ocean_level'].value,
              Step.get_by_name(f['generation_params/step'].value))

    # Elevation
    e = numpy.array(f['elevation/data'])
    e_th = [('sea', f['elevation/thresholds/sea'].value),
            ('plain', f['elevation/thresholds/plain'].value),
            ('hill', f['elevation/thresholds/hill'].value),
            ('mountain', None)]
    w.set_elevation(e, e_th)

    # Plates
    w.set_plates(numpy.array(f['plates']))

    # Ocean
    w.set_ocean(numpy.array(f['ocean']))
    w.sea_depth = numpy.array(f['sea_depth'])

    # Biome
    if 'biome' in f.keys():
        biome_data = []
        for y in range(w.height):
            row = []
            for x in range(w.width):
                value = f['biome'][y, x]
                row.append(biome_index_to_name(value))
            biome_data.append(row)
        biome = numpy.array(biome_data, dtype=object)
        w.set_biome(biome)

    # Humidity
    # FIXME: use setters
    if 'humidity' in f.keys():
        w.humidity = _from_hdf5_matrix_with_quantiles(f['humidity'])
        w.humidity['data'] = numpy.array(w.humidity['data']) # numpy conversion

    if 'irrigation' in f.keys():
        w.irrigation = numpy.array(f['irrigation'])

    if 'permeability' in f.keys():
        p = numpy.array(f['permeability/data'])
        p_th = [
            ('low', f['permeability/thresholds/low'].value),
            ('med', f['permeability/thresholds/med'].value),
            ('hig', None)
        ]
        w.set_permeability(p, p_th)

    if 'watermap' in f.keys():
        w.watermap = dict()
        w.watermap['data'] = numpy.array(f['watermap/data'])
        w.watermap['thresholds'] = {}
        w.watermap['thresholds']['creek'] = f['watermap/thresholds/creek'].value
        w.watermap['thresholds']['river'] =  f['watermap/thresholds/river'].value
        w.watermap['thresholds']['main river'] =  f['watermap/thresholds/mainriver'].value

    if 'precipitation' in f.keys():
        p = numpy.array(f['precipitation/data'])
        p_th = [
            ('low', f['precipitation/thresholds/low'].value),
            ('med', f['precipitation/thresholds/med'].value),
            ('hig', None)
        ]
        w.set_precipitation(p, p_th)

    if 'temperature' in f.keys():
        t = numpy.array(f['temperature/data'])
        t_th = [
            ('polar', f['temperature/thresholds/polar'].value),
            ('alpine', f['temperature/thresholds/alpine'].value),
            ('boreal', f['temperature/thresholds/boreal'].value),
            ('cool', f['temperature/thresholds/cool'].value),
            ('warm', f['temperature/thresholds/warm'].value),
            ('subtropical', f['temperature/thresholds/subtropical'].value),
            ('tropical', None)
        ]
        w.set_temperature(t, t_th)

    if 'lake_map' in f.keys():
        m = numpy.array(f['lake_map'])
        w.set_lakemap(m)

    if 'river_map' in f.keys():
        m = numpy.array(f['river_map'])
        w.set_rivermap(m)

    f.close()

    return w