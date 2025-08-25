import json
import os

# Load registry
with open('avot_registry.json') as f:
    registry = json.load(f)

# Output folder
output_folder = "generated_scrolls"
os.makedirs(output_folder, exist_ok=True)

# Load templates
template_dir = "scroll_templates"

for avot in registry["avots"]:
    name = avot["name"]
    topic = avot["scroll_topic"]
    template_path = os.path.join(template_dir, topic + ".txt")

    if os.path.exists(template_path):
        with open(template_path) as t:
            template = t.read()

        # Replace placeholder values
        scroll_content = template.replace("{{AVOT_NAME}}", name).replace("{{SCROLL_TOPIC}}", topic)

        # Write to output
        output_path = os.path.join(output_folder, f"{name}_{topic}_scroll.txt")
        with open(output_path, "w") as out:
            out.write(scroll_content)