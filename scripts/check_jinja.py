from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
import sys

templates_path = r'c:\Users\Denzel\OneDrive\Task 1 2022\templates'
env = Environment(loader=FileSystemLoader(templates_path))
try:
    env.get_template('index.html')
    print('Template compiled OK')
except TemplateSyntaxError as e:
    print('TemplateSyntaxError:', e)
    sys.exit(1)
except Exception as e:
    print('Other error:', e)
    sys.exit(2)
