from setuptools import setup

package_name = 'turtlebot3_bioinspired_nav'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rajaonsl',
    maintainer_email='lois.rajaonson@grenoble-inp.pro',
    description='Bioinspired navigation model applied to the turtlebot3',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "space_memory_node = turtlebot3_bioinspired_nav.space_memory_node:main"
        ],
    },
)
