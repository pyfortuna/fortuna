from fpdf import FPDF
import fortunacommon as fc

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Ashok Leyland", ln=1, align="C")
pdf.image('/home/ec2-user/plutus/smaplot003.png', x=10, y=20, w=200)
pdf.add_page()
pdf.image('/home/ec2-user/plutus/candleplot003.png', x=10, y=20, w=200)
pdf.output('/home/ec2-user/plutus/testpdf.pdf')

fc.sendMail('PDF','test pdf','/home/ec2-user/plutus/testpdf.pdf')
