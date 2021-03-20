class EdisnFrame:

    __slots__ = ['frame_number', 'frame_bgr', 'frame_rgb',
                 'frame_resized', 'frame_grayscale',
                 'process_start_time', 'process_end_time',
                 'rgb_start_time', 'rgb_end_time',
                 'resize_start_time', 'resize_end_time',
                 'grayscale_start_time', 'grayscale_end_time',
                 'disk_write_start_time', 'disk_write_end_time']
