import yaml
from jinja2 import Template

# Your YAML content as a string with Jinja2 placeholders
yaml_content = """
rules:
  - id: check_option_tenor
    description: "Check if the tenor of any option is below a certain threshold"
    conditions:
      - type: "tenor"
        asset_type: "option"
        comparison: "less_than"
        threshold: 12  # in months
    actions:
      - action_type: "rebalance_option"
        sell:
          asset_id: "{{ asset_id }}"  # Jinja2 placeholder
        buy:
          new_tenor: 60  # in months, specifying a new option to buy
"""

# Define the actual values to substitute
context = {
    'asset_id': 'OPT123456'
}

# Create a Jinja2 Template instance using the string
template = Template(yaml_content)

# Render the template with the provided context
rendered_yaml = template.render(context)

# Parse the rendered YAML string into a Python dictionary
rules = yaml.safe_load(rendered_yaml)

print(rules)
