default_scope = 'mmdet3d'

default_hooks = dict(
    timer=dict(type='IterTimerHook'),
    logger=dict(type='LoggerHook', interval=50),
    param_scheduler=dict(type='ParamSchedulerHook'),
    checkpoint=dict(type='CheckpointHook',     
                    interval=1,          # 每1个epoch保存一次
                    by_epoch=True,       # 按epoch计数
                    save_optimizer=True, # 保存优化器状态（便于恢复训练）
                    out_dir='checkpoints',  # 保存目录
                    max_keep_ckpts=10     # 最多保留5个历史检查点
                    ),
    # checkpoint=dict(type='CheckpointHook',     
    #                 interval=-1
    #                 ),    
    sampler_seed=dict(type='DistSamplerSeedHook'),
    visualization=dict(type='Det3DVisualizationHook'))

env_cfg = dict(
    cudnn_benchmark=False,
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0),
    dist_cfg=dict(backend='nccl'),
)

log_processor = dict(type='LogProcessor', window_size=50, by_epoch=True)

log_level = 'INFO'
load_from = None

# TODO: support auto scaling lr
