from flask import Flask, request, send_file, jsonify
import subprocess
from flask_cors import CORS
import os

from jinja2 import Template

app = Flask(__name__)
CORS(app)

LATEX_TEMPLATE = r"""
\documentclass[10pt, letterpaper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{hyperref}
\begin{document}
\title{Resume: {{ name }}}
\author{}
\date{}
\maketitle

\section*{Contact Information}
Email: \href{mailto:{{ email }}}{{ email }} \\
Location: {{ location }} \\
Phone: {{ phone }} \\
Website: \href{ {{ website }} }{ {{ website }} } \\
LinkedIn: \href{ https://linkedin.com/in/{{ linkedin }} }{ {{ linkedin }} } \\
GitHub: \href{ https://github.com/{{ github }} }{ {{ github }} }

\section*{Education}
{{ education }}

\section*{Work Experience}
{{ work_experience }}

\section*{Projects}
{{ projects }}

\section*{Achievements}
{{ achievements }}

\end{document}
"""

@app.route('/generate', methods=['POST'])
def generate_resume():
    data = request.json or {}

    #  Create a Jinja2 template
    template = Template(LATEX_TEMPLATE)

    #  Render the template using .render()
    latex_code = template.render(
        name=data.get('name', 'Your Name'),
        email=data.get('email', 'youremail@domain.com'),
        location=data.get('location', 'Your Location'),
        phone=data.get('phone', 'Your Phone Number'),
        website=data.get('website', 'yourwebsite.com'),
        linkedin=data.get('linkedin', 'yourlinkedinprofile'),
        github=data.get('github', 'yourgithubprofile'),
        education=data.get('education', 'Your Education Details'),
        work_experience=data.get('workExperience', 'Your Work Experience Details'),
        projects=data.get('projects', 'Your Projects Details'),
        achievements=data.get('achievements', 'Your Achievements Details'),
    )

    # Write LaTeX code to a temporary .tex file
    tex_file = 'resume.tex'
    with open(tex_file, 'w') as f:
        f.write(latex_code)

    # Compile LaTeX to PDF
    try:
        subprocess.run(['pdflatex', tex_file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "LaTeX compilation failed.", "details": str(e)}), 500

    # Send the generated PDF file
    pdf_file = 'resume.pdf'
    return send_file(pdf_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
