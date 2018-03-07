from setuptools import setup, find_packages

def get_readme(filename):
      read_md = open(filename,'rb')
      try:
            import requests
            r = requests.post(url='http://c.docverter.com/convert',
                        data={'to':'rst','from':'markdown'},
                        files={'input_files[]':read_md})
            if r.ok:
                  readme_converted = str(r.content, 'utf-8')
            else:
                  raise Exception
      except:
            print("Warning: could not convert Markdown to RST")
            readme_converted = open(filename,'r').read()
      print(readme_converted)
      return readme_converted

setup(name = 'stannp',
      packages = find_packages(),
      version = '1.0.0',
      description = 'An API wrapper for Stannp, a service for sending snail mail via a web api, such as postcards and letters.',
      long_description = get_readme('README.md'),
      license='GNU',
      author = 'AndyPi',
      author_email = 'info@andypi.co.uk',
      url = 'https://github.com/andy-pi/stannp-api',
      project_urls = {'Author': 'https://andypi.co.uk/',
                      'Stannp API': 'https://www.stannp.com/direct-mail-api',
                      },
      keywords = ['stannp', 'postcard', 'letters', 'api', 'snail mail'],
      classifiers = ['Development Status :: 4 - Beta','Programming Language :: Python :: 3','License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
      install_requires = ['requests'],
      python_requires='>=3',
  
)