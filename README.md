# SR4RS

An open source tool for super resolution.
You can add your own models, cost functions, feel free to open a PR!

## Cite

http://doi.org/10.5334/jors.369

## Cara Pakai (Automatic Download and Running)

1. Masuk Docker Desktop
2. Buka Terminal
3. Running code ini:
```
docker run -ti --runtime=nvidia mdl4eo/otbtf:3.4.0-gpu bash
```
4. Untuk Download File dari GDrive:
```
python SR4RS_Auto/drive_downloader.py --url 'GANTI URL DISINI' --save 'GANTI NAMA FILE DISINI'.tif
``` 
5. Jalankan Processing
```
python SR4RS_Auto/running_sr4rs.py --load 'MASUKAN NAMA FILE HASIL DOWNLOAD'.tif --saving 'GANTI NAMA FILE OUTPUT'.tif
```

## Catatan
1. File Input haruslah hanya memiliki 4 Band (4,3,2,8)
2. Link GDrive File adalah pada Share-->Copy Link
3. Download File melalui Google Drive adalah bersifat optional, boleh menggunakan file hosting lainnya (bisa menggunakan command 'wget')
4. Resource yang dibutuhkan cukup besar untuk downloading model

## How to use? (Original)

SR4RS needs **OTBTF>=2.3** to work.

### Quick HR image generation using pre-trained model

1. Get the latest OTBTF docker image and enter the docker image.  Here is an example with the otbtf 3.4 gpu image, using NVIDIA runtime:
```
docker run -ti --runtime=nvidia mdl4eo/otbtf:3.4.0-gpu bash
```

2. Download and unzip a pre-trained SavedModel (see [this section](doc/PRETRAINED_MODELS.md) to see available pre-trained models)
```
wget https://nextcloud.inrae.fr/s/boabW9yCjdpLPGX/download/sr4rs_sentinel2_bands4328_france2020_savedmodel.zip
unzip sr4rs_sentinel2_bands4328_france2020_savedmodel.zip
```

3. Clone SR4RS
```
git clone https://github.com/remicres/sr4rs.git
```

4. Use SR4RS to create an HR image (the considered pre-trained model runs on a Sentinel-2 image, 4-channels ordered as Red, Green, Blue, Near infrared). Just download a Sentinel-2 image from ESA hub or elsewhere, then concatenate the bands in this order (for that you can use the OTB application named `otbcli_ConcatenateImages`).
```
python sr4rs/code/sr.py \
--savedmodel sr4rs_sentinel2_bands4328_france2020_savedmodel \
--input /path/to/some/S2_image/stacked_channels_4328_10m.tif \
--output test.tif
```

### Train a model

Here is a summary of the steps to follow.
1. Generate patches images using the `PatchesExtraction` application from OTBTF, from one low-res image (LR) and one high-res image (HR)
2. Run `train.py` on your patches images, and generate a SavedModel
3. Use `sr.py` on LR image using the previously generated SavedModel

For more details, see the [documentation](doc/HOW_TO.md) and check the [pre-trained models](doc/PRETRAINED_MODELS.md).
