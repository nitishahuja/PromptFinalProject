import graphviz
import openai
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import random

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_steps_from_abstract(abstract: str) -> list[str]:
    prompt = f"""
You are a technical writer who creates process diagrams.

From the following abstract or methodology section, extract the key steps in the research process as a numbered list.

Text:
\"\"\"{abstract}\"\"\"
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    steps_text = response.choices[0].message.content
    steps = [line for line in steps_text.split("\n") if line.strip() and any(char.isdigit() for char in line)]
    return steps


def generate_flowchart(steps: list[str], filename="outputs/flowchart", format="png"):
    dot = graphviz.Digraph(format=format)
    for i, step in enumerate(steps):
        dot.node(str(i), step)
        if i > 0:
            dot.edge(str(i - 1), str(i))
    output_path = dot.render(filename=filename, cleanup=True)
    print(f"✅ Flowchart saved to {output_path}")
    return output_path


# 🧠 Generate a flowchart directly from a section title and content
def generate_flowchart_from_section(title: str, section_text: str, filename: str = "outputs/flowchart") -> str:
    print(f"🧠 Generating flowchart for: {title}")
    steps = extract_steps_from_abstract(section_text)
    return generate_flowchart(steps, filename=filename)


# 🧠 NEW: Decide how to visualize a section
def determine_visualization_strategy(section_title: str, section_text: str) -> str:
    """Return the best visualization type based on the section title."""
    title = section_title.lower()

    if any(word in title for word in ["method", "approach", "procedure", "design"]):
        return "flowchart"
    elif any(word in title for word in ["result", "findings", "analysis", "evaluation"]):
        return "chart"
    elif any(word in title for word in ["discussion", "conclusion", "limitation", "future work"]):
        return "summary"
    elif any(word in title for word in ["abstract", "introduction", "background"]):
        return "text"
    else:
        return "none"



def generate_chart_from_section(title: str, section_text: str, filename: str = "outputs/chart.png") -> str:
    # Dummy implementation: simulate extracted data
    metrics = {
        "Accuracy": random.uniform(80, 95),
        "Precision": random.uniform(70, 90),
        "Recall": random.uniform(60, 85),
        "F1-Score": random.uniform(65, 88)
    }

    fig, ax = plt.subplots()
    ax.bar(metrics.keys(), metrics.values(), color="skyblue")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Percentage")
    ax.set_title(f"Extracted Metrics – {title}")

    output_path = f"{filename}"
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"✅ Chart saved to {output_path}")
    return output_path
