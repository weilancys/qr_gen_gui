from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name = 'qr_gen',
    version = "0.0.1",
    author="lbcoder",
    author_email="lbcoder@hotmail.com",
    description="a simple tool with GUI for generating QR code, for educational purposes.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/weilancys/qr_gen_gui",
    py_modules=['qr_gen', ],
    install_requires = [
        "qrcode[pil]",
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'gui_scripts': [
            'qr_gen = qr_gen:launcher',
        ],
    }
)