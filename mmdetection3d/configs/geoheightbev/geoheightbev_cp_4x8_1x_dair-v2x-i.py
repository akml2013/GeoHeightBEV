_base_ = [
    '../_base_/datasets/dair-v2x-i-3d_bev.py',
    '../_base_/schedules/cosine-40e.py',
    '../_base_/default_runtime.py'
]

voxel_size = [0.075, 0.075, 0.1]
pillar_size = [0.075, 0.075, 4]
point_cloud_range = [0, -48, -3, 204, 48, 1]

class_names = ['Pedestrian', 'Cyclist', 'Car']
final_dim=(864, 1536) # HxW
downsample=8
imc = 256
lic = 512

camera_depth_range=[4, 204, 2.0]
height_bound=[-2.0, 0.0, 90]

model = dict(
    type='BEVF_CenterPoint',
    freeze_img=False,
    freeze_pts=False,
    use_pts=False,
    se=True,
    lss=False,

    camera_aligner=True,
    num_ibaf_blocks=3,

    camera_stream=True, 
    grid=0.6, 
    num_views=1,
    final_dim=final_dim,
    downsample=downsample, 
    imc=imc, 
    lic=lic,
    lc_fusion=True,
    pc_range = point_cloud_range,
    img_depth_loss_weight=20,  
    img_depth_loss_method='kld',
    camera_depth_range=camera_depth_range,
    height_bound=height_bound,
    img_backbone=dict(
        type='mmdet.ResNet',
        depth=50,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        norm_cfg=dict(type='BN', requires_grad=False),
        norm_eval=True,
        style='pytorch',
        init_cfg=dict(type='Pretrained', checkpoint='open-mmlab://resnet50_v1c')
        ),
    img_neck=dict(
        type='FPNC',
        final_dim=final_dim,
        downsample=downsample, 
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        outC=imc,
        use_adp=True,
        num_outs=5),

    pts_voxel_layer=dict(
        max_num_points=10,
        voxel_size=voxel_size,
        max_voxels=(120000, 160000),
        point_cloud_range=point_cloud_range),
    pts_pillar_layer=dict(
        max_num_points=20,
        voxel_size=pillar_size,
        max_voxels=(30000, 60000),
        point_cloud_range=point_cloud_range),
    pts_voxel_encoder=dict(
        type='HardSimpleVFE', 
        num_features=5, ),
    pts_middle_encoder=dict(
        type='SparseEncoder',
        in_channels=5,
        sparse_shape=[41, 1280, 2720],
        output_channels=128,
        order=('conv', 'norm', 'act'),
        ),
    pts_backbone=dict(
        type='SECOND',
        in_channels=256,
        out_channels=[128, 256],
        layer_nums=[5, 5],
        layer_strides=[1, 2],
        norm_cfg=dict(type='BN', eps=0.001, momentum=0.01),
        conv_cfg=dict(type='Conv2d', bias=False)),
    pts_neck=dict(
        type='SECONDFPN',
        in_channels=[128, 256],
        out_channels=[256, 256],
        upsample_strides=[1, 2],
        norm_cfg=dict(type='BN', eps=0.001, momentum=0.01),
        upsample_cfg=dict(type='deconv', bias=False),
        use_conv_for_no_stride=True),
    pts_bbox_head=dict(
        type='CenterHeadBEV',
        in_channels=sum([256, 256]),
        tasks=[
            dict(num_class=1, class_names=['Pedestrian']),
            dict(num_class=1, class_names=['Cyclist']),
            dict(num_class=1, class_names=['Car'])
        ],
        common_heads=dict(
            reg=(2, 2), height=(1, 2), dim=(3, 2), rot=(2, 2)),
        share_conv_channel=64,
        bbox_coder=dict(
            type='CenterPointBBoxCoder',
            post_center_range=point_cloud_range,
            max_num=500,
            score_threshold=0.1,
            out_size_factor=8,
            voxel_size=voxel_size[:2],
            pc_range=point_cloud_range[:2],
            code_size=7),
        separate_head=dict(
            type='DCNSeparateHead',
            dcn_config=dict(
                type='DCN',
                in_channels=64,
                out_channels=64,
                kernel_size=3,
                padding=1,
                groups=4),
            init_bias=-2.19,
            final_kernel=3),
        camera_depth_range = camera_depth_range,
        height_bound = height_bound,
        loss_cls=dict(type='mmdet.GaussianFocalLoss', reduction='mean'),
        loss_bbox=dict(type='mmdet.L1Loss', reduction='mean', loss_weight=0.25),
        loss_predict_depth=dict(type='mmdet.FocalLoss', use_sigmoid=True, gamma=2, alpha=0.25, reduction='mean', loss_weight=1.0),
        loss_predict_height=dict(type='mmdet.FocalLoss', use_sigmoid=True, gamma=2, alpha=0.25, reduction='mean', loss_weight=1.0),
        norm_bbox=True),
    train_cfg=dict(
        pts=dict(
            # grid_size=[1360, 1280, 40],
            grid_size=[2720, 1280, 40],
            voxel_size=voxel_size,
            point_cloud_range=point_cloud_range,
            out_size_factor=8,
            dense_reg=1,
            gaussian_overlap=0.1,
            max_objs=500,
            min_radius=2,
            code_weights=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])),
    test_cfg=dict(
        pts=dict(
            post_center_limit_range=point_cloud_range,
            max_per_img=500,
            max_pool_nms=False,
            min_radius=[4, 12, 10, 1, 0.85, 0.175],
            score_threshold=0.1,
            out_size_factor=8,
            voxel_size=voxel_size[:2],
            pc_range=point_cloud_range[:2],
            nms_type='circle',
            pre_max_size=1000,
            post_max_size=83,
            nms_thr=0.2)))

freeze_lidar_components = True
find_unused_parameters = True
no_freeze_head = True

data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,)

resume = False
load_from = None