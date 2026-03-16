# This schedule is mainly used by models with dynamic voxelization
# optimizer
#lr = 0.003  # max learning rate
lr = 2e-4   # max learning rate
epochs = 50
val_interval = 5
optim_wrapper = dict(
    type='OptimWrapper',
    optimizer=dict(
        type='AdamW', lr=lr, weight_decay=0.01, betas=(0.95, 0.99)),
    clip_grad=dict(max_norm=0.1, norm_type=2),
)

param_scheduler = [
    dict(type='LinearLR', start_factor=0.1, by_epoch=False, begin=0, end=1000),
    dict(
        type='CosineAnnealingLR',
        begin=0,
        T_max=epochs,
        end=epochs,
        by_epoch=True,
        eta_min=lr * 1e-4)
]
# training schedule for 1x
train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=epochs, val_interval=val_interval)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')

# Default setting for scaling LR automatically
#   - `enable` means enable scaling LR automatically
#       or not by default.
#   - `base_batch_size` = (8 GPUs) x (2 samples per GPU).
auto_scale_lr = dict(enable=False, base_batch_size=16)
