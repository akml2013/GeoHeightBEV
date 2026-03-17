# Installation Guide

## Environment Requirements

This project is designed to run on **Linux systems only**.

---

## Install MMDetection3D

First, install the MMDetection3D framework:

```bash
# Clone the MMDetection3D repository
git clone https://github.com/open-mmlab/mmdetection3d.git
cd mmdetection3d

# Install MMDetection3D in development mode
pip install -v -e .
```

---

## Prepare DAIR-V2X-I Dataset

First, download the DAIR-V2X-I dataset from the official repository:

- [DAIR-V2X Dataset](https://github.com/AIR-THU/DAIR-V2X)

After downloading, convert the DAIR-V2X-I dataset to KITTI format using the following steps:

### Step 1: Convert DAIR-V2X-I to KITTI format

```bash
python tools/dataset_converter/dair2kitti.py \
    --source-root /path/to/DAIR-V2X-I \
    --target-root /path/to/converted-DAIR-V2X-I \
    --split-path data/split_datas/single-infrastructure-split-data.json \
    --label-type camera \
    --sensor-view infrastructure
```

Replace `/path/to/DAIR-V2X-I` with your actual DAIR-V2X-I dataset path.

### Step 2: Create symbolic link

```bash
ln -s /path/to/converted-DAIR-V2X-I mmdetection3d/data/single-infrastructure-side
```

### Step 3: Create data info files

```bash
python tools/create_data.py kitti \
    --kitti-type dair-v2x-i \
    --root-path ./data/single-infrastructure-side \
    --out-dir ./data/single-infrastructure-side \
    --extra-tag kitti
```

---

## Inference

Run inference using the following command:

```bash
tools/dist_test.sh \
    configs/geoheightbev/geoheightbev_cp_4x8_1x_dair-v2x-i.py \
    checkpoints/geoheightbev_cp_4x8_1x_dair-v2x-i/geoheightbev_dair-v2x-i.pth
```

---

## Notes

- Make sure you have CUDA installed and properly configured on your Linux system.
- Adjust the paths according to your actual directory structure.
- For detailed information about MMDetection3D, please refer to the [official documentation](https://mmdetection3d.readthedocs.io/).
