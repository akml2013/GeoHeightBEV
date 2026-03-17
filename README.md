# GeoHeightBEV: A Geometric Height Prior Framework for Calibration-Error-Robust BEV Perception

[Dengfeng Liu](https://orcid.org/0000-0002-6193-6641), [Ruize Song](https://orcid.org/0009-0009-0486-3907), [Shanjie Li](https://orcid.org/0009-0000-9150-7621), and [Mai Xu](https://orcid.org/0000-0002-0277-3301), Senior Member, IEEE

## Overview

![alt text](assets/GeoHeightBEV-Structure.png)

## Abstract

With the growing importance of environmental perception for autonomous driving, multimodal roadside 3D perception is key to enhancing accuracy and reliability. Current Bird's-Eye View (BEV) methods, however, face two major limitations: traditional height prediction relies solely on cameras, leading to inherently unstable and non-robust estimates; meanwhile, sensor calibration errors cause feature misalignment in BEV space, degrading fusion performance.

To overcome these issues, we propose GeoHeightBEV, a multimodal roadside BEV perception framework. Its geometry-guided height prediction (GHP) module leverages LiDAR height distribution as a prior to enable camera-LiDAR collaborative prediction. A geometry-aligned dynamic compensation (GDC) module uses multi-scale deformation fields to reverse-map camera features into LiDAR height space, improving calibration robustness. Furthermore, an iterative bidirectional aligned fusion (i-BAF) module applies heterogeneous offset deformable convolution for multi-round alignment, progressively refining residual misalignment during fusion.

Our method achieves state-of-the-art results on the DAIR-V2X-I benchmark, raising vehicle, pedestrian, and cyclist detection mAP by 11.18%, 6.48%, and 9.74%, respectively.

## Incoming

- Currently, only configuration files are released. The complete inference code pipeline will be available soon.

## Installation

For detailed installation instructions, please refer to [INSTALL.md](INSTALL.md).

## Model Checkpoints

Due to GitHub's file size limit, the model checkpoint will be uploaded to an external storage service. Download links will be available soon.

After downloading, place the checkpoint file at:
```
mmdetection3d/checkpoints/geoheightbev_cp_4x8_1x_dair-v2x-i/geoheightbev_dair-v2x-i.pth
```