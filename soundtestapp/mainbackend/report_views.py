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
    canvas.drawString(2 * cm, HEIGHT - _(3.5, 0), f"Badanie utworzone przez {exam.creator_name}. W badaniu udział wzięło {len(exam_results)} osób")
    canvas.drawString(2 * cm, HEIGHT - _(3.5, 1), f"W badanej grupie {m_persons} osób to mężczyźni, a {f_persons} to kobiety.")
    canvas.drawString(2 * cm, HEIGHT - _(3.5, 2), f"Badanie składało się z {len(exam_tests)} testów, a konkretnie:")

    t = "        "

    for i, exam_test in enumerate(exam_tests):
        canvas.drawString(2 * cm, HEIGHT -  _(3.5, 3 + i), f"{t}- {exam_test.test.name}, na zestawie plików {exam_test.parameter_1}")
    
    canvas.showPage()

    canvas.setFont("Tinos", 24)
    canvas.drawString(2 * cm, HEIGHT - 2 * cm, f"Raport z badania {exam.exam_name}")
    
    fig = plt.figure(figsize=(4, 3))
    plt.hist(persons_age)
    plt.xlabel('Wiek (lata)')
    plt.ylabel('Ilość osób')
    plt.title('Rozkład wieku osób w grupie badawczej')
    plt.axvline(mean(persons_age), color='k', linestyle='dashed', linewidth=1)
    plt.text(mean(persons_age), plt.ylim()[1]*0.9, 'Średnia: {:.2f}'.format(mean(persons_age)))

    imgdata = BytesIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data

    drawing=svg2rlg(imgdata)
    renderPDF.draw(drawing,canvas, 3.5 * cm, HEIGHT - _(12, 0))
    
    canvas.setFont("Tinos", 14)
    canvas.drawString(2 * cm, HEIGHT - _(13.5, 0), f"Średnia wieku osób uczestniczących w badaniu wynosi {int(mean(persons_age))} lat(a).")

    return canvas


def create_page(recording, result, canvas, fileset_type, exam, test_no, files, test_name, strings):
    canvas.showPage()
    canvas.setFont("Tinos", 24)
    canvas.drawString(2 * cm, HEIGHT - 2 * cm, f"Raport z badania {exam.exam_name}")
    canvas.setFont("Tinos", 16)
    if fileset_type == 'MUSHRA Set':
        canvas.drawString(2 * cm, HEIGHT - _(3.5, 0), f"Test {test_name} (test {test_no}/{exam.test_amount}) - próbka {files[recording].file_label}")
    elif fileset_type == 'One File Set':
        canvas.drawString(2 * cm, HEIGHT - _(3.5, 0), f"Test {test_name} (test {test_no}/{exam.test_amount}) - próbka {files[recording - 1].file_label}")
    else:
        canvas.drawString(2 * cm, HEIGHT - _(3.5, 0), f"Test {test_name} (test {test_no}/{exam.test_amount}) - porównanie {files[2*recording - 2].file_label} - {files[2*recording - 1].file_label}")
   

    fig = plt.figure(figsize=(4, 3))
    plt.hist(result)
    plt.xlabel('Ocena')
    plt.ylabel('Ilość osób')
    plt.title('Rozkład ocen w grupie badawczej')
    plt.axvline(mean(result), color='k', linestyle='dashed', linewidth=1)
    plt.text(mean(result), plt.ylim()[1]*0.9, 'Średnia: {:.2f}'.format(mean(result)))

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
        'Listening-quality scale': 'jakości odsłuchu', 
        'Listening-effort scale': 'wysiłku słuchacza',
        'Loudness-preference scale': 'preferowanej głośności'
    }

    marks_quality = {
        5: ['Excellent', 'doskonałe'],
        4: ['Good', 'dobre'],
        3: ['Fair', 'w porządku'], 
        2: ['Poor', 'kiepskie'],
        1: ['Bad', 'złe']
    }

    marks_effort = {
        5: ['Complete relaxation possible; no effort required', 'zrozumiałe bez wysiłku'],
        4: ['Attention necessary; no appreciable effort required', 'zrozumiałe bez większego wysiłku'],
        3: ['Moderate effort required', 'zrozumiałe przy umiarkowanym wysiłku'], 
        2: ['Considerable effort required', 'zrozumiałe przy dużym wysiłku'],
        1: ['No meaning understood with any feasible effort', 'niezrozumiałe niezależnie od wysiłku']
    }

    marks_loudness = {
        5: ['Much louder than preferred', 'dużo głośniejsze niż powinno'],
        4: ['Louder than preferred', 'głośniejsze niż powinno'],
        3: ['Preferred', 'zrozumiałe przy umiarkowanym wysiłku'], 
        2: ['Quieter than preferred', 'cichsze niż powinno'],
        1: ['Much quieter than preferred', 'dużo cichsze niż powinno']
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
                    strings=[f"W teście wykorzystano skalę {scales[scale]} ({scale}).",
                            f"Średni wynik dla tego nagrania to {f_render(mean(result))}, a więc nagranie zostało ocenione jako",
                            f"{get_mark(marks, mean(result))[1]}, ({get_mark(marks, mean(result))[0]}).",
                        ]
                    )

    return canvas


def DCR_test(results, canvas, exam_no, test_no):
    pres_methods = {
        "Pairs": "parami, bez powtórzeń",
        "Repeated pairs": "parami, z powtórzeniem"
    }

    marks = {
        5: ['Degradation is inaudible', 'zniekształcenie jest niesłyszalne'],
        4: ['Degradation is audible but not annoying', 'zniekształcenie jest niesłyszalne, ale nie irytujące'],
        3: ['Degradation is slightly annoying', 'zniekształcenie jest trochę irytujące'], 
        2: ['Degradation is annoying', 'zniekształcenie jest irytujące'],
        1: ['Degradation is very annoying', 'zniekształcenie jest bardzo irytujące']
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
                            f"Średni wynik dla tego nagrania to {f_render(mean(result))}, a więc można uznać, że",
                            f"{get_mark(marks, mean(result))[1]} ({get_mark(marks, mean(result))[0]})."
                        ]
                    )

    return canvas


def CCR_test(results, canvas, exam_no, test_no):
    pres_methods = {
        "Pairs": "parami, bez powtórzeń",
        "Repeated pairs": "parami, z powtórzeniem"
    }

    marks = {
        3: ['Much Better', 'dużo lepsza'],
        2: ['Better', 'lepsza'],
        1: ['Slightly Better', 'trochę lepsza'], 
        0: ['About the Same', 'podobna'],
        -1: ['Slightly Worse', 'trochę gorsza'],
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
                            f"Średni wynik dla tego nagrania to {f_render(mean(result))}, a więc można uznać, że jakość drugiego nagrania jest",
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
                    strings=[f"Różnicę między nagraniami rozpoznało {f_render(mean(result) * 100)}% badanych." ]
                    )

    return canvas


def ABCHR_test(results, canvas, exam_no, test_no):
    marks = {
        5: ['Imperceptible', 'niezauważalne'],
        4: ['Perceptible, but not annoying', 'zauważalne, ale nie irytujące'],
        3: ['Slightly annoying ', 'odrobinę irytujące'], 
        2: ['Annoying', 'irytujące'],
        1: ['Very annoying', 'bardzo irytujące']
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
                strings=[f"Średni różnica między referencją, a ukrytym nagraniem testowym wynosi {f_render(mean(result))}, ",
                        f"a więc można uznać, że różnice są {get_mark(marks, mean(result))[1]} ({get_mark(marks, mean(result))[0]})."]
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
                strings=[f"Średnia ocena przeprocesowanego nagrania wynosi {mean(result)}."]
                )
        
    return canvas