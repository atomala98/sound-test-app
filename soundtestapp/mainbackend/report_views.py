from configparser import InterpolationMissingOptionError
from .models import *
from django.http.response import HttpResponse
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
import matplotlib.pyplot as plt
from datetime import datetime, timezone
from io import BytesIO
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.shortcuts import render, redirect
import statistics

LENGTH = 21 * cm
HEIGHT = 29.7 * cm
INTERLINE = 0.8

def f_render(f):
    return str(round(f, 2))

def mean(arr):
    return sum(arr)/len(arr)

def _(n, int_a):
    return (n + int_a * INTERLINE) * cm

def get_mark(d, val):
    for key in sorted(d.keys())[::-1]:
        if key <= val:
            return d[key]

def start(request, exam_no):
    exam = Exam.objects.filter(id=exam_no).first()
    exam_results = ExaminationResult.objects.filter(exam_id=exam)
    exam_tests = ExamTest.objects.filter(exam=exam)
    result_dict = {i + 1 : {} for i, _ in enumerate(exam_tests)}
    for exam_result in exam_results:
        results = Result.objects.filter(examination_result=exam_result)
        for result in results:
            test_num = result.exam_test.test_number
            result_num = int(result.result_number)
            if result_dict[test_num].get(result_num):
                result_dict[test_num][result_num].append(int(result.result))
            else:
                result_dict[test_num][result_num] = [int(result.result)]
    canvas = create_file(exam_no)
    for test, results in result_dict.items():
        func = exam_tests[test - 1].test.function
        exec(f'{func}(results, canvas, exam_no, test)')
    canvas.save()
    
    return render(request, 'mainbackend/export_report.html', {"file_dir": f'output_reports/{exam_no}.pdf'})
    

def create_file(exam_no):
    exam = Exam.objects.filter(id=exam_no).first()
    output_dir = 'mainbackend/static/output_reports/'
    canvas = Canvas(f"{output_dir}{exam_no}.pdf", pagesize=(LENGTH, HEIGHT))
    pdfmetrics.registerFont(TTFont('Tinos', 'mainbackend/fonts/Tinos-Regular.ttf'))
    canvas.setFont("Tinos", 24)
    canvas.drawString(2 * cm, HEIGHT - 2 * cm, f"Raport z badania {exam.exam_name}")
    exam_results = ExaminationResult.objects.filter(exam_id=exam)
    exam_tests = ExamTest.objects.filter(exam=exam)
    m_persons = 0
    f_persons = 0
    persons_age = []
    for exam_result in exam_results:
        persons_age.append((datetime.now(timezone.utc) - exam_result.person_id.birth_date).days // 365)
        if exam_result.person_id.gender == "M":
            m_persons += 1
        else:
            f_persons += 1
    canvas.setFont("Tinos", 14)
    canvas.drawString(2 * cm, HEIGHT - _(3.5, 0), f"Badanie utworzone przez {exam.creator_name}. W badaniu udzia?? wzi????o {len(exam_results)} os??b")
    canvas.drawString(2 * cm, HEIGHT - _(3.5, 1), f"W badanej grupie {m_persons} os??b to m????czy??ni, a {f_persons} to kobiety.")
    canvas.drawString(2 * cm, HEIGHT - _(3.5, 2), f"Badanie sk??ada??o si?? z {len(exam_tests)} test??w, a konkretnie:")

    t = "        "

    for i, exam_test in enumerate(exam_tests):
        canvas.drawString(2 * cm, HEIGHT -  _(3.5, 3 + i), f"{t}- {exam_test.test.name}, na zestawie plik??w {exam_test.parameter_1}")
    
    canvas.showPage()

    canvas.setFont("Tinos", 24)
    canvas.drawString(2 * cm, HEIGHT - 2 * cm, f"Raport z badania {exam.exam_name}")
    
    fig = plt.figure(figsize=(4, 3))
    plt.hist(persons_age)
    plt.xlabel('Wiek (lata)')
    plt.ylabel('Ilo???? os??b')
    plt.title('Rozk??ad wieku os??b w grupie badawczej')
    plt.axvline(mean(persons_age), color='k', linestyle='dashed', linewidth=1)
    plt.text(mean(persons_age), plt.ylim()[1]*0.9, '??rednia: {:.2f}'.format(mean(persons_age)))

    imgdata = BytesIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data

    drawing=svg2rlg(imgdata)
    renderPDF.draw(drawing,canvas, 3.5 * cm, HEIGHT - _(12, 0))
    
    canvas.setFont("Tinos", 14)
    canvas.drawString(2 * cm, HEIGHT - _(13.5, 0), f"??rednia wieku os??b uczestnicz??cych w badaniu wynosi {mean(persons_age)} lat(a).")
    canvas.drawString(2 * cm, HEIGHT - _(13.5, 1), f"Mediana wieku os??b uczestnicz??cych w badaniu wynosi {statistics.median(persons_age)} lat(a).")

    return canvas


def create_page(recording, result, canvas, fileset_type, exam, test_no, files, test_name, strings):
    canvas.showPage()
    canvas.setFont("Tinos", 24)
    canvas.drawString(2 * cm, HEIGHT - 2 * cm, f"Raport z badania {exam.exam_name}")
    canvas.setFont("Tinos", 16)
    if fileset_type == 'MUSHRA Set':
        canvas.drawString(2 * cm, HEIGHT - _(3.5, 0), f"Test {test_name} (test {test_no}/{exam.test_amount}) - pr??bka {files[recording].file_label}")
    elif fileset_type == 'One File Set':
        canvas.drawString(2 * cm, HEIGHT - _(3.5, 0), f"Test {test_name} (test {test_no}/{exam.test_amount}) - pr??bka {files[recording - 1].file_label}")
    else:
        canvas.drawString(2 * cm, HEIGHT - _(3.5, 0), f"Test {test_name} (test {test_no}/{exam.test_amount}) - por??wnanie {files[2*recording - 2].file_label} - {files[2*recording - 1].file_label}")
   

    fig = plt.figure(figsize=(4, 3))
    plt.hist(result)
    plt.xlabel('Ocena')
    plt.ylabel('Ilo???? os??b')
    plt.title('Rozk??ad ocen w grupie badawczej')
    plt.axvline(mean(result), color='k', linestyle='dashed', linewidth=1)
    plt.text(mean(result), plt.ylim()[1]*0.9, '??rednia: {:.2f}'.format(mean(result)))

    imgdata = BytesIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data

    drawing=svg2rlg(imgdata)
    renderPDF.draw(drawing,canvas, 3.5 * cm, HEIGHT - _(14, 0))

    canvas.setFont("Tinos", 14)
    for i, string in enumerate(strings):
        canvas.drawString(2 * cm, HEIGHT - _(15, i), string)

    return canvas    


def ACR_test(results, canvas, exam_no, test_no):
    scales = {
        'Listening-quality scale': 'jako??ci ods??uchu', 
        'Listening-effort scale': 'wysi??ku s??uchacza',
        'Loudness-preference scale': 'preferowanej g??o??no??ci'
    }

    marks_quality = {
        5: ['Excellent', 'doskona??e'],
        4: ['Good', 'dobre'],
        3: ['Fair', 'w porz??dku'], 
        2: ['Poor', 'kiepskie'],
        1: ['Bad', 'z??e']
    }

    marks_effort = {
        5: ['Complete relaxation possible; no effort required', 'zrozumia??e bez wysi??ku'],
        4: ['Attention necessary; no appreciable effort required', 'zrozumia??e bez wi??kszego wysi??ku'],
        3: ['Moderate effort required', 'zrozumia??e przy umiarkowanym wysi??ku'], 
        2: ['Considerable effort required', 'zrozumia??e przy du??ym wysi??ku'],
        1: ['No meaning understood with any feasible effort', 'niezrozumia??e niezale??nie od wysi??ku']
    }

    marks_loudness = {
        5: ['Much louder than preferred', 'du??o g??o??niejsze ni?? powinno'],
        4: ['Louder than preferred', 'g??o??niejsze ni?? powinno'],
        3: ['Preferred', 'zrozumia??e przy umiarkowanym wysi??ku'], 
        2: ['Quieter than preferred', 'cichsze ni?? powinno'],
        1: ['Much quieter than preferred', 'du??o cichsze ni?? powinno']
    }

    marks = {
        'Listening-quality scale': marks_quality, 
        'Listening-effort scale': marks_effort,
        'Loudness-preference scale': marks_loudness
    }

    exam = Exam.objects.filter(id=exam_no).first()
    exam_test = ExamTest.objects.filter(exam=exam)[test_no - 1]
    fileset_name = exam_test.parameter_1
    scale = exam_test.parameter_3
    fileset = Fileset.objects.filter(fileset_name=fileset_name)[0]
    files = FileDestination.objects.filter(fileset=fileset).order_by('file_number')
    marks = marks[scale]

    for recording, result in results.items():
        canvas = create_page(recording=recording, 
                    result=result, 
                    canvas=canvas, 
                    fileset_type=fileset.fileset_type, 
                    exam=exam, 
                    test_no=test_no, 
                    files=files, 
                    test_name=exam_test.test.name, 
                    strings=[f"W te??cie wykorzystano skal?? {scales[scale]} ({scale}).",
                            f"??redni wynik dla tego nagrania to {f_render(mean(result))}, a wi??c nagranie zosta??o ocenione jako",
                            f"{get_mark(marks, mean(result))[1]}, ({get_mark(marks, mean(result))[0]}).",
                        ]
                    )

    return canvas


def DCR_test(results, canvas, exam_no, test_no):
    pres_methods = {
        "Pairs": "parami, bez powt??rze??",
        "Repeated pairs": "parami, z powt??rzeniem"
    }

    marks = {
        5: ['Degradation is inaudible', 'zniekszta??cenie jest nies??yszalne'],
        4: ['Degradation is audible but not annoying', 'zniekszta??cenie jest nies??yszalne, ale nie irytuj??ce'],
        3: ['Degradation is slightly annoying', 'zniekszta??cenie jest troch?? irytuj??ce'], 
        2: ['Degradation is annoying', 'zniekszta??cenie jest irytuj??ce'],
        1: ['Degradation is very annoying', 'zniekszta??cenie jest bardzo irytuj??ce']
    }

    exam = Exam.objects.filter(id=exam_no).first()
    exam_test = ExamTest.objects.filter(exam=exam)[test_no - 1]
    fileset_name = exam_test.parameter_1
    presentation = exam_test.parameter_3
    fileset = Fileset.objects.filter(fileset_name=fileset_name)[0]
    files = FileDestination.objects.filter(fileset=fileset).order_by('file_number')

    for recording_pair, result in results.items():
        canvas = create_page(recording=recording_pair, 
                    result=result, 
                    canvas=canvas, 
                    fileset_type=fileset.fileset_type, 
                    exam=exam, 
                    test_no=test_no, 
                    files=files, 
                    test_name=exam_test.test.name, 
                    strings=[f"Nagrania prezentowano {pres_methods[presentation]}.",
                            f"??redni wynik dla tego nagrania to {f_render(mean(result))}, a wi??c mo??na uzna??, ??e",
                            f"{get_mark(marks, mean(result))[1]} ({get_mark(marks, mean(result))[0]})."
                        ]
                    )

    return canvas


def CCR_test(results, canvas, exam_no, test_no):
    pres_methods = {
        "Pairs": "parami, bez powt??rze??",
        "Repeated pairs": "parami, z powt??rzeniem"
    }

    marks = {
        3: ['Much Better', 'du??o lepsza'],
        2: ['Better', 'lepsza'],
        1: ['Slightly Better', 'troch?? lepsza'], 
        0: ['About the Same', 'podobna'],
        -1: ['Slightly Worse', 'troch?? gorsza'],
        -2: ['Worse', 'gorsza'],
        -3: ['Much Worse', 'znacznie gorsza']
    }

    exam = Exam.objects.filter(id=exam_no).first()
    exam_test = ExamTest.objects.filter(exam=exam)[test_no - 1]
    fileset_name = exam_test.parameter_1
    presentation = exam_test.parameter_3
    fileset = Fileset.objects.filter(fileset_name=fileset_name)[0]
    files = FileDestination.objects.filter(fileset=fileset).order_by('file_number')

    for recording_pair, result in results.items():
        canvas = create_page(recording=recording_pair, 
                    result=result, 
                    canvas=canvas, 
                    fileset_type=fileset.fileset_type, 
                    exam=exam, 
                    test_no=test_no, 
                    files=files, 
                    test_name=exam_test.test.name, 
                    strings=[ f"Nagrania prezentowano {pres_methods[presentation]}.",
                            f"??redni wynik dla tego nagrania to {f_render(mean(result))}, a wi??c mo??na uzna??, ??e jako???? drugiego nagrania jest",
                            f"{get_mark(marks, mean(result))[1]} ({get_mark(marks, mean(result))[0]}) w stosunku do orginalnego nagrania.",
                        ]
                    )

    return canvas



def ABX_test(results, canvas, exam_no, test_no):
    exam = Exam.objects.filter(id=exam_no).first()
    exam_test = ExamTest.objects.filter(exam=exam)[test_no - 1]
    fileset_name = exam_test.parameter_1
    fileset = Fileset.objects.filter(fileset_name=fileset_name)[0]
    files = FileDestination.objects.filter(fileset=fileset).order_by('file_number')

    for recording_pair, result in results.items():
        canvas = create_page(recording=recording_pair, 
                    result=result, 
                    canvas=canvas, 
                    fileset_type=fileset.fileset_type, 
                    exam=exam, 
                    test_no=test_no, 
                    files=files, 
                    test_name=exam_test.test.name, 
                    strings=[f"R????nic?? mi??dzy nagraniami rozpozna??o {f_render(mean(result) * 100)}% badanych." ]
                    )

    return canvas


def ABCHR_test(results, canvas, exam_no, test_no):
    marks = {
        5: ['Imperceptible', 'niezauwa??alne'],
        4: ['Perceptible, but not annoying', 'zauwa??alne, ale nie irytuj??ce'],
        3: ['Slightly annoying ', 'odrobin?? irytuj??ce'], 
        2: ['Annoying', 'irytuj??ce'],
        1: ['Very annoying', 'bardzo irytuj??ce']
    }

    exam = Exam.objects.filter(id=exam_no).first()
    exam_test = ExamTest.objects.filter(exam=exam)[test_no - 1]
    fileset_name = exam_test.parameter_1
    fileset = Fileset.objects.filter(fileset_name=fileset_name)[0]
    files = FileDestination.objects.filter(fileset=fileset).order_by('file_number')

    for recording_pair, result in results.items():
        canvas = create_page(recording=recording_pair, 
                result=result, 
                canvas=canvas, 
                fileset_type=fileset.fileset_type, 
                exam=exam, 
                test_no=test_no, 
                files=files, 
                test_name=exam_test.test.name, 
                strings=[f"??redni r????nica mi??dzy referencj??, a ukrytym nagraniem testowym wynosi {f_render(mean(result))}, ",
                        f"a wi??c mo??na uzna??, ??e r????nice s?? {get_mark(marks, mean(result))[1]} ({get_mark(marks, mean(result))[0]})."]
                )

    return canvas


def MUSHRA(results, canvas, exam_no, test_no):
    exam = Exam.objects.filter(id=exam_no).first()
    exam_test = ExamTest.objects.filter(exam=exam)[test_no - 1]
    fileset_name = exam_test.parameter_1
    fileset = Fileset.objects.filter(fileset_name=fileset_name)[0]
    files = FileDestination.objects.filter(fileset=fileset).order_by('file_number')
    for recording, result in results.items():
        canvas = create_page(recording=recording, 
                result=result, 
                canvas=canvas, 
                fileset_type=fileset.fileset_type, 
                exam=exam, 
                test_no=test_no, 
                files=files, 
                test_name=exam_test.test.name, 
                strings=[f"??rednia ocena przeprocesowanego nagrania wynosi {mean(result)}."]
                )
        
    return canvas