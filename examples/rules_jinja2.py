import yaml
from jinja2 import Environment, FileSystemLoader

# Define the actual values to substitute
context = {
    'asset_id': 'OPT123456'
}

# Set up the Jinja2 environment and load the YAML template file
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('rules.yaml')

# Render the template with the provided context
rendered_yaml = template.render(context)

# Parse the rendered YAML string into a Python dictionary
rules = yaml.safe_load(rendered_yaml)

print(rules)
