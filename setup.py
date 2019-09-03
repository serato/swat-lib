import setuptools
setuptools.setup(
  name = 'serato_swat_lib',         # How you named your package folder (MyLib)
  packages = ['serato_swat_lib'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A small library that includes a test automation runner and utilities',   # Give a short description about your library
  author = 'Benjamin Farrelly',                   # Type in your name
  author_email = 'benjamin.farrelly@serato.com',      # Type in your E-Mail
  url = 'https://github.com/user/serato',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/serato/archive/swat-lib-0.1-alpha.tar.gz',    # I explain this later on
  keywords = ['Serato', 'Test', 'Automation'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7'
  ],
  python_requires='>=3.6',
)