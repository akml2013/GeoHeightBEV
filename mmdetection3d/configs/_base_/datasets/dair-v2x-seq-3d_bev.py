# dataset settings
dataset_type = 'DairV2XIDataset'
data_root = 'data/single-infrastructure-side-seq-example/'
# data_root = 'data/single-infrastructure-side/'
# data_root = 'data/single-infrastructure-side-seq/'
class_names = ['Pedestrian', 'Cyclist', 'Car']
# class_names = ['Car', 'Truck', 'Van', 'Bus', 'Cyclist', 'Motorcyclist','Pedestrian']
# class_names = ['Car', 'Truck', 'Van', 'Bus', 'Cyclist', 'Tricyclist', 'Motorcyclist','Barrowlist', 'Pedestrian', 'Trafficcone']

# point_cloud_range = [0, -70.4, -3, 204.8, 70.4, 1]
# point_cloud_range = [0, -45.2, -3, 102.4, 45.2, 1]
point_cloud_range = [0, -48, -3, 204, 48, 1]
height_bound=[-2.0, 0.0, 90]

input_modality = dict(use_lidar=True, use_camera=True)
metainfo = dict(classes=class_names)
# img_scale = (1024, 768)
img_scale = (1536, 864)
img_norm_cfg = dict(mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)

# Example to use different file client
# Method 1: simply set the data root and let the file I/O module
# automatically infer from prefix (not support LMDB and Memcache yet)

# data_root = 's3://openmmlab/datasets/detection3d/kitti/'

# Method 2: Use backend_args, file_client_args in versions before 1.1.0
# backend_args = dict(
#     backend='petrel',
#     path_mapping=dict({
#         './data/': 's3://openmmlab/datasets/detection3d/',
#          'data/': 's3://openmmlab/datasets/detection3d/'
#      }))
backend_args = None

train_pipeline = [
    dict(
        type='LoadPointsFromFile',
        coord_type='LIDAR',
        load_dim=4,
        use_dim=4,
        backend_args=backend_args),
    dict(type='LoadImageFromFile', backend_args=backend_args),
    dict(type='LoadAnnotations3D', with_bbox_3d=True, with_label_3d=True),

    # dict(
    # type='RandomResize',
    # scale=img_scale,  # (W, H) 目标尺寸
    # # scale=(800, 450),  # (W, H) 目标尺寸
    # ratio_range=(1.0, 1.0),  # 固定宽高比
    # keep_ratio=False),  # 不保持原图比例

    # dict(type='MyResize', scale=img_scale, keep_ratio=False),
    # dict(
    #     type="GlobalRotScaleTrans",
    #     rot_range=[-0.78539816, 0.78539816],
    #     scale_ratio_range=[0.95, 1.05],
    #     translation_std=[0.2, 0.2, 0.2],
    # ),
    # dict(type="RandomFlip3D", 
    #      flip_ratio_bev_horizontal=0.5,
    #      flip_ratio_bev_vertical=0.0      # 关闭垂直翻转
    # ),

    dict(type='MyResize', scale=img_scale, keep_ratio=False),

    dict(
        type='OurGlobalRotScaleTrans',
        rot_range=[-0.3925 * 2, 0.3925 * 2],
        scale_ratio_range=[0.95, 1.05],
        translation_std=[0.2, 0.2, 0.2],
    ),
    dict(
        type='OurRandomFlip3D',
        sync_2d=False,
        flip_ratio_bev_horizontal=0.0,
        flip_ratio_bev_vertical=0.0
    ),

    dict(type='ImageEnhance', 
            is_train=True,
            ratio_range = [1.0, 0.20],
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
    dict(type='ImageOffset', 
            # ratio_range = [1.0, 0.20],
            # roll_range = [0.0, 2.00],
            # pitch_range = [0.0, 0.67]
            ratio_range = [1.0, 0.0],
            roll_range = [0.0, 0.0],
            pitch_range = [0.0, 0.0]
        ),        
    dict(type='ImageDepth', scale_factors=[8], exp_time=0),       
    dict(type='ImageHeight', scale_factors=[8], exp_time=0),   
    dict(type='DepthAndGrad', scale_factors=[8], is_train=True),
    dict(type='HeightAndGrad', scale_factors=[8], point_cloud_range=point_cloud_range, lower_bound=height_bound[0], is_train=True),        

    dict(type='PointsRangeFilter', point_cloud_range=point_cloud_range),
    dict(type='ObjectRangeFilter', point_cloud_range=point_cloud_range),
    dict(type='PointShuffle'),

    dict(
        type='Pack3DDetInputs',
        keys=[
            'points', 'img', 'gt_bboxes_3d', 'gt_labels_3d', 'gt_bboxes',
            'gt_labels'
        ],
        meta_keys=('img_path', 'ori_shape', 'img_shape', 'lidar2img',
        'depth2img', 'cam2img', 'pad_shape','lidar2cam_mats','lidar2img_mats','cam2img_mats',
        'cam2img_ori','lidar2img_ori', "img_edge", 'affine_matrix',
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
        'axis_align_matrix', 'cam_intrinsic','sparse_depth','img_depth',
        'depth','grad_depth','max_depth','max_grad_depth',
        'depth_ori','grad_depth_ori','max_depth_ori','max_grad_depth_ori',
        'height','grad_height','max_height','max_grad_height',
        'height_ori','grad_height_ori','max_height_ori','max_grad_height_ori',
        'sensor2ego_mats', 'intrin_mats', 'ida_mats', 'bda_mat',
        'sensor2sensor_mats', 'sensor2virtual_mats', 'reference_heights'
         ))
]
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
            ratio_range = [1.0, 0.20],
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
    dict(type='ImageOffset', 
            # ratio_range = [1.0, 0.20],
            # roll_range = [0.0, 2.00],
            # pitch_range = [0.0, 0.67]
            ratio_range = [1.0, 0.0],
            roll_range = [0.0, 0.0],
            pitch_range = [0.0, 0.0]
        ),        
    dict(type='ImageDepth', scale_factors=[8], exp_time=0),  
    dict(type='DepthAndGrad', scale_factors=[8], is_train=True),
    dict(type='HeightAndGrad', scale_factors=[8], lower_bound=height_bound[0], is_train=True), 
     
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
    dict(type='Pack3DDetInputs', keys=['points', 'img'],
        meta_keys=('img_path', 'ori_shape', 'img_shape', 'lidar2img',
                'depth2img', 'cam2img', 'pad_shape','lidar2cam_mats','lidar2img_mats','cam2img_mats',
                'cam2img_ori','lidar2img_ori', "img_edge", 'affine_matrix',
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
                'axis_align_matrix', 'cam_intrinsic','sparse_depth','img_depth',
                'depth','grad_depth','max_depth','max_grad_depth',
                'depth_ori','grad_depth_ori','max_depth_ori','max_grad_depth_ori',
                'height','grad_height','max_height','max_grad_height',
                'height_ori','grad_height_ori','max_height_ori','max_grad_height_ori',
                'sensor2ego_mats', 'intrin_mats', 'ida_mats', 'bda_mat',
                'sensor2sensor_mats', 'sensor2virtual_mats', 'reference_heights'
                ))
    # dict(type='Pack3DDetInputs', keys=['points', 'img'],
    #         meta_keys=('img_path', 'ori_shape', 'img_shape', 'lidar2img',
    #                 'depth2img', 'cam2img', 'pad_shape',
    #                 'scale_factor', 'flip', 'pcd_horizontal_flip',
    #                 'pcd_vertical_flip', 'box_mode_3d', 'box_type_3d',
    #                 'img_norm_cfg', 'num_pts_feats', 'pcd_trans',
    #                 'sample_idx', 'pcd_scale_factor', 'pcd_rotation',
    #                 'pcd_rotation_angle', 'lidar_path',
    #                 'transformation_3d_flow', 'trans_mat',
    #                 'affine_aug', 'sweep_img_metas', 'ori_cam2img',
    #                 'cam2global', 'crop_offset', 'img_crop_offset',
    #                 'resize_img_shape', 'lidar2cam', 'ori_lidar2img',
    #                 'num_ref_frames', 'num_views', 'ego2global',
    #                 'axis_align_matrix', 'new_field', 
    #                 'sensor2ego_mats', 'intrin_mats', 'ida_mats', 'bda_mat',
    #                 'sensor2sensor_mats', 'sensor2virtual_mats', 'reference_heights'))
]
# construct a pipeline for data and gt loading in show function
# please keep its loading function consistent with test_pipeline (e.g. client)
# eval_pipeline = [
#     dict(
#         type='LoadPointsFromFile',
#         coord_type='LIDAR',
#         load_dim=4,
#         use_dim=4,
#         backend_args=backend_args),
#     dict(type='Pack3DDetInputs', keys=['points'])
# ]
train_dataloader = dict(
    batch_size=2,
    num_workers=2,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type='RepeatDataset',
        times=2,
        dataset=dict(
            type=dataset_type,
            data_root=data_root,
            ann_file='kitti_infos_train.pkl',
            data_prefix=dict(
                pts='training/velodyne_reduced', img='training/image_2'),
            pipeline=train_pipeline,
            modality=input_modality,
            test_mode=False,
            metainfo=metainfo,
            # we use box_type_3d='LiDAR' in kitti and nuscenes dataset
            # and box_type_3d='Depth' in sunrgbd and scannet dataset.
            box_type_3d='LiDAR',
            backend_args=backend_args)))
val_dataloader = dict(
    batch_size=2,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        data_prefix=dict(
            pts='training/velodyne_reduced', img='training/image_2'),
        ann_file='kitti_infos_val.pkl',
        pipeline=test_pipeline,
        modality=input_modality,
        test_mode=True,
        metainfo=metainfo,
        box_type_3d='LiDAR',
        backend_args=backend_args))
test_dataloader = val_dataloader
# test_dataloader = dict(
#     batch_size=2,
#     num_workers=2,
#     persistent_workers=True,
#     drop_last=False,
#     sampler=dict(type='DefaultSampler', shuffle=False),
#     dataset=dict(
#         type=dataset_type,
#         data_root=data_root,
#         data_prefix=dict(
#             pts='testing/velodyne_reduced', img='testing/image_2'),
#         ann_file='kitti_infos_test.pkl',
#         pipeline=test_pipeline,
#         modality=input_modality,
#         test_mode=True,
#         metainfo=metainfo,
#         box_type_3d='LiDAR',
#         backend_args=backend_args))

val_evaluator = dict(
    type='KittiMetric', ann_file=data_root+'kitti_infos_val.pkl',pcd_limit_range=point_cloud_range)
test_evaluator = val_evaluator
# test_evaluator = dict(
#     type='KittiMetric', ann_file=data_root+'kitti_infos_test.pkl',pcd_limit_range=point_cloud_range)


vis_backends = [dict(type='LocalVisBackend')]
visualizer = dict(
    type='Det3DLocalVisualizer', vis_backends=vis_backends, name='visualizer')

