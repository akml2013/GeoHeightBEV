# dataset settings
dataset_type = 'DairV2XIDataset'
data_root = 'data/single-infrastructure-side/'
class_names = ['Pedestrian', 'Cyclist', 'Car']

# point cloud range
point_cloud_range = [0, -48, -3, 204, 48, 1]
height_bound=[-2.0, 0.0, 90]

input_modality = dict(use_lidar=True, use_camera=True)
metainfo = dict(classes=class_names)
img_scale = (1536, 864)
img_norm_cfg = dict(mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)

backend_args = None

test_pipeline = [
    dict(
        type='LoadPointsFromFile',
        coord_type='LIDAR',
        load_dim=4,
        use_dim=4,
        backend_args=backend_args),
    dict(type='LoadImageFromFile', backend_args=backend_args),

    dict(type='MyResize', scale=img_scale, keep_ratio=False),
    dict(type='ImageEnhance', 
            is_train=False,
            ratio_range = [1.0, 0.00],
            roll_range = [0.0, 2.00],
            pitch_range = [0.0, 0.67],
            ida_aug_conf = {
            'final_dim':(img_scale[1], img_scale[0]),
            'H':1080,
            'W':1920,
            'bot_pct_lim': (0.0, 0.0),
            'cams': ['CAM_FRONT'],
            'Ncams': 1,
        }),     
    dict(
        type='RandomLidarDegradationWithFOV',
        prob_clean=1.0,
        prob_sparse=0.0,
        prob_limited_fov=0.0,
        prob_no_lidar=0.0,
        sparse_ratio=0.5,
        fov_angles=[30],
        seed=None
    ),
    
    dict(type='HeightAndGrad', 
        scale_factors=[8], 
        point_cloud_range=point_cloud_range, 
        step=3, 
        lower_bound=height_bound[0], 
        is_train=True
    ), 
     
    dict(
        type='MultiScaleFlipAug3D',
        img_scale=img_scale,
        pts_scale_ratio=1,
        flip=False,
        transforms=[
            # Temporary solution, fix this after refactor the augtest
            dict(type='Resize', scale=0, keep_ratio=True),
            dict(
                type='GlobalRotScaleTrans',
                rot_range=[0, 0],
                scale_ratio_range=[1., 1.],
                translation_std=[0, 0, 0]),
            dict(type='RandomFlip3D'),
            dict(
                type='PointsRangeFilter', point_cloud_range=point_cloud_range),
        ]),
    dict(type='Pack3DDetInputs', 
        keys=[
            'points', 'img', 'gt_bboxes_3d', 'gt_labels_3d', 'gt_bboxes',
            'gt_labels'
        ],
        meta_keys=('img_path', 'ori_shape', 'img_shape', 'lidar2img',
                'depth2img', 'cam2img', 'pad_shape','lidar2cam_mats','lidar2img_mats','cam2img_mats',
                'cam2img_ori','lidar2img_ori',
                'scale_factor', 'flip', 'pcd_horizontal_flip',
                'pcd_vertical_flip', 'box_mode_3d', 'box_type_3d',
                'img_norm_cfg', 'num_pts_feats', 'pcd_trans',
                'sample_idx', 'pcd_scale_factor', 'pcd_rotation',
                'pcd_rotation_angle', 'lidar_path',
                'transformation_3d_flow', 'trans_mat',
                'affine_aug', 'sweep_img_metas', 'ori_cam2img',
                'cam2global', 'crop_offset', 'img_crop_offset',
                'resize_img_shape', 'lidar2cam', 'ori_lidar2img',
                'num_ref_frames', 'num_views', 'ego2global',
                'axis_align_matrix', 'cam_intrinsic',
                'depth','grad_depth','max_depth','max_grad_depth',
                'depth_ori','grad_depth_ori','max_depth_ori','max_grad_depth_ori',
                'height','grad_height','max_height','max_grad_height',
                'height_ori','grad_height_ori','max_height_ori','max_grad_height_ori',
                'sensor2ego_mats', 'intrin_mats', 'ida_mats', 'bda_mat',
                'sensor2sensor_mats', 'sensor2virtual_mats', 'reference_heights'
                ))
]

val_dataloader = dict(
    batch_size=1,
    num_workers=1,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        data_prefix=dict(
            pts='training/velodyne_reduced', img='training/image_2'
        ),
        ann_file='kitti_infos_val.pkl',
        pipeline=test_pipeline,
        modality=input_modality,
        test_mode=True,
        metainfo=metainfo,
        box_type_3d='LiDAR',
        backend_args=backend_args))
test_dataloader = val_dataloader

val_evaluator = dict(
    type='KittiMetric', ann_file=data_root+'kitti_infos_val.pkl',pcd_limit_range=point_cloud_range)
test_evaluator = val_evaluator

vis_backends = [dict(type='LocalVisBackend')]
visualizer = dict(
    type='Det3DLocalVisualizer', vis_backends=vis_backends, name='visualizer')