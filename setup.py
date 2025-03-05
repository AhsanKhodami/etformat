from setuptools import setup, find_packages

setup(
    name="etformat",
    use_scm_version=True,  # Automatically manage versioning from Git tags
    setup_requires=["setuptools-scm"],  # Required for setuptools-scm versioning
    author="Mohammad Ahsan Khodami",  # Replace with your actual name
    author_email="ahsan.khodami@gmail.com",  # Replace with your actual email
    description="A Python package for eye-tracking data processing",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/etformat",  # Replace with actual GitHub repo URL
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib"
    ],
)
