import configparser
import os
import logging

class Config():
    def __init__(self, config_fname='config.ini'):
        if not os.path.exists(config_fname):
            logging.fatal('Failed to find the config file: %s'%(config_fname))
            exit(-1)
        config = configparser.ConfigParser()
        default_config_name = os.path.join(
            os.path.dirname(__file__), 'config_default.ini')
        config.read(default_config_name)
        config.read(config_fname)
        self.build = config['build']
        self.deploy = config['deploy']
        self.project = config['project']
        self.html = config['html']
        self.library = config['library']
        self.colab = config['colab']

        # A bunch of directories
        self.src_dir = self.build['source_dir']
        self.tgt_dir = self.build['output_dir']
        self.eval_dir = os.path.join(self.tgt_dir, 'eval')
        self.rst_dir = os.path.join(self.tgt_dir, 'rst')
        self.html_dir = os.path.join(self.tgt_dir, 'html')
        self.pdf_dir = os.path.join(self.tgt_dir, 'pdf')
        self.colab_dir = os.path.join(self.tgt_dir, 'colab')
        self.linkcheck_dir = os.path.join(self.tgt_dir, 'linkcheck')

        # Some targets names.
        self.pdf_fname = os.path.join(self.pdf_dir, self.project['name']+'.pdf')
        self.tex_fname = os.path.join(self.pdf_dir, self.project['name']+'.tex')
        self.pkg_fname = os.path.join(self.tgt_dir, self.project['name']+'.zip')

        # Sanity checks.
        self.sanity_check()

    def sanity_check(self):
        notebook_patterns = self.build['notebooks'].split()
        for p in notebook_patterns:
            assert p.endswith('md'), '`notebooks` patterns must end with `md`' \
                   ' in `config.init`. Examples: `notebooks = *.md */*.md`.'

        rst_patterns = self.build['rsts'].split()
        for p in rst_patterns:
            assert p.endswith('rst'), '`rsts` patterns must end with `rst`' \
                    ' in `config.init`. Examples: `rsts = index.rst' \
                    ' api/**/*.rst`.'
