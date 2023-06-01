from setuptools import setup, find_packages

setup(
    name='pdf2anki',
    version='0.1.1',
    description='A Python package to create Anki cards from PDFs using OpenAI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Fabio Carvalho',
    author_email='hipnologo@gmail.com',
    url='https://github.com/hipnologo/pdf2anki',
    packages=find_packages(exclude=['pdftoanki']),
    install_requires=[
        'openai>=0.27.0',
        'PyPDF2>=1.26.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'pdf2anki=pdf2anki.main:main',
        ],
    },
)