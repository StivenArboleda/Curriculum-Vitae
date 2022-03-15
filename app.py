from flask import Flask, render_template,request,send_file
from mailmerge import MailMerge
import aspose.words as aw

app = Flask(__name__)
test = []
path_output_file_dock = './templates/utils/ouput_file_curriculum.docx'
path_output_file_pdf = './templates/utils/ouput_file_curriculum.pdf'
template = './templates/utils/hoja-de-vida-para-editar.docx'


@app.route('/',methods=['POST', 'GET'])
def Index():
    return render_template('index.html')
    

@app.route('/education',methods=['GET','POST'])
def Template():
    if request.method == 'POST':
        
        test = ''
        for key in request.form.keys():
            test = test+key+","+request.form.get(key)+" ;"
        print(test)
        return render_template('education.html',data=test,max=1)

@app.route('/education/<int:ammount>/<string:data>', methods=['GET','POST'])
def ReloadEdu(ammount,data):
    data.replace('%','')
    return render_template('education.html',max=ammount,data=data)

@app.route('/professional/<string:data>',methods=['GET','POST'])
def Send(data):
    if request.method == 'POST':
        data = data.replace('%','')
        for key in request.form.keys():
            data = data+key+","+request.form.get(key)+" ;"
        return render_template('professional.html',max=1,data=data)

@app.route('/professional/<int:ammount>/<string:data>', methods=['GET','POST'])
def ReloadPro(ammount,data):
    data = data.replace('%','')
    return render_template('professional.html',max=ammount,data=data)

@app.route("/download/<string:data>",methods=['GET','POST'])
def Download(data):
    data = data.replace('%','')
    for key in request.form.keys():
        data = data+key+","+request.form.get(key)+" ;"
    
    arrayData = data.split(';')
    dictData = {}
    for tuple in arrayData:
        ky = tuple.split(',')[0]
        value = " "
        if(len(tuple.split(','))>1):
            value = tuple.split(',')[1]
        dictData[ky] = value
    print('=====================================================')
    print(dictData)
    print('=====================================================')
    
    document = MailMerge(template)
    print(document.get_merge_fields())
    document.merge(
        #Perfil
        fullname = dictData['fullname'],
        job = dictData['job'],
        perfil_description = dictData['description'],
        professional_skills = dictData['skills_professional'],
        personal_skills = dictData['skills_personal'],
        telefono = dictData['phone'],
        correo = dictData['email'],
        ciudad_pais = dictData['city'],
    )
    document.merge(
        #Educacion
        titulo_ano_edu1= dictData['carrera0']+"-"+dictData['yearEdu0'],
        ciudad_pais_edu1=dictData['ciudadEdu0']+"-"+dictData['paisEdu0'],
        universidad_edu1=['universidad0'],
        
    )
    if('carrera1'in dictData):
        document.merge(
        #Educacion
        titulo_ano_edu2= dictData['carrera1']+"-"+dictData['yearEdu1'],
        ciudad_pais_edu2=dictData['ciudadEdu1']+"-"+dictData['paisEdu1'],
        universidad_edu2=['universidad1']
        )
    
    if('carrera2' in dictData):
        document.merge(
        #Educacion
        titulo_ano_edu3= dictData['carrera2']+"-"+dictData['yearEdu2'],
        ciudad_pais_edu3=dictData['ciudadEdu2']+"-"+dictData['paisEdu2'],
        universidad_edu3=['universidad2'],
        )
    document.merge(
        #Professional
        fecha_inicio_fecha_fin_1=dictData['fecha_inicioPro0']+'\n'+ dictData['fecha_finPro0'],
        nombre_empresa1=dictData['empresa0'],
        job_emp1 = dictData['puestoPro0'],
        ciudad_pais_empresa1 = dictData['ciudadPro0']+'-'+ dictData['paisPro0'],
        description_empresa1 = dictData['descripcionPro0']
        )   
    if('empresa1' in dictData):
        document.merge(
        #Professional
        fecha_inicio_fecha_fin_2=dictData['fecha_inicioPro1']+'\n'+ dictData['fecha_finPro1'],
        nombre_empresa2=dictData['empresa1'],
        job_emp2 = dictData['puestoPro1'],
        ciudad_pais_empresa2 = dictData['ciudadPro1']+'-'+ dictData['paisPro1'],
        description_empresa2 = dictData['descripcionPro1']
        )
    if('empresa2' in dictData):
        document.merge(
        #Professional
        fecha_inicio_fecha_fin_3=dictData['fecha_inicioPro2']+'\n'+ dictData['fecha_finPro2'],
        nombre_empresa3=dictData['empresa2'],
        job_emp3 = dictData['puestoPro2'],
        ciudad_pais_empresa3 = dictData['ciudadPro2']+'-'+ dictData['paisPro2'],
        description_empresa3 = dictData['descripcionPro2']
        )
    document.write(path_output_file_dock)
    doc = aw.Document(path_output_file_dock)
    doc.save(path_output_file_pdf)
    
    return send_file(path_output_file_pdf, as_attachment=True)


if __name__ == '__main__': 
    app.run(port = 3002,debug=True)
