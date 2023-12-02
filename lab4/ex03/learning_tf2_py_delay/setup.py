import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'learning_tf2_py_delay'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            [f'resource/{package_name}'],
        ),
        (f'share/{package_name}', ['package.xml']),
        (
            os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*launch.[pxy][yma]*')),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sovego',
    maintainer_email='egor.sofronov03@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtle_tf2_broadcaster = learning_tf2_py_delay.turtle_tf2_broadcaster:main',
            'turtle_tf2_listener = learning_tf2_py_delay.turtle_tf2_listener:main',
            'fixed_frame_tf2_broadcaster = learning_tf2_py_delay.fixed_frame_tf2_broadcaster:main',
        ],
    },
)
