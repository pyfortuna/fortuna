# Import Libraries
from fpdf import FPDF
import fortunacommon as fc

# Create PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.write(5, 'Ashok Leyland')
lMargin=10
imgW=pdf.w - (2*lMargin)
img1Y=20
img2Y=250
pdf.image('/home/ec2-user/plutus/smaplot003.png', x=lMargin, y=img1Y, w=imgW)
pdf.image('/home/ec2-user/plutus/candleplot003.png', x=lMargin, y=img2Y, w=imgW)
pdf.output('/home/ec2-user/plutus/testpdf.pdf')

# Send Mail
fc.sendMail('PDF','test pdf','/home/ec2-user/plutus/testpdf.pdf')
