import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

import os
def build_report_servico(servico, usuario):

    name = 'assets/reports/servicos/servico_$id.pdf'
    name = name.replace('$id', str(servico.id))

    doc = SimpleDocTemplate('app/'+name, pagesize=letter,
                            rightMargin=20, leftMargin=20,
                            topMargin=20, bottomMargin=20)
    Story = []
    logo = "app/assets/imgs/logo_reports.png"

    text_content = '<font size="11">$message</font>'
    im = Image(logo, 2 * inch, 2 * inch)
    Story.append(im)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    Story.append(Paragraph('', styles["Normal"]))
    Story.append(Spacer(1, 6))
    Story.append(Paragraph(text_content.replace('$message', 'Cliente: '+servico.cliente.nome), styles["Normal"]))
    Story.append(Spacer(1, 6))
    Story.append(Paragraph(text_content.replace('$message', 'Gerado por: '+usuario.nome), styles["Normal"]))

    Story.append(Spacer(1, 15))

    Story.append(Paragraph('<font size="13">Serviço</font>', styles["Normal"]))
    Story.append(Spacer(1, 12))
    Story.append(Paragraph(    text_content.replace('$message', servico.descricao), styles["Normal"]))
    Story.append(Spacer(1, 24))

    Story.append(Paragraph('<font size="13">Observação</font>', styles["Normal"]))
    Story.append(Spacer(1, 12))
    Story.append(Paragraph(text_content.replace('$message', servico.observacao), styles["Normal"]))

    Story.append(Spacer(1, 24))
    Story.append(Paragraph('<font size="13">Materiais a serem utilizados</font>', styles["Normal"]))
    Story.append(Spacer(1, 12))
    Story.append(Paragraph(text_content.replace('$message', servico.materiais_utilizados), styles["Normal"]))
    Story.append(Spacer(1, 48))
    Story.append(Paragraph('<center><font size="11" >contato@rrestofados.com</font></center>', styles["Normal"]))

    doc.build(Story)

    return name
