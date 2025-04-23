from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
import os

heading_font_name = "PlayfairDisplay"
heading_font_file_path = "font/PlayfairDisplay-VariableFont_wght.ttf"

normal_font_name = "NunitoSans"
normal_font_file_path = "font/NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf"

def create_quiz_pdf(question, answer, output_filename="auto_quiz.pdf"):
    output_filedir = 'static/result'
    output_filepath = os.path.join( output_filedir, output_filename)

    # Ensure the directory exists
    if not os.path.exists(output_filedir):
        os.makedirs(output_filedir)

    doc = SimpleDocTemplate(output_filepath, pagesize=letter)

    heading_style = ParagraphStyle(
        name="BoldText",
        fontName=heading_font_name,
        fontSize=20,
        alignment=TA_CENTER
    )
    normal_style = ParagraphStyle(
        name="CustomStyle",
        fontName=normal_font_name,
        fontSize=12
    )

    small_heading_style = ParagraphStyle(
        name="CustomStyle",
        fontName=normal_font_name,
        fontSize=13
    )

    story = []

    # Add the main heading
    heading = Paragraph("QUESTIONS AND ANSWERS FROM AUTO QUIZ", heading_style)
    story.append(heading)
    story.append(Spacer(1, 0.5 * inch))  # Add some space after the heading

    # Add the text content
    question_text = Paragraph(question, normal_style)
    
    answer_text = Paragraph(answer, small_heading_style)

    story.append(question_text)
    story.append(Spacer(1, 0.5 * inch))  # Add some space after the heading
    story.append(answer_text)

    doc.build(story)
    print(f"PDF '{output_filename}' created successfully.")

    return output_filepath

def export_to_pdf(generated_questions, file_name):
    pdfmetrics.registerFont(TTFont(heading_font_name, heading_font_file_path))
    pdfmetrics.registerFont(TTFont(normal_font_name, normal_font_file_path))
    question_list = []
    try:
        start_index = generated_questions.index('[')
        end_index = generated_questions.rindex(']')
        list_string = generated_questions[start_index : end_index + 1].lstrip()
        question_list = eval(list_string)
    except Exception as e:
        print("error: " + e)
        print("please try again")

    formatted_question = ""
    answer = "ANSWERS:<br/>"

    for i in range(len(question_list)):
        formatted_question += str(i + 1) + ". " + question_list[i][0]

        formatted_question += "<br/>A. " + question_list[i][1]
        formatted_question += "<br/>B. " + question_list[i][2]
        formatted_question += "<br/>C. " + question_list[i][3]
        formatted_question += "<br/>D. " + question_list[i][4]

        formatted_question += "<br/><br/>"

        answer += str(i + 1) + ". " + question_list[i][5] + "<br/>"

    return create_quiz_pdf(formatted_question, answer, file_name + ".pdf")