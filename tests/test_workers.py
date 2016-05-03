import rasterio

from rio_color.workers import atmos_worker, color_worker


def test_atmos():
    i = 77
    args = {
        'atmo': 0.03,
        'contrast': 10,
        'bias': 15,
        'out_dtype': 'uint8'}

    with rasterio.open('tests/rgb8.tif') as src:
        ij, window = list(src.block_windows())[i]
        arr = atmos_worker([src], window, ij, args)
        assert arr.dtype == args['out_dtype']
        assert arr.shape == (3, 32, 32)
        assert arr.max() <= 255
        max_uint8 = arr.max()

    with rasterio.open('tests/rgb16.tif') as src:
        ij, window = list(src.block_windows())[i]
        arr = atmos_worker([src], window, ij, args)
        assert arr.dtype == args['out_dtype']
        assert arr.shape == (3, 32, 32)
        assert arr.max() <= 255

    with rasterio.open('tests/rgb8.tif') as src:
        ij, window = list(src.block_windows())[i]
        args['out_dtype'] = 'uint16'
        arr = atmos_worker([src], window, ij, args)
        assert arr.dtype == args['out_dtype']
        assert arr.shape == (3, 32, 32)
        assert arr.max() > max_uint8


def test_color():
    i = 77
    args = {
        'ops_string': 'gamma 3 0.95 gamma 1,2 0.99',
        'out_dtype': 'uint8'}

    with rasterio.open('tests/rgb8.tif') as src:
        ij, window = list(src.block_windows())[i]
        arr = color_worker([src], window, ij, args)
        assert arr.dtype == args['out_dtype']
        assert arr.shape == (3, 32, 32)
        assert arr.max() <= 255
        assert arr.min() >= 0
        max_uint8 = arr.max()

    with rasterio.open('tests/rgb16.tif') as src:
        ij, window = list(src.block_windows())[i]
        arr = color_worker([src], window, ij, args)
        assert arr.dtype == args['out_dtype']
        assert arr.shape == (3, 32, 32)
        assert arr.max() <= 255
        assert arr.min() >= 0

    with rasterio.open('tests/rgb8.tif') as src:
        ij, window = list(src.block_windows())[i]
        args['out_dtype'] = 'uint16'
        arr = color_worker([src], window, ij, args)
        assert arr.dtype == args['out_dtype']
        assert arr.shape == (3, 32, 32)
        assert arr.max() <= 65535
        assert arr.max() > max_uint8
        assert arr.min() >= 0